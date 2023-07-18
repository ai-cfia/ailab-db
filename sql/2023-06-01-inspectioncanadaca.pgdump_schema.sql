--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat access method';


--
-- Name: encoding; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.encoding AS ENUM (
    'cl100k_base'
);


--
-- Name: example_function(public.vector); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.example_function(params public.vector) RETURNS TABLE(num integer)
    LANGUAGE sql
    AS $$
	select 1;
$$;


--
-- Name: match_documents(public.vector, double precision, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.match_documents(query_embedding public.vector, match_threshold double precision, match_count integer) RETURNS TABLE(id uuid, url text, title text, subtitle text, content text, similarity double precision, tokens_count integer)
    LANGUAGE sql
    AS $$
	SET ivfflat.probes = 8;
	select
	    documents.id,
	    documents.url,
	    documents.title,
	    documents.subtitle,
	    documents.content,
	    1 - (documents.embedding <=> query_embedding) as similarity,
	    documents.tokens_count as tokens_count
  	from documents
  	where 1 - (documents.embedding <=> query_embedding) > match_threshold
  	order by similarity desc
  	limit match_count;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chunk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chunk (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    crawl_id uuid,
    title text,
    text_content text
);


--
-- Name: crawl; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crawl (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    url text,
    title text,
    lang character(2),
    html_content text,
    last_crawled text,
    last_updated text
);


--
-- Name: text-embedding-ada-002; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."text-embedding-ada-002" (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    token_id uuid,
    embedding public.vector(1536)
);


--
-- Name: token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.token (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    chunk_id uuid,
    tokens integer[],
    encoding public.encoding
);


--
-- Name: documents; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.documents AS
 SELECT crawl.id,
    crawl.url,
    crawl.html_content,
    crawl.title,
    chunk.title AS subtitle,
    chunk.text_content AS content,
    embedding.embedding,
    cardinality(token.tokens) AS tokens_count
   FROM public.crawl,
    public.chunk,
    public.token,
    public."text-embedding-ada-002" embedding
  WHERE ((crawl.id = chunk.crawl_id) AND (chunk.id = token.chunk_id) AND (token.id = embedding.token_id));


--
-- Name: link; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.link (
    source_crawl_id uuid NOT NULL,
    destination_crawl_id uuid NOT NULL
);


--
-- Name: test-model; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."test-model" (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    token_id uuid,
    embedding public.vector(1536)
);


--
-- Name: chunk chunk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chunk
    ADD CONSTRAINT chunk_pkey PRIMARY KEY (id);


--
-- Name: chunk chunk_text_content_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chunk
    ADD CONSTRAINT chunk_text_content_key UNIQUE (text_content);


--
-- Name: crawl crawl_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crawl
    ADD CONSTRAINT crawl_pkey PRIMARY KEY (id);


--
-- Name: crawl crawl_url_last_updated_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crawl
    ADD CONSTRAINT crawl_url_last_updated_key UNIQUE (url, last_updated);


--
-- Name: link link_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link
    ADD CONSTRAINT link_pkey PRIMARY KEY (source_crawl_id, destination_crawl_id);


--
-- Name: test-model test-model_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."test-model"
    ADD CONSTRAINT "test-model_pkey" PRIMARY KEY (id);


--
-- Name: test-model test-model_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."test-model"
    ADD CONSTRAINT "test-model_token_id_key" UNIQUE (token_id);


--
-- Name: text-embedding-ada-002 text-embedding-ada-002_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."text-embedding-ada-002"
    ADD CONSTRAINT "text-embedding-ada-002_pkey" PRIMARY KEY (id);


--
-- Name: token token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: token token_tokens_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_tokens_key UNIQUE (tokens);


--
-- Name: chunk chunk_crawl_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chunk
    ADD CONSTRAINT chunk_crawl_uuid_fkey FOREIGN KEY (crawl_id) REFERENCES public.crawl(id);


--
-- Name: link link_destination_crawl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link
    ADD CONSTRAINT link_destination_crawl_id_fkey FOREIGN KEY (destination_crawl_id) REFERENCES public.crawl(id);


--
-- Name: link link_source_crawl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link
    ADD CONSTRAINT link_source_crawl_id_fkey FOREIGN KEY (source_crawl_id) REFERENCES public.crawl(id);


--
-- Name: test-model test-model_token_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."test-model"
    ADD CONSTRAINT "test-model_token_id_fkey" FOREIGN KEY (token_id) REFERENCES public.token(id);


--
-- Name: text-embedding-ada-002 text-embedding-ada-002_token_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."text-embedding-ada-002"
    ADD CONSTRAINT "text-embedding-ada-002_token_uuid_fkey" FOREIGN KEY (token_id) REFERENCES public.token(id);


--
-- Name: token token_chunk_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_chunk_uuid_fkey FOREIGN KEY (chunk_id) REFERENCES public.chunk(id);


--
-- PostgreSQL database dump complete
--

