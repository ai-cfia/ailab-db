CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

create table if not exists crawl (
	id uuid default uuid_generate_v4 (),
	url text,
	title text,
	lang char(2),
	html_content text,
	last_crawled text,
	last_updated text,
	primary key(id),
	unique(url, last_updated)
);

create table if not exists link (
	source_crawl_id uuid references crawl(id),
	destination_crawl_id uuid references crawl(id),
	primary key(source_crawl_id, destination_crawl_id)
);

create table if not exists chunk (
	id uuid default uuid_generate_v4 (),
	crawl_id uuid references crawl(id),
	title text,
	text_content text,
	primary key(id),
	unique(text_content)
);

create table if not exists token (
	id uuid default uuid_generate_v4 (),
	chunk_id uuid references chunk(id),
	tokens INTEGER[],
	encoding text default 'cl100k_base',
	primary key(id),
	unique(tokens)
);

create table if not exists "ada_002" (
	id uuid default uuid_generate_v4 (),
	token_id uuid references token(id),
	embedding vector(1536),
	primary key(id),
	unique(token_id)
);

drop view documents;

create view documents as(
	select
		crawl.id as id,
		crawl.url as url,
		crawl.html_content as html_content,
		crawl.title as title,
		chunk.title as subtitle,
		chunk.text_content as content,
		embedding.embedding as embedding,
		cardinality(token.tokens) as tokens_count
	from crawl, chunk, token, "ada_002" as embedding
	where crawl.id = chunk.crawl_id
	and chunk.id = token.chunk_id
	and token.id = embedding.token_id
);

create or replace function match_documents (
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
  tokens_count integer
)
language sql volatile
as $$
	SET ivfflat.probes = 8;
	select
	    documents.id,
	    documents.url,
	    documents.title,
	    documents.subtitle,
	    documents.content,
	    1 - (documents.embedding <=> query_embedding) as similarity,
	    documents.tokens_count as tokens_count
  	from documents
  	where 1 - (documents.embedding <=> query_embedding) > match_threshold
  	order by similarity desc
  	limit match_count;
$$;

-- https://github.com/pgvector/pgvector
-- lists: rows / 1000 for up to 1M rows and sqrt(rows) for over 1M rows
-- probes: lists / 10 for up to 1M rows and sqrt(lists) for over 1M rows
-- 83K records = 83 lists and 8 probes
create index if not exists t_ada002_embedding_cosine_idx
	ON "ada_002"
	USING ivfflat (embedding vector_cosine_ops) WITH (lists = 83);
