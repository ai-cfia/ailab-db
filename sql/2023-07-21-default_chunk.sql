create table default_chunk as
	select distinct(d.url), l.id, l.chunk_id  
	from documents d,
	  LATERAL (
	   SELECT dl.id, chunk_id, tokens_count
	   FROM   documents dl
	   WHERE  dl.url = d.url  -- lateral reference
	   LIMIT  1
	 ) l
	 ;