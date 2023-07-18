set
search_path to louis_v002,
logs;

create table logs.count 
(
	csuristem text,
	hitcount integer
);

drop index logs.count_csuristem_idx;

insert
	into
	logs.count (
	select
		csuristem,
		count(*) as hitcount
	from
		logs.iislog
	group by
		csuristem
);

-- spurious entries where png images are appended to the url
-- or attempts are made to overflow the incoming webserver buffer
delete
from
	logs.count
where
	length(csuristem) > 3000;

-- create index after insertion to save on indexing cost
create unique index count_csuristem_idx on
logs.count (csuristem);


-- match documents URI between crawled docs and current doc
insert into score(entity_id, score, score_type) 
with hitcountstats as (
	select
		max(hitcount) as max_hitcount,
		min(hitcount) as min_hitcount,
		1 / AVG(hitcount) as lambda
	from
		logs.count c 
)
select
	id as entity_id,
	log(hitcountstats.lambda * (hitcount - hitcountstats.min_hitcount)::float + 1) / 
	log(hitcountstats.lambda * (hitcountstats.max_hitcount - hitcountstats.min_hitcount)::float + 1)
	as score,
	'traffic' as score_type
from
	logs.count as c,
	louis_v002.crawl crawl,
	hitcountstats
where
	c.csuristem = REGEXP_REPLACE(crawl.url,
	'^https://[a-zA-Z0-9.\-]+\/',
	'/')
order by
	hitcount desc;
	
select * 
from scoring inner join crawl on scoring.entity_id = crawl.id 
order by score desc;