CREATE OR REPLACE FUNCTION schema_to_csv(schema_source TEXT, path TEXT) RETURNS void AS $$
declare
   tables RECORD;
   statement TEXT;
begin
FOR tables IN
   SELECT (table_schema || '.' || table_name) AS schema_table, table_schema, table_name
   FROM information_schema.tables t INNER JOIN information_schema.schemata s
   ON s.schema_name = t.table_schema
   WHERE t.table_schema = schema_source
   AND t.table_type NOT IN ('VIEW')
   ORDER BY schema_table
LOOP
   statement := 'COPY ' || tables.schema_table || ' TO ''' || path || '/' || tables.table_name || '.csv' ||''' DELIMITER '';'' CSV HEADER';
   EXECUTE statement;
END LOOP;
return;
end;
$$ LANGUAGE plpgsql;

