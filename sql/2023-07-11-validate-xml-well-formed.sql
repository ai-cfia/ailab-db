
SELECT * 
FROM crawl  
WHERE NOT xml_is_well_formed(html_content);  
