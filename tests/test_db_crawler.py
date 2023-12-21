"""test database functions"""
import unittest
import ailab.db as db
import ailab.db.crawler as crawler
import tests.testing_utils as test

class TestDBCrawler(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_link_pages_and_fetch_links(self):
        """sample test to check if link_pages works"""
        with db.cursor(self.connection) as cursor:
            source_url = "https://inspection.canada.ca/preventive-controls/sampling-procedures/eng/1518033335104/1528203403149"
            destination_url = "https://inspection.canada.ca/animal-health/terrestrial-animals/exports/pets/australia/eng/1321292836314/1321292933011"
            crawler.link_pages(cursor, source_url, destination_url)
            links = crawler.fetch_links(cursor, source_url)
            self.connection.rollback()
        self.assertTrue(destination_url in links)

    def test_fetch_crawl_row_by_http_url(self):
        """sample test to check if fetch_crawl_row works"""
        with db.cursor(self.connection) as cursor:
            row = crawler.fetch_crawl_row(
                cursor,
                "https://inspection.canada.ca/a-propos-de-l-acia/structure-organisationnelle/mandat/fra/1299780188624/1319164463699"
                )
            self.connection.rollback()
        self.assertEqual(row['url'], "https://inspection.canada.ca/a-propos-de-l-acia/structure-organisationnelle/mandat/fra/1299780188624/1319164463699")
        self.assertEqual(
            row['title'],
            "Mandat - Agence canadienne d'inspection des aliments")

    def test_fetch_crawl_row_by_postgresql_url(self):
        """sample test to check if fetch_crawl_row works"""
        url = db.create_postgresql_url(
            "DBNAME",
            "crawl",
            "8b25a4d3-bd83-412d-8cd8-0fd969f28efc")
        with db.cursor(self.connection) as cursor:
            row = crawler.fetch_crawl_row(
                cursor,
                url
                )
            self.connection.rollback()
        self.assertEqual(row['url'], "https://inspection.canada.ca/preventive-controls/sampling-procedures/eng/1518033335104/1528203403149")
        self.assertEqual(
            row['title'],
            "Sampling procedures - Canadian Food Inspection Agency")

    def test_fetch_chunk_id_without_embedding(self):
        """sample test to check if fetch_chunk_id_without_embedding works"""
        with db.cursor(self.connection) as cursor:
            cursor.execute(test.embedding_table.format(embedding_model='test-model'))
            rows = crawler.fetch_chunk_id_without_embedding(cursor, 'test-model')
            _entity_id = rows[0]
            self.connection.rollback()

    def test_store_chunk_item(self):
        """Test storing a chunk item."""
        with db.cursor(self.connection) as cursor:
            item = {
                "url": "https://inspection.canada.ca/a-propos-de-l-acia/fra/1299008020759/1299008778654",
                "title": "À propos de l'ACIA - Agence canadienne d'inspection des aliments",
                "text_content": "This is an example content.",
                "tokens": [73053,10045,409,326,6,1741,5987,2998,37622,934,6,8629,44618,409,38682,1001,367,3869,348,2328,7330,52760,11,326,6,1741,5987,264,653,348,5642,11837,266,7930,2995,64097,1208,4371,392,1018,978,38450,12267,11,1208,77323,951,4039,12249,11,1208,9313,951,348,19395,978,2629,2249,1880,326,69537,12416,8065,84751,6625,13,17360,535,89,551,5690,6405,13674,33867,14318,3765,91080,1370,2126,22811,11876,459,5979,729,3539,5512,409,326,6,1741,5987,56311,39929,64079,3869,951,90108,35933,46680,969,645,551,2009,85182,40280,3930,7008,90108,1082,3625,459,5979,729,3539,5512,5019,3625,4824,76,1154,25540,5512,1370,514,72601,409,2343,68,2405,10610,953,13,2998,62163,42145,40948,5512,294,6,97675,4149,3462,16848,85046,1880,83229,70,91555,11683,12416,3869,326,6,26125,1880,1208,9313,951,5790,325,625,3808,1732,36527,3459,360,17724,409,326,6,1741,5987,22555,951,24261,288,1880,951,917,2053,3700,34965,11,93084,1880,3057,65,811,57967,1220,294,26248,1088,1759,409,1208,6377,30052,9359,10333,5392,788,95188,4949,11,2126,22811,11,1008,44357,11,95995,409,3729,8471,1880,5790,325,625,3808,65381,10045,409,17317,24789,266,11,9131,11,11376,11,4046,6414,51084,951,97035,13,8245,22139,64829,29696,409,11692,1880,409,85182,77,685,328,5164,409,80080,423,944,59307,80080,11,17889,1354,5860,24985,3946,11,62163,409,5790,325,625,3808,951,35030,3557,1880,3930,586,13,51097,4972,35933,44564,20392,3869,326,58591,73511,7769,3136,13,3744,268,2850,1900,5856,288,9952,3625,447,2053,17317,58673,484,2439,5019,65827,268,404,1880,5201,261,3625,7617,288,409,77463,38450,12267,1880,1097,73511,15171,1208,9313,1880,1208,6225,31617,8082,951,1615,316,18543,1759,13,5856,288,8666,266,22589,1219,13109,8666,50848,294,6,4683,15916,11,1219,13109,8666,1413,3930,49904,265,11,43252,89781,288,1765,3625,13826,25108,4978,409,51304,13,29124,6414,51084,951,97222,1880,951,3600,45629,288,5019,38682,404,15907,22639,9952,3625,2027,38647,11,3625,1615,316,18543,1759,11,326,6,485,592,7379,1880,3625,46106,31957,1821,13,20915,21066,409,1208,26965,13109,44564,3057,1557,409,1208,26965,13109,38682,1001,12267,13,2998,2842,40280,1880,82620,27220,18042,283,35573,514,82620,27220,1880,326,91655,11323,266,2428,13,2998,29033,6672,51097,737,2727,392,645,432,1137,625,3808,1765,3625,737,2727,392,645,1880,46106,21744,10515,5512,409,326,6,1741,5987,13]
            }
            stored_item = crawler.store_chunk_item(cursor, item)
            self.connection.rollback()
        self.assertEqual(stored_item["url"], item["url"])

    def test_store_crawl_item(self):
        """Test storing a crawl item."""
        with db.cursor(self.connection) as cursor:
            item = {
                "url": "https://example.com",
                "title": "Example",
                "html_content": "<html><body>This is an example.</body></html>",
                "lang": "en",
                "last_crawled": "2022-01-01",
                "last_updated": "2022-01-01"
            }
            stored_item = crawler.store_crawl_item(cursor, item)
            self.connection.rollback()
        self.assertEqual(item["title"], stored_item["title"])
        self.assertEqual(item["url"], stored_item["url"])

    def test_store_embedding_item(self):
        """Test storing an embedding item."""
        with db.cursor(self.connection) as cursor:
            item = {
                "token_id": "be612259-9b52-42fd-8d0b-d72120efa3b6",
                "embedding": test.generate_random_embedding(1536),
                "embedding_model": "test-model"
            }
            stored_item = crawler.store_embedding_item(cursor, item)
            self.connection.rollback()
        self.assertEqual(item["token_id"], stored_item)

    def test_fetch_crawl_ids_without_chunk(self):
        """Test fetching crawl IDs without a chunk."""
        with db.cursor(self.connection) as cursor:
            id = crawler.fetch_crawl_ids_without_chunk(cursor)
            self.connection.rollback()
        self.assertEqual(id, [])

    def test_fetch_crawl_row(self):
        """Test fetching a crawl row."""
        with db.cursor(self.connection) as cursor:
            row = crawler.fetch_crawl_row(cursor, "https://inspection.canada.ca/a-propos-de-l-acia/structure-organisationnelle/mandat/fra/1299780188624/1319164463699")
            self.connection.rollback()
        self.assertEqual(row['title'], "Mandat - Agence canadienne d'inspection des aliments")

    # def test_fetch_crawl_row_with_test_data(self):
    #     """Test fetching a crawl row."""
    #     with db.cursor(self.connection) as cursor:
    #         test_chunk_id = test.test_uuid
    #         test_crawl_id = test.test_uuid
    #         test_md5hash = test.test_hash


    #         cursor.execute(f"""
    #         INSERT INTO html_content VALUES ('<html><body>Test Content</body></html>', '{test_md5hash}');
    #         INSERT INTO crawl (id, url, title, lang, last_crawled, last_updated, last_updated_date, md5hash)
    #         VALUES ('{test_chunk_id}', 'http://example.com', 'Test Title', 'en', NOW(), NOW(), NOW(), '{test_md5hash}');
    #         INSERT INTO html_content_to_chunk VALUES ('{test_crawl_id}', '{test_md5hash}');
    #         """
    #             )
    #         row = crawler.fetch_crawl_row(cursor, "http://example.com")
    #         self.connection.rollback()
    #     self.assertEqual(row['title'], "Test Title")
        
    def test_fetch_chunk_token_row(self):
        """Test fetching a chunk token row."""
        with db.cursor(self.connection) as cursor:
            row = crawler.fetch_chunk_token_row(cursor, "469812c5-190c-4e56-9f88-c8621592bcb5")
            self.connection.rollback()
        self.assertEqual(str(row['chunk_id']), "469812c5-190c-4e56-9f88-c8621592bcb5")

    def test_fetch_crawl_row_with_invalid_url(self):
        """Test fetching a crawl row with an invalid URL."""
        with db.cursor(self.connection) as cursor:
            with self.assertRaises(db.DBError):
                crawler.fetch_crawl_row(cursor, "invalid_url")
