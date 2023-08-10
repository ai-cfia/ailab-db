import unittest

import psycopg
from psycopg.rows import dict_row

import testing_utils as test

class TestDBData(unittest.TestCase):

    def execute(self, filename):
        query = open(filename).read()
        self.cursor.execute(query)

    def setUp(self):
        self.connection = psycopg.connect(test.LOUIS_DSN)
        self.cursor = self.connection.cursor(row_factory=dict_row)
        self.cursor.execute("SET search_path TO louis_v004, public")

    def tearDown(self):
        self.connection.rollback()
        self.cursor.close()
        self.connection.close()

    def upgrade_schema(self):
        return
        if test.LOUIS_SCHEMA == 'louis_v004':
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
            FROM html_content
            WHERE NOT xml_is_well_formed(content);""")
        result = self.cursor.fetchall()
        self.assertEqual(result[0]['count'], 0, "All xml should be well formed")

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
