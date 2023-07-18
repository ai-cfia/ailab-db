
-- '%<section id="archived-bnr" class="wb-overlay modal-content overlay-def wb-bar-t">%'

create temporary table archives as
	select id, xpath_exists('//section[@id="archived-bnr"]',html_content::xml) as archived 
	from crawl;
	
alter type score_type add value if not exists 'current';

insert into score(entity_id, score, score_type)
	select id, 0, 'current' from archives where archived = true;

insert into score(entity_id, score, score_type)
	select id, 1, 'current' from archives where archived = false;