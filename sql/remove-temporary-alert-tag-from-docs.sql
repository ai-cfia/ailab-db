-- test that this is not a greedy match
UPDATE crawl  
SET html_content = regexp_replace(html_content, '<section[^>]*class\s*=\s*"alert alert-warning"[^>]*>.*?</section>', '', 'g')  
WHERE html_content ~ '<section[^>]*class\s*=\s*"alert alert-warning"[^>]*>.*?</section>';  
