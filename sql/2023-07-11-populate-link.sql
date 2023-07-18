drop table links;
create temporary table links as
		select id, t.token as url_path from (
			select id, unnest(cast(xpath('//a/@href', html_content::xml) as text[])) as url from crawl
		) as c, ts_debug('simple', c.url) as t where t.alias = 'file';
	

create temporary table destinations as
		select id, t.token as url_path from (
			select id, f.* from crawl c, ts_debug('simple', c.url) f
		) as t where t.alias = 'url_path';
	
select d. from destinations d, links l where links.url_path = destinations.url_path;

insert into link(source_crawl_id, destination_crawl_id)
	select links.id as source_crawl_id, destinations.id as destination_crawl_id 
		from links inner join destinations on links.url_path = destinations.url_path
on conflict do nothing;

