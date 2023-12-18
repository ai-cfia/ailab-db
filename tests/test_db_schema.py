"""test database functions"""
import unittest

import psycopg

import ailab.db as db


class TestDBSchema(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_crawl_exists(self):
        """Test if a specific table exists in the database."""
        table_name = "crawl" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name};""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_false_table_not_exists(self):
        """Test if a specific table does not exists in the database."""
        table_name = "false_table" 
        with db.cursor(self.connection) as cursor:
            with self.assertRaises(psycopg.errors.UndefinedTable):
                cursor.execute(f"""SELECT * FROM {table_name};""")

    def test_table_has_correct_columns(self):
        """Test if a specific table has the correct columns."""
        table_name = "chunk"  
        expected_columns = ["id", "title", "text_content"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertCountEqual(actual_columns, expected_columns, f"Table {table_name} does not have the correct columns.")

    # def test_schema(self):
    #     """sample test to check if the schema is correct and idempotent"""
    #     schema_filename = f"dumps/{test.LOUIS_SCHEMA}/schema.sql"
    #     with open(schema_filename, encoding='utf-8') as schema_file:
    #         schema = schema_file.read()
    #         schema = schema.replace(test.LOUIS_SCHEMA, 'test')
    #     with db.cursor(self.connection) as cursor:
    #         cursor.execute(schema)
    #         self.connection.rollback()

    # def test_schema_exist(self):
    #     """sample test to check if the schema exists"""
    #     with db.cursor(self.connection) as cursor:
    #         cursor.execute(
    #             "SELECT EXISTS(SELECT * FROM )",
    #             (test.LOUIS_SCHEMA,)
    #             )
    #         self.connection.rollback()
    #         row = cursor.fetchone()
    #     self.assertTrue(row[0])
