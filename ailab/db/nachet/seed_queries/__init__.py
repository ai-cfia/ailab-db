def seeds_urls(cursor, wanted_files_number):
    query = """
        SELECT DISTINCT
            (regexp_matches(filtered_content,
            'href="([^"]*seeds-identification[^"]*)"', 'g'))[1] AS seeds_url
        FROM (
            SELECT content AS filtered_content
            FROM html_content
            WHERE md5hash = '1a365c39a8afd80d438ddf1bd3c9afed'
        ) AS filtered_data
        LIMIT %s;
    """
    cursor.execute(query, (wanted_files_number,))
    return cursor.fetchall()

def get_seed_name(cursor, seed_full_url):
    query = (
        "SELECT regexp_replace("
        "%s, '.*seeds-identification/([^/]+).*', '\\1') AS sd_nme;"
    )
    cursor.execute(query, (seed_full_url,))
    return cursor.fetchall()

def get_webpage(cursor, url):
    query = """
        SELECT
            hc.md5hash,
            REGEXP_REPLACE(hc.content, '<[^>]+>', '', 'g') AS cleaned_content
        FROM
            html_content hc
        INNER JOIN
            crawl c ON hc.md5hash = c.md5hash
        WHERE
            c.url = %s;
    """
    cursor.execute(query, (url,))
    web_pages = cursor.fetchall()
    return web_pages

def get_images(cursor, md5hash):
    query = """
    SELECT DISTINCT
        image_links[1] AS photo_link,
        image_descriptions[1] AS photo_description
    FROM (
        SELECT
            (regexp_matches(content, 'src="([^"]+)"', 'g')) AS image_links,
            (regexp_matches(content, '<figcaption>(.*?)</figcaption>', 'gs'))
            AS image_descriptions
        FROM html_content
        WHERE md5hash = %s
    )
    AS extracted_data;
    """
    cursor.execute(query, (md5hash,))
    return cursor.fetchall()
