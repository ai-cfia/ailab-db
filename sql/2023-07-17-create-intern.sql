drop function if exists public.create_intern;
create or replace function public.create_intern(
	email text, 
	secret text) 
returns text as 
$BODY$
begin
	if not exists ( select from PG_CATALOG.pg_roles where rolname = email) then
		execute FORMAT('CREATE ROLE %I LOGIN PASSWORD %L', email, secret);
	else
		execute FORMAT('ALTER ROLE %I WITH PASSWORD %L', email, secret);
	end if;
	execute FORMAT('CREATE SCHEMA IF NOT EXISTS %I', email);
	execute format('GRANT ALL ON SCHEMA %I TO %I', email, email);
	execute format('grant usage on schema %I to %I', 'louis_v004', email);
	execute format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I', 'louis_v004', email);
	return email;
end;
$BODY$
language plpgsql strict VOLATILE SECURITY DEFINER;

ALTER FUNCTION public.create_intern(text, text)
  OWNER TO postgres;