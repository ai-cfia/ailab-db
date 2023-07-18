

--
-- Name: encoding; Type: TYPE; Schema: public_new; Owner: -
--

CREATE TYPE public_new.encoding AS ENUM (
    'cl100k_base'
);


--
-- Name: example_function(public.vector); Type: FUNCTION; Schema: public_new; Owner: -
--

CREATE FUNCTION public_new.example_function(params public.vector) RETURNS TABLE(num integer)
    LANGUAGE sql
    AS $$
	select 1;
$$;


--
-- Name: match_documents(public.vector, double precision, integer); Type: FUNCTION; Schema: public_new; Owner: -
--

CREATE FUNCTION public_new.match_documents(query_embedding vector, match_threshold double precision, match_count integer) RETURNS TABLE(id uuid, url text, title text, subtitle text, content text, similarity double precision, tokens_count integer)
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
-- Name: chunk; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new.chunk (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    crawl_id uuid,
    title text,
    text_content text
);


--
-- Name: crawl; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new.crawl (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    url text,
    title text,
    lang character(2),
    html_content text,
    last_crawled text,
    last_updated text
);


--
-- Name: text-embedding-ada-002; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new."text-embedding-ada-002" (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    token_id uuid,
    embedding public.vector(1536)
);


--
-- Name: token; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new.token (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    chunk_id uuid,
    tokens integer[],
    encoding public_new.encoding
);


--
-- Name: documents; Type: VIEW; Schema: public_new; Owner: -
--

CREATE VIEW public_new.documents AS
 SELECT crawl.id,
    crawl.url,
    crawl.html_content,
    crawl.title,
    chunk.title AS subtitle,
    chunk.text_content AS content,
    embedding.embedding,
    cardinality(token.tokens) AS tokens_count
   FROM public_new.crawl,
    public_new.chunk,
    public_new.token,
    public_new."text-embedding-ada-002" embedding
  WHERE ((crawl.id = chunk.crawl_id) AND (chunk.id = token.chunk_id) AND (token.id = embedding.token_id));


--
-- Name: link; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new.link (
    source_crawl_id uuid NOT NULL,
    destination_crawl_id uuid NOT NULL
);


--
-- Name: test-model; Type: TABLE; Schema: public_new; Owner: -
--

CREATE TABLE public_new."test-model" (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    token_id uuid,
    embedding public.vector(1536)
);


--
-- Name: chunk chunk_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.chunk
    ADD CONSTRAINT chunk_pkey PRIMARY KEY (id);


--
-- Name: chunk chunk_text_content_key; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.chunk
    ADD CONSTRAINT chunk_text_content_key UNIQUE (text_content);


--
-- Name: crawl crawl_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.crawl
    ADD CONSTRAINT crawl_pkey PRIMARY KEY (id);


--
-- Name: crawl crawl_url_last_updated_key; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.crawl
    ADD CONSTRAINT crawl_url_last_updated_key UNIQUE (url, last_updated);


--
-- Name: link link_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.link
    ADD CONSTRAINT link_pkey PRIMARY KEY (source_crawl_id, destination_crawl_id);


--
-- Name: test-model test-model_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new."test-model"
    ADD CONSTRAINT "test-model_pkey" PRIMARY KEY (id);


--
-- Name: test-model test-model_token_id_key; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new."test-model"
    ADD CONSTRAINT "test-model_token_id_key" UNIQUE (token_id);


--
-- Name: text-embedding-ada-002 text-embedding-ada-002_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new."text-embedding-ada-002"
    ADD CONSTRAINT "text-embedding-ada-002_pkey" PRIMARY KEY (id);


--
-- Name: token token_pkey; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: token token_tokens_key; Type: CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.token
    ADD CONSTRAINT token_tokens_key UNIQUE (tokens);


--
-- Name: chunk chunk_crawl_uuid_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.chunk
    ADD CONSTRAINT chunk_crawl_uuid_fkey FOREIGN KEY (crawl_id) REFERENCES public_new.crawl(id);


--
-- Name: link link_destination_crawl_id_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.link
    ADD CONSTRAINT link_destination_crawl_id_fkey FOREIGN KEY (destination_crawl_id) REFERENCES public_new.crawl(id);


--
-- Name: link link_source_crawl_id_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.link
    ADD CONSTRAINT link_source_crawl_id_fkey FOREIGN KEY (source_crawl_id) REFERENCES public_new.crawl(id);


--
-- Name: test-model test-model_token_id_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new."test-model"
    ADD CONSTRAINT "test-model_token_id_fkey" FOREIGN KEY (token_id) REFERENCES public_new.token(id);


--
-- Name: text-embedding-ada-002 text-embedding-ada-002_token_uuid_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new."text-embedding-ada-002"
    ADD CONSTRAINT "text-embedding-ada-002_token_uuid_fkey" FOREIGN KEY (token_id) REFERENCES public_new.token(id);


--
-- Name: token token_chunk_uuid_fkey; Type: FK CONSTRAINT; Schema: public_new; Owner: -
--

ALTER TABLE ONLY public_new.token
    ADD CONSTRAINT token_chunk_uuid_fkey FOREIGN KEY (chunk_id) REFERENCES public_new.chunk(id);


--
-- PostgreSQL database dump complete
--

