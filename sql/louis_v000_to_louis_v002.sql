CREATE OR REPLACE FUNCTION louis_v000_to_louis_v002() RETURNS void AS $$
begin
	set search_path to 'louis_v002', 'public';

	create table if not exists louis_v002.query (
		id uuid default uuid_generate_v4 (),
		query text,
		tokens INTEGER[],
		embedding vector(1536),
		encoding text default 'cl100k_base',
		model text default 'ada_002',
		primary key(id),
		unique(tokens)
	);


	if not exists (select 1 from pg_type where typname = 'score_type') then
		CREATE type score_type AS ENUM ('recency');
	end if;

	create table if not exists louis_v002.score(
		entity_id uuid,
		score float,
		score_type score_type
	);
	
	ALTER TABLE louis_v002.crawl ADD column if not exists last_updated_date date;
	
	update louis_v002.crawl set last_updated = '2018-12-14' where last_updated = '2018-14-12';
	
	update louis_v002.crawl set last_updated_date = date(last_updated);
	
	
	-- documents last update follow an exponential curve distribution of date values that we want to normalize so that 0 is the oldest document and 1 is the most recent document.
	
	--One way to normalize the exponential curve distribution of date values so that 0 is the oldest document and 1 is the most recent document is to use the cumulative distribution function (CDF) of the exponential distribution. The CDF of the exponential distribution is given by:
	--
	--F(x) = 1 - e^(-λx)
	--
	--where λ is the rate parameter of the exponential distribution and x is the date value. To normalize the data, you can use the following formula:
	--
	--normalized_value = F(x) / F(max)
	--
	--where F(max) is the CDF value at the maximum date value in your dataset. This will transform the date values into a range of [0, 1] that is evenly distributed according to the exponential distribution.
	
	insert into louis_v002.score (entity_id, score, score_type)
		SELECT
		  id,
		  (1.0 - EXP(lambda * (last_updated_date - min_date)::float) ) /
		  (1.0 - EXP(lambda * (max_date - min_date)::float)) as normalized_value,
		  'recency'
		FROM louis_v002.crawl,
		     (SELECT 1 / AVG('now' - last_updated_date) as lambda, MIN(last_updated_date) as min_date, MAX(last_updated_date) as max_date FROM louis_v002.crawl) as date_range
		order by last_updated_date asc;
	
	
	drop view if exists louis_v002.documents;
	drop view if exists louis_v002.scoring;
	
	create view louis_v002.scoring as(
		select
			entity_id,
			avg(score) as score
		from score
		group by entity_id
	);
	
	
	create view louis_v002.documents as(
		select
			crawl.id as id,
			crawl.url as url,
			crawl.html_content as html_content,
			crawl.title as title,
			chunk.title as subtitle,
			chunk.text_content as content,
			embedding.embedding as embedding,
			cardinality(token.tokens) as tokens_count,
			crawl.last_updated as last_updated,
			scoring.score as score
		from crawl, chunk, token, "ada_002" as embedding, scoring
		where crawl.id = chunk.crawl_id
			and chunk.id = token.chunk_id
			and token.id = embedding.token_id
			and crawl.id = scoring.entity_id
	);
	

	create or replace function louis_v002.match_documents (
	  query_embedding vector(1536),
	  match_threshold float,
	  match_count int
	)
	returns table (
	  id uuid,
	  url text,
	  title text,
	  subtitle text,
	  content text,
	  similarity float,
	  tokens_count integer,
	  last_updated text,
	  score float
	)
	language sql volatile
	as $match_documents$
		SET ivfflat.probes = 8;
		with documents as (
			select documents.*, 1 - (documents.embedding <=> query_embedding) as similarity
			from documents
		)
		select
		    documents.id,
		    documents.url,
		    documents.title,
		    documents.subtitle,
		    documents.content,
		    similarity,
		    documents.tokens_count as tokens_count,
		    documents.last_updated as last_updated,
		    documents.score as score
	  	from documents
	  	where similarity > match_threshold
	  	order by (score + similarity) / 2 desc
	  	limit match_count;
	$match_documents$;
	
	ALTER TABLE louis_v002.chunk DROP CONSTRAINT chunk_crawl_uuid_fkey;
	ALTER TABLE louis_v002.chunk ADD CONSTRAINT chunk_crawl_uuid_fkey FOREIGN KEY (crawl_id) REFERENCES louis_v002.crawl(id) ON DELETE CASCADE;
	ALTER TABLE louis_v002."token" DROP CONSTRAINT token_chunk_uuid_fkey;
	ALTER TABLE louis_v002."token" ADD CONSTRAINT token_chunk_uuid_fkey FOREIGN KEY (chunk_id) REFERENCES louis_v002.chunk(id) ON DELETE CASCADE;
	ALTER TABLE louis_v002.link DROP CONSTRAINT link_source_crawl_id_fkey;
	ALTER TABLE louis_v002.link ADD CONSTRAINT link_source_crawl_id_fkey FOREIGN KEY (source_crawl_id) REFERENCES louis_v002.crawl(id) ON DELETE CASCADE;
	ALTER TABLE louis_v002.link DROP CONSTRAINT link_destination_crawl_id_fkey;
	ALTER TABLE louis_v002.link ADD CONSTRAINT link_destination_crawl_id_fkey FOREIGN KEY (destination_crawl_id) REFERENCES louis_v002.crawl(id) ON DELETE CASCADE;
	ALTER TABLE louis_v002."ada_002" DROP CONSTRAINT "ada_002_token_uuid_fkey";
	ALTER TABLE louis_v002."ada_002" ADD CONSTRAINT "ada_002_token_uuid_fkey" FOREIGN KEY (token_id) REFERENCES louis_v002."token"(id) ON DELETE CASCADE;
end;
$$ LANGUAGE plpgsql;