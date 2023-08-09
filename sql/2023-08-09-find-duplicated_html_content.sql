with hashes as (
select id, md5(html_content) as md5sum, url from crawl 
),
aggregated as(
	select array_agg(id), array_agg(url), count(*) as dups
	from hashes 
	group by md5sum
)
select * from aggregated where dups > 1