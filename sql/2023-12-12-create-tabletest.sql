-- Set the search path to the louis_0.0.6 schema
SET
    search_path TO "louis_0.0.6";
    
CREATE TABLE  (
    content VARCHAR(255) -- Change 255 to the desired length of the string
);

TRUNCATE TABLE tabletest;

CREATE TABLE tabletest (
    id SERIAL PRIMARY KEY,
    html_content TEXT
);

INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
INSERT INTO tabletest (html_content) VALUES ('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
