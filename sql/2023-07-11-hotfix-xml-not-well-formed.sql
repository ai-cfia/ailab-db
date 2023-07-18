update crawl
set html_content = regexp_replace(html_content, '<div class="small">', '', 'g')
where id = '3eec740f-59f6-44ba-a9f5-73d0d44dc71a' or id = 'e9a64ea3-c7c4-4f0e-bd49-c4e1d9de1a7f';
