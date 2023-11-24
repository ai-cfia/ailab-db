"""test database functions"""
import unittest
import ailab.db as db
import tests.testing_utils as test 

class TestDBUtils(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_create_postgresql_url(self):
        """sample test to check if create_parse_postgresql_url works"""
        entity_uuid = '5cef886d-8408-4868-9a69-0f0ca2167941'
        url = db.create_postgresql_url(
            "inspection.canada.ca",
            "chunk", entity_uuid,
            {'encoding': 'cl100k_base'})
        self.assertEqual(url, f"postgresql://inspection.canada.ca/{test.LOUIS_SCHEMA}/chunk/{entity_uuid}?encoding=cl100k_base")
        parsed = db.parse_postgresql_url(url)
        self.assertEqual(parsed['dbname'], "inspection.canada.ca")
        self.assertEqual(parsed['tablename'], "chunk")
        self.assertEqual(parsed['id'], entity_uuid)
        self.assertEqual(parsed['parameters']['encoding'][0], "cl100k_base")
