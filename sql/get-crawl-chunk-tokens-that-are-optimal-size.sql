-- select count(*) from chunk;
-- select round(avg(length(text_content))) from chunk;

select *
from (
	select url, lang, crawl.title as title, chunk.title as subtitle, text_content, ARRAY_LENGTH(tokens,1) as length_tokens
	from crawl, chunk, token
	where crawl.id = chunk.crawl_id and token.chunk_id = chunk.id 
) as chunks
where length_tokens >= 256 and length_tokens <= 512;
