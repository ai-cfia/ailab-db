delete from crawl where id in ( 
	select id from crawl where title = 'Test Title'
)