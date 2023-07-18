drop schema louis_v002 cascade;

alter table public."text-embedding-ada-002" rename table to ada_002;

alter table public.ada_002 rename constraint "text-embedding-ada-002_token_uuid_fkey" to ada_002_token_uuid_fkey;

select
	*
from
	clone_schema('public',
	'louis_v002',
	false);

select
	*
from
	csv_to_schema('louis_v002',
	'/workspaces/louis-crawler/db/dumps/louis_v000',
	array['crawl',
	'link',
	'chunk',
	'token',
	'ada_002']);

select
	*
from
	louis_v000_to_louis_v002();

delete
from
	crawl
where
	last_updated is null;

delete from crawl where title = 'Test Title';

select
	*
from
	schema_to_csv('louis_v002',
	'/workspaces/louis-crawler/db/dumps/louis_v002');