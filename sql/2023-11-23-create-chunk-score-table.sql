CREATE TABLE chunk_score (
    id uuid default uuid_generate_v4 (),
    score FLOAT,
    score_type VARCHAR(50)
);