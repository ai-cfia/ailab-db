ALTER TABLE crawl DISABLE TRIGGER ALL; 
ALTER TABLE chunk DISABLE TRIGGER ALL; 
ALTER TABLE token DISABLE TRIGGER ALL; 
ALTER TABLE ada_002 DISABLE TRIGGER ALL; 

EXPLAIN (ANALYZE, BUFFERS) delete from crawl where url like 'https://www.inspection.gc.ca/%' and id in (select id from crawl limit 1);

delete from crawl where url like 'https://www.inspection.gc.ca/%';

ALTER TABLE crawl ENABLE TRIGGER ALL; 
ALTER TABLE chunk ENABLE TRIGGER ALL; 
ALTER TABLE token ENABLE TRIGGER ALL; 
ALTER TABLE ada_002 ENABLE TRIGGER ALL; 

select * from crawl where url not like 'https://inspection.canada.ca/%';

reindex table crawl;

vacuum analyze;