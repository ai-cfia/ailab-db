CREATE OR REPLACE FUNCTION search(
	query_embedding vector, 
	match_threshold double precision, 
	match_count integer,
	weights JSONB
) 
RETURNS TABLE(
    id uuid, 
    url text, 
    title text, 
    subtitle text, 
    content text, 
    tokens_count integer, 
    last_updated text, 
    score double precision,
    scores jsonb
)
AS
$BODY$
DECLARE
    similarity_search boolean;
BEGIN
    create temp table weights (
        score_type score_type,
        weight double precision
    );

    INSERT INTO weights  
        SELECT key::score_type, value::float 
        FROM jsonb_each_text(weights)
        WHERE value::float > 0.0;

    -- check if there is a query embedding, if not skip similarity search
    if query_embedding is null then
        similarity_search := false;
    else
        similarity_search := true;
    end if;

    if similarity_search then
        create temp table similarity as
            -- to use the index, must use a match_threshold where condition, an order by and a limit
            with selected_chunks as (
                select d.id, d.chunk_id, d.embedding operator(<=>) query_embedding as closeness
                    from documents d
                    where d.embedding operator(<=>) query_embedding < match_threshold
                    order by d.embedding operator(<=>) query_embedding
                    limit match_count*10
            ),
            chunk_closest_by_id as (
                select c.id, min(c.closeness) as closeness
                    from selected_chunks c
                    group by c.id
            )
            select c.id as id, c.chunk_id as chunk_id, (1-c.closeness) as score
                from selected_chunks c
                inner join chunk_closest_by_id cc on c.id = cc.id and c.closeness = cc.closeness
                order by score desc
                limit match_count;

        create temp table measurements as
            select s.id, s.chunk_id, 'similarity'::score_type as score_type, s.score as score
                from similarity s;
        
        insert into measurements
            select entity_id as id, chunk_id, s.score_type, s.score 
                from score s
                inner join similarity sim on s.entity_id = sim.id
                where s.entity_id in (select m.id from measurements m);
    else
        -- take the longest chunk per document based on the number of tokens_count
        -- grouped by url to avoid duplicates

        create temp view measurements as
            select entity_id as id, chunk_id, s.score_type, s.score 
                from default_chunk d
                inner join score s on s.entity_id = d.id
                where s.score_type in (select w.score_type from weights w);   
    end if;

    return query
        with matches as (
            select m.id, m.chunk_id,
                sum(m.score * w.weight) as score,
                jsonb_object_agg(m.score_type, m.score) as scores
                from measurements m
                inner join weights w on m.score_type = w.score_type
                group by m.id, m.chunk_id
                order by score desc
                limit match_count
        )
        select d.id, d.url, d.title, d.subtitle, d.content, d.tokens_count, d.last_updated, m.score, m.scores
            from matches m
            inner join documents d on m.id = d.id 
            and m.chunk_id = d.chunk_id
            order by m.score desc
            limit match_count;
END;
$BODY$
LANGUAGE plpgsql;

COMMENT ON FUNCTION search IS 
$COMMENT$
    Searches for similar documents to the query embedding taking 
    into account the weights on the different existing measurements of the 
    document. 

    similarity search is done on chunks from each document.

    There are multiple chunks per document and each chunk has a vector embeddings.
$COMMENT$;

