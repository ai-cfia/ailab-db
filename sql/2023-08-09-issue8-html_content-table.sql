-- because the same html_content can be used by multiple crawl entries
-- we modify the crawl table by moving the column html_content to a new table html_content
-- and add a foreign key to the crawl table to html_content
-- we also modify chunk, originally linked to the crawl table as follows:
-- * the same chunk (example: this page has been archived can be extracted from different crawl entries (and html_content)
--   even when these pages are not the same (do not have the same md5sum hash)
-- * we add an N:N relation between chunk and html_content

-- original tables:
---
-- CREATE TABLE crawl (
-- 	id uuid NOT NULL DEFAULT uuid_generate_v4(),
-- 	url text NULL,
-- 	title text NULL,
-- 	lang bpchar(2) NULL,
-- 	html_content text NULL,
-- 	last_crawled text NULL,
-- 	last_updated text NULL,
-- 	last_updated_date date NULL,
-- 	CONSTRAINT crawl_pkey PRIMARY KEY (id),
-- 	CONSTRAINT crawl_url_last_updated_key UNIQUE (url, last_updated)
-- );
--
-- CREATE TABLE chunk (
-- 	id uuid NOT NULL DEFAULT uuid_generate_v4(),
-- 	crawl_id uuid NULL,
-- 	title text NULL,
-- 	text_content text NULL,
-- 	CONSTRAINT chunk_pkey PRIMARY KEY (id),
-- 	CONSTRAINT chunk_text_content_key UNIQUE (text_content),
-- 	CONSTRAINT chunk_crawl_uuid_fkey FOREIGN KEY (crawl_id) REFERENCES crawl(id) ON DELETE CASCADE
-- );

CREATE table if not EXISTS html_content (
  content text NOT NULL,
  md5hash CHAR(32) NOT NULL,
  CONSTRAINT html_content_md5hash_key UNIQUE (md5hash)
);

ALTER TABLE crawl
    ADD COLUMN md5hash CHAR(32);

-- the tables crawl and chunk already contain data so we need to move the data to the new table first before applying constraints
-- on duplicate key value

UPDATE crawl
  SET md5hash = md5(html_content);

INSERT INTO html_content (content, md5hash)
  SELECT html_content, md5hash FROM crawl
ON CONFLICT (md5hash) DO NOTHING;

-- we create N:N mapping between html_content and chunk
-- as from different html_content it is possible to extract
-- the same chunk even if not all chunks are the same
CREATE table html_content_to_chunk (
  html_content_md5hash CHAR(32) NOT NULL,
  chunk_id uuid NOT NULL
);

insert into html_content_to_chunk (html_content_md5hash, chunk_id)
  select crawl.md5hash, chunk.id
    from chunk
      join crawl on chunk.crawl_id = crawl.id;

-- we add constraint AFTER insertion for better performance
ALTER TABLE html_content_to_chunk
  ADD CONSTRAINT html_content_to_chunk_pkey PRIMARY KEY (html_content_md5hash, chunk_id),
  ADD CONSTRAINT html_content_to_chunk_html_content_md5hash_fkey FOREIGN KEY (html_content_md5hash) REFERENCES html_content(md5hash) ON DELETE CASCADE,
  ADD CONSTRAINT html_content_to_chunk_chunk_id_fkey FOREIGN KEY (chunk_id) REFERENCES chunk(id) ON DELETE CASCADE;

CREATE OR REPLACE VIEW documents
AS SELECT crawl.id,
    chunk.id AS chunk_id,
    crawl.url,
    html_content.content as html_content,
    crawl.title,
    chunk.title AS subtitle,
    chunk.text_content AS content,
    embedding.embedding,
    cardinality(token.tokens) AS tokens_count,
    crawl.last_updated,
    scoring.score
   FROM crawl,
    html_content,
    html_content_to_chunk,
    chunk,
    token,
    ada_002 embedding,
    scoring
  WHERE chunk.id = token.chunk_id
    AND token.id = embedding.token_id
    AND crawl.id = scoring.entity_id
    AND crawl.md5hash = html_content.md5hash
    AND html_content_to_chunk.html_content_md5hash = html_content.md5hash
    AND html_content_to_chunk.chunk_id = chunk.id;

ALTER TABLE chunk
  DROP CONSTRAINT chunk_crawl_uuid_fkey,
  DROP COLUMN crawl_id;

alter table crawl
  drop column html_content;