"""test database functions"""
import unittest

import testing_utils as test
import louis.db as db


class TestDBSchema(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_schema(self):
        """sample test to check if the schema is correct and idempotent"""
        with open(f"dumps/{test.LOUIS_SCHEMA}/schema.sql", encoding='utf-8') as schema_file:
            schema = schema_file.read()
            schema = schema.replace(test.LOUIS_SCHEMA, 'test')
        with db.cursor(self.connection) as cursor:
            cursor.execute(schema)
            self.connection.rollback()