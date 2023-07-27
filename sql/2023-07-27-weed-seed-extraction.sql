
with urls as (
	select id, unnest(cast(xpath('//a/@href', html_content::xml) as text[])) as url 
	from crawl
	where url = 'https://inspection.canada.ca/plant-health/seeds/seed-testing-and-grading/seeds-identification/eng/1333136604307/1333136685768'
)
select * from urls where url like '/plant-health%'

with start_page as (
	select id
	from crawl
	where url = 'https://inspection.canada.ca/plant-health/seeds/seed-testing-and-grading/seeds-identification/eng/1333136604307/1333136685768'
),
html_content as (
	select crawl.id, title, html_content from start_page, link inner join crawl on link.destination_crawl_id = crawl.id 
	where source_crawl_id = start_page.id
),
headers as (
	select id, unnest(cast(xpath('//h2/text()', html_content::xml) as text[])) as h2 from html_content
),
headers_with_rows as (
	select id, h2, row_number() over (partition by id) from headers 
),
max_row_numbers as (
	select id, max(row_number) as max_row_number from headers_with_rows group by id
),
pairwise as (
	select headers_with_rows.id, row_number as row_number_start, row_number+1 as row_number_end from headers_with_rows 
	inner join max_row_numbers on headers_with_rows.id = max_row_numbers.id 
	where row_number < max_row_number
)
select pairwise.id, row_number_start, row_number_end, cast(
	xpath('//h2[' || row_number_start || '] | //*[following-sibling::h2[' || row_number_start || '] and preceding-sibling::h2['|| row_number_end || ']]', html_content::xml) 
 as text[])
	from pairwise
inner join html_content on pairwise.id = html_content.id