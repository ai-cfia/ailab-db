update crawl 
set url = new_url
from (
	select crawl.id as id, replace(url, token, 'inspection.canada.ca') as new_url from crawl, ( 
		select id, token from (
			SELECT c.id as id, t.alias as alias, t.token as token
			FROM  crawl c, ts_debug('english', url) t
		) as subquery
		where alias = 'host' and token <> 'inspection.canada.ca' 
	) as subquery2
	where crawl.id = subquery2.id 
) subquery3
where subquery3.id = crawl.id
and not exists (
	select 1 from crawl where url = new_url
);