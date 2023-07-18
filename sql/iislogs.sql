-- https://www.itnota.com/import-iis-log-postgresql/
create schema logs;

-- loading
-- COPY logs.iislog FROM '/workspaces/louis-crawler/logs/iis_combined_logs_escaped_content_pages_2.log' DELIMITER ' ';
CREATE TABLE logs.iislog
(
    date date,
    "time" time without time zone,
    sip character varying(48) COLLATE pg_catalog."default",
    csmethod character varying(8) COLLATE pg_catalog."default",
    csuristem TEXT COLLATE pg_catalog."default",
    csuriquery TEXT COLLATE pg_catalog."default",
    sport character varying(4) COLLATE pg_catalog."default",
    susername character varying(256) COLLATE pg_catalog."default",
    cip character varying(48) COLLATE pg_catalog."default",
    csuseragent TEXT COLLATE pg_catalog."default",
    csreferer text COLLATE pg_catalog."default",
    scstatus integer,
    scsubstatus integer,
    scwin32status bigint,
    timetaken integer
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE logs.iislog
    OWNER to postgres;
   