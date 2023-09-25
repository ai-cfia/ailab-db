"""test database functions"""
import unittest
import json

import louis.db as db
import louis.db.api as api

import testing_utils as test


class TestDBAPI(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()
        self.cursor = db.cursor(self.connection)

    def tearDown(self):
        self.connection.rollback()
        self.connection.close()

    def test_match_documents_text_query(self):
        with db.cursor(self.connection) as cursor:
            docs = api.match_documents_from_text_query(
                cursor,
                'what are the cooking temperatures for e.coli?')
            self.connection.rollback()
        self.assertEqual(len(docs), 10)

    # obsoleted by weighted search
    # def test_president_of_cfia(self):
    #     with db.cursor(self.connection) as cursor:
    #         docs = api.match_documents_from_text_query(
    #             cursor, 'who is the president of the CFIA?')
    #         self.connection.rollback()
    #     self.assertEqual(
    #         docs[0]['title'],
    #         'Dr. Harpreet S. Kochhar - Canadian Food Inspection Agency')

    def test_weighted_search(self):
        with open('tests/embeddings/president.json') as f:
            embeddings = json.load(f)
        query = 'who is the president of the CFIA?'
        weights = json.dumps(
            {'similarity': 0.6, 'recency': 0.2, 'traffic': 0.0, 'current': 0.1})
        self.cursor.execute(
            "SELECT * FROM search(%s, %s::vector, %s::float, %s::integer, %s::jsonb)", (
                query, embeddings, test.MATCH_THRESHOLD, test.MATCH_COUNT, weights))
        results = self.cursor.fetchall()
        result = results[0]['search']
        self.assertEqual(
            result[0]['title'],
            "Dr. Harpreet S. Kochhar - Canadian Food Inspection Agency")

        query_id = result[0]['query_id']
        self.cursor.execute("SELECT * FROM query where id = %s::uuid", (query_id,))
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['query'], query)
        result_embedding = result[0]['embedding']
        self.assertAlmostEqual(result_embedding[0], embeddings[0])
        self.assertEqual(len(result[0]['result']), test.MATCH_COUNT)

    def test_weighted_search_with_empty_query(self):
        weights = json.dumps({ 'recency': 0.4, 'traffic': 0.4, 'current': 0.2})
        self.cursor.execute(
            "SELECT * FROM search(%s, %s::vector, %s::float, %s::integer, %s::jsonb)", (
                None, None, test.MATCH_THRESHOLD, test.MATCH_COUNT, weights))
        result = self.cursor.fetchall()[0]['search']
        self.assertEqual(len(result), test.MATCH_COUNT, "Should return 10 results")
        urls = dict([(r['url'], True) for r in result])
        self.assertEqual(
            len(urls.keys()),
            test.MATCH_COUNT,
            "All urls should be unique")