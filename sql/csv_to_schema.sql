CREATE OR REPLACE FUNCTION public.csv_to_schema(schema_dest TEXT, dirpath text, table_names text[]) RETURNS void AS $$
declare
   filenames RECORD;
   target_table TEXT;
   statement TEXT;
begin
FOR filenames IN
   SELECT (dirpath || '/' || table_name || '.csv') AS full_path, table_name
   FROM unnest(table_names) as table_name
loop
	target_table := schema_dest || '.' || filenames.table_name;
   	statement := 'COPY ' || target_table || ' FROM ''' || filenames.full_path ||''' DELIMITER '';'' CSV HEADER';
   	EXECUTE statement;
END LOOP;
return;
end;
$$ LANGUAGE plpgsql;

