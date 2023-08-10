import os
import unittest

import psycopg
import json
from psycopg.rows import dict_row

import dotenv
dotenv.load_dotenv()

def raise_error(message):
    raise Exception(message)

LOUIS_DSN = os.getenv("LOUIS_DSN") or raise_error("LOUIS_DSN is not set")
LOUIS_SCHEMA = os.getenv("LOUIS_SCHEMA") or raise_error("LOUIS_SCHEMA is not set")
MATCH_THRESHOLD = 0.5
MATCH_COUNT = 10

class DBTest(unittest.TestCase):

    def execute(self, filename):
        query = open(filename).read()
        self.cursor.execute(query)

    def setUp(self):
        self.connection = psycopg.connect(LOUIS_DSN)
        self.cursor = self.connection.cursor(row_factory=dict_row)
        self.cursor.execute("SET search_path TO louis_v004, public")

    def tearDown(self):
        self.connection.rollback()
        self.cursor.close()
        self.connection.close()

    def upgrade_schema(self):
        return
        if LOUIS_SCHEMA == 'louis_v004':
            self.execute('sql/2023-07-11-hotfix-xml-not-well-formed.sql')
            self.execute('sql/2023-07-11-populate-link.sql')
            self.execute('sql/2023-07-12-score-current.sql')
            self.execute('sql/2023-07-19-modify-score_type-add-similarity.sql')
            self.execute('sql/2023-07-19-modified-documents.sql')
            self.execute('sql/2023-07-19-weighted_search.sql')
            self.execute('sql/2023-07-21-default_chunk.sql')

    def test_well_formed_xml(self):
        self.upgrade_schema()
        # SELECT count(*) FROM crawl WHERE NOT xml_is_well_formed(html_content);
        self.cursor.execute("""
            SELECT count(*)
            FROM crawl
            WHERE NOT xml_is_well_formed(html_content);""")
        result = self.cursor.fetchall()
        self.assertEqual(result[0]['count'], 0, "All xml should be well formed")

    def test_weighted_search(self):
        self.upgrade_schema()

        with open('tests/embeddings/president.json') as f:
            embeddings = json.load(f)
        query = 'who is the president of the CFIA?'
        weights = json.dumps(
            {'similarity': 0.6, 'recency': 0.2, 'traffic': 0.0, 'current': 0.1})
        self.cursor.execute(
            "SELECT * FROM search(%s, %s::vector, %s::float, %s::integer, %s::jsonb)", (
                query, embeddings, MATCH_THRESHOLD, MATCH_COUNT, weights))
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
        result_embedding = json.loads(result[0]['embedding'])
        self.assertAlmostEqual(result_embedding[0], embeddings[0])
        self.assertEqual(len(result[0]['result']), MATCH_COUNT)

    def test_weighted_search_with_empty_query(self):
        self.upgrade_schema()

        weights = json.dumps({ 'recency': 0.4, 'traffic': 0.4, 'current': 0.2})
        self.cursor.execute(
            "SELECT * FROM search(%s, %s::vector, %s::float, %s::integer, %s::jsonb)", (
                None, None, MATCH_THRESHOLD, MATCH_COUNT, weights))
        result = self.cursor.fetchall()[0]['search']
        self.assertEqual(len(result), MATCH_COUNT, "Should return 10 results")
        urls = dict([(r['url'], True) for r in result])
        self.assertEqual(len(urls.keys()), MATCH_COUNT, "All urls should be unique")


    @unittest.skip("issue #8: we have to re-chunk the documents using louis-crawler first")
    def test_every_crawl_doc_should_have_at_least_one_chunk(self):
        self.execute('sql/2023-08-09-html_content-table.sql')
        self.cursor.execute("""
            select count(*)
                from crawl left join documents on crawl.id = documents.id
                where documents.id is null""")
        result = self.cursor.fetchall()
        self.assertEqual(
            result[0]['count'], 0,
            "Every crawl doc should have at least one chunk")
