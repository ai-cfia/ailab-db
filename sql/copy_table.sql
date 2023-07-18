CREATE OR REPLACE FUNCTION public.copy_table(
    source_schema text,
    dest_schema text,
    table_name text)
  RETURNS void AS
$BODY$
BEGIN
	EXECUTE 'INSERT INTO ' || dest_schema || '.' || quote_ident(table_name) || ' SELECT * FROM ' || quote_ident(source_schema) || '.' || quote_ident(table_name) || ';';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION copy_table(text, text, text)
  OWNER TO postgres;
  