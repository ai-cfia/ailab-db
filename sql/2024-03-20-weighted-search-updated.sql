DROP FUNCTION if exists search(text,vector,double precision,integer,jsonb);
CREATE OR REPLACE FUNCTION search(
    query text,
	query_embedding vector,
	match_threshold double precision,
	match_count integer,
	weights_parameter JSONB
)
RETURNS JSONB
AS
$BODY$
DECLARE
    similarity_search boolean;
    query_id uuid;
    query_result JSONB;
BEGIN

    create temp table weights (
        score_type score_type,
        weight double precision
    ) on commit drop;

    INSERT INTO weights
        SELECT key::score_type, value::float
        FROM jsonb_each_text(weights_parameter)
        WHERE value::float > 0.0;

    -- check if there is a query embedding, if not skip similarity search
    if query_embedding is null then
        similarity_search := false;
    else
        similarity_search := true;
        insert into query(query, embedding) values (query, query_embedding)
            on conflict do nothing
            returning id, result into query_id, query_result;

        if query_result is not null then
            return query_result;
        end if;
    end if;

    if similarity_search then
    	create temp table selected_chunks on commit drop as
			select
				ada_002.id as embedding_id,
				chunk.id as chunk_id,
				crawl.id as crawl_id,
				score,
				score_type,
				ada_002.embedding <=> query_embedding  as closeness
			    from ada_002
			    inner join "token" on ada_002.token_id = "token".id
			    inner join "chunk" on "token".chunk_id = chunk.id
			    inner join html_content_to_chunk hctc on hctc.chunk_id = chunk.id
			    inner join html_content hc on hctc.md5hash_uuid = hc.md5hash_uuid
			    inner join crawl on hc.md5hash_uuid = crawl.md5hash_uuid
			    inner join "score" on crawl.id = score.entity_id
			    order by ada_002.embedding <=> query_embedding
			    limit match_count*10;


        create temp table similarity on commit drop as
            with chunk_closest_by_id as (
                select c.crawl_id, min(c.closeness) as closeness
                    from selected_chunks c
                    group by c.crawl_id
            )
            select c.crawl_id as crawl_id, c.chunk_id as chunk_id, (1-c.closeness) as score
                from selected_chunks c
                inner join chunk_closest_by_id cc on c.crawl_id = cc.crawl_id and c.closeness = cc.closeness
                order by score desc
                limit match_count;

        create temp table measurements on commit drop as
            select s.crawl_id as id, s.chunk_id, 'similarity'::score_type as score_type, s.score as score
                from similarity s;

        insert into measurements
            select entity_id as id, chunk_id, s.score_type, s.score
                from score s
                inner join similarity sim on s.entity_id = sim.crawl_id
                where s.entity_id in (select m.id from measurements m);
    else
        -- take the longest chunk per document based on the number of tokens_count
        -- grouped by url to avoid duplicates

        create or replace temp view measurements as
            select entity_id as id, chunk_id, s.score_type, s.score
                from default_chunk d
                inner join score s on s.entity_id = d.id
                where s.score_type in (select w.score_type from weights w);
    end if;

    with matches as (
        select m.id, m.chunk_id,
            avg(m.score * w.weight) as score,
            jsonb_object_agg(m.score_type, m.score) as scores
            from measurements m
            inner join weights w on m.score_type = w.score_type
            group by m.id, m.chunk_id
            order by score desc
            limit match_count
    )
    select json_agg(r) as search from (
        select
        	query_id,
        	c.id,
        	c.url,
        	c.title,
        	ck.title as subtitle,
        	ck.text_content as content,
        	c.last_updated,
        	m.score,
        	m.scores
            from matches m
            inner join crawl c on m.id = c.id
            inner join chunk ck on m.chunk_id = ck.id
            order by m.score desc
            limit match_count
    ) r into query_result;

    if query_id is not null then
        update query set result = query_result where id = query_id;
    end if;

    return query_result;

END;
$BODY$
LANGUAGE plpgsql;
