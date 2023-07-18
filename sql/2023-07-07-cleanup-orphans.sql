set search_path to "louis_v003", public;

ALTER TABLE louis_v003.chunk DISABLE TRIGGER ALL;

delete from chunk where id in (
	select chunk.id from chunk left outer join crawl on chunk.crawl_id = crawl.id where crawl.id is null
);

ALTER TABLE louis_v003.chunk ENABLE TRIGGER ALL;

ALTER TABLE louis_v003.token DISABLE TRIGGER ALL;

delete from token where id in (
	select token.id from token left outer join chunk on token.chunk_id = chunk.id where chunk.id is null
);

ALTER TABLE louis_v003.token ENABLE TRIGGER ALL;

ALTER TABLE louis_v003.ada_002 DISABLE TRIGGER ALL;

delete from ada_002 where id in (
	select ada_002.id from ada_002 left outer join token on ada_002.token_id = token.id where token.id is null
);

ALTER TABLE louis_v003.ada_002 ENABLE TRIGGER ALL;