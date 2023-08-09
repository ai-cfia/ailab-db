select count(*) 
from crawl left join chunk 
on crawl.id = chunk.crawl_id 
where chunk.crawl_id is null