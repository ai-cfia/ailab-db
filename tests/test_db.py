import dotenv
dotenv.load_dotenv()

import os
import unittest
import psycopg
import json
from psycopg.rows import dict_row


LOUIS_DSN = os.getenv("LOUIS_DSN")
MATCH_THRESHOLD = 0.5
MATCH_COUNT = 10

class DBTest(unittest.TestCase):

    def execute(self, filename):
        query = open('sql/2023-07-19-weighted_search.sql').read()
        self.cursor.execute(query)

    def setUp(self):
        self.connection = psycopg.connect(LOUIS_DSN)
        self.cursor = self.connection.cursor(row_factory=dict_row)
        self.cursor.execute("SET search_path TO louis_v004, public")

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def test_weighted_search(self):
        self.execute('sql/2023-07-19-modified-documents.sql')
        self.execute('sql/2023-07-19-weighted_search.sql')
        
        embeddings = json.load(open('tests/embeddings/president.json'))

        weights = json.dumps({ 'similarity': 0.6, 'recency': 0.2, 'traffic': 0.0, 'current': 0.1})
        self.cursor.execute("SELECT * FROM search(%s::vector, %s::float, %s::integer, %s::jsonb)", (
            embeddings, MATCH_THRESHOLD, MATCH_COUNT, weights))
        result = self.cursor.fetchall()
        # self.assertEqual(len(result), MATCH_COUNT)
        # print([(r['title'], r['subtitle'], r['url'], r['last_updated'], r['score'], r['scores'])for r in result])
        self.assertEqual(result[0]['title'], "Dr. Harpreet S. Kochhar - Canadian Food Inspection Agency")

