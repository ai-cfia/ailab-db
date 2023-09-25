ALTER TABLE crawl ADD CONSTRAINT crawl_to_html_content_md5hash_fkey FOREIGN KEY (md5hash) REFERENCES html_content(md5hash) ON DELETE cascade;
ALTER TABLE default_chunks ADD CONSTRAINT default_chunks_to_chunk_fkey FOREIGN KEY (chunk_id) REFERENCES chunk(id) ON DELETE cascade;
ALTER TABLE html_content_to_chunk RENAME COLUMN html_content_md5hash TO md5hash;
