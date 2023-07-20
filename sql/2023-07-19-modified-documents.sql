drop view if exists documents;
CREATE OR REPLACE VIEW documents
AS SELECT 
    crawl.id,
    chunk.id AS chunk_id,
    crawl.url,
    crawl.html_content,
    crawl.title,
    chunk.title AS subtitle,
    chunk.text_content AS content,
    embedding.embedding,
    cardinality(token.tokens) AS tokens_count,
    crawl.last_updated,
    scoring.score
   FROM crawl,
    chunk,
    token,
    ada_002 embedding,
    scoring
  WHERE crawl.id = chunk.crawl_id AND chunk.id = token.chunk_id AND token.id = embedding.token_id AND crawl.id = scoring.entity_id;