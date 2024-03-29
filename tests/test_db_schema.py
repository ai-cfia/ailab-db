"""test database functions"""
import unittest

import ailab.db as db


class TestDBSchema(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    # def test_schema(self):
    #     """sample test to check if the schema is correct and idempotent"""
    #     schema_filename = f"dumps/{test.LOUIS_SCHEMA}/schema.sql"
    #     with open(schema_filename, encoding='utf-8') as schema_file:
    #         schema = schema_file.read()
    #         schema = schema.replace(test.LOUIS_SCHEMA, 'test')
    #     with db.cursor(self.connection) as cursor:
    #         cursor.execute(schema)
    #         self.connection.rollback()
