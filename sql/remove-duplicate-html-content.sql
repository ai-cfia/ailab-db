DELETE FROM crawl  
WHERE id NOT IN (  
  SELECT id  
  FROM (  
    SELECT id, ROW_NUMBER() OVER (  
      PARTITION BY md5(html_content)  
      ORDER BY last_crawled DESC  
    ) AS rn  
    FROM crawl  
  ) subquery  
  WHERE subquery.rn = 1  
);  