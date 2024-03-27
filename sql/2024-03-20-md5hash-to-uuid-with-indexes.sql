ALTER TABLE html_content ADD md5hash_uuid uuid;
ALTER TABLE html_content_to_chunk ADD md5hash_uuid uuid;
ALTER TABLE crawl ADD md5hash_uuid uuid;

update html_content set md5hash_uuid = md5hash::uuid;
update html_content_to_chunk set md5hash_uuid = md5hash::uuid;
update crawl set md5hash_uuid = md5hash::uuid;

create index html_content_to_chunk_md5hash_uuid_idx on html_content_to_chunk(md5hash_uuid);
create index html_content_to_chunk_md5hash_uuid_idx on html_content(md5hash_uuid);
create index crawl_md5hash_uuid_idx on crawl(md5hash_uuid);
