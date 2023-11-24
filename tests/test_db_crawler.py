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

    def test_fetch_chunk_row(self):
        """sample test to check if fetch_chunk_row works"""
        url = db.create_postgresql_url(
            "DBNAME",
            "chunk",
            "469812c5-190c-4e56-9f88-c8621592bcb5")
        with db.cursor(self.connection) as cursor:
            row = crawler.fetch_chunk_token_row(cursor, url)
            self.connection.rollback()
        self.assertTrue(isinstance(row, dict))
        self.assertEqual(len(row['tokens']), 76)
        self.assertEqual(str(row['chunk_id']), "469812c5-190c-4e56-9f88-c8621592bcb5")
        self.assertEqual(str(row['token_id']), 'dbb7b498-2cbf-4ae9-aa10-3169cc72f285')

    def test_fetch_chunk_id_without_embedding(self):
        """sample test to check if fetch_chunk_id_without_embedding works"""
        with db.cursor(self.connection) as cursor:
            cursor.execute(test.embedding_table.format(embedding_model='test-model'))
            rows = crawler.fetch_chunk_id_without_embedding(cursor, 'test-model')
            _entity_id = rows[0]
            self.connection.rollback()
