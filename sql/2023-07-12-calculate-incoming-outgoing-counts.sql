drop table counts;
create temporary table counts as
	select incoming.id, incoming_count, outgoing_count, (incoming_count - outgoing_count) as net_count from (
		select destination_crawl_id as id, count(*) as incoming_count from link group by destination_crawl_id 
	) as incoming, (
		select source_crawl_id as id, count(*) as outgoing_count from link group by source_crawl_id 
	) as outgoing
	where incoming.id = outgoing.id
	order by net_count asc;

create temporary table net_count_score as
(
	with total as(
		select count(*) as count_rows from counts 
	),
	per_value as (
		SELECT net_count, count(*) as items
		FROM counts cross join total 
		GROUP BY net_count
		ORDER BY net_count
	),
	prob as (
		select net_count, items, (items/total.count_rows::float) as base_score
		from per_value cross join total 
	),
	probstat as (
		select max(base_score) as max_base_score
		from prob
	)
	select net_count, items, base_score/max_base_score as score
	from prob cross join probstat
);


alter type score_type add value if not exists 'typicality';

insert into score(entity_id, score_type, score) 
	select id as entity_id, 'typicality' as score_type, score from counts join net_count_score on net_count_score.net_count = counts.net_count;


--drop table stats;
--create temporary table stats as (
--	select 
--		avg(incoming_count) as avg_incoming_count, 
--		max(incoming_count) as max_incoming_count,
--		min(incoming_count) as min_incoming_count,
--		avg(outgoing_count) as avg_outgoing_count, 
--		avg(net_count) as avg_netcount,
--		stddev(incoming_count) as stddev_incoming_count,
--		stddev(outgoing_count) as stddev_outgoing_count,
--		stddev(net_count) as stddev_net_count
--	from counts
--);
