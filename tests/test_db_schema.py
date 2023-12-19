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
        """Test if crawl table exists in the database and is not empty."""
        table_name = "crawl" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_crawl_has_correct_columns(self):
        """Test if crawl table has the correct columns."""
        table_name = "crawl"  
        expected_columns = ["id", "url", "title", "lang", "last_crawled", 
                            "last_updated", "last_updated_date", "md5hash"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertCountEqual(actual_columns, expected_columns)
    
    def test_chunk_exists(self):
        """Test if chunk table exists in the database and is not empty."""
        table_name = "chunk" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_chunk_has_correct_columns(self):
        """Test if chunk table has the correct columns."""
        table_name = "chunk"  
        expected_columns = ["id", "title", "text_content"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertEqual(actual_columns, expected_columns)
    
    def test_token_exists(self):
        """Test if token table exists in the database and is not empty."""
        table_name = "token" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_token_has_correct_columns(self):
        """Test if token table has the correct columns."""
        table_name = "token"  
        expected_columns = ["id", "chunk_id", "tokens", "encoding"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertEqual(actual_columns, expected_columns)

    def test_score_exists(self):
        """Test if score table exists in the database and is not empty."""
        table_name = "score" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_score_has_correct_columns(self):
        """Test if score table has the correct columns."""
        table_name = "score"  
        expected_columns = ["entity_id", "score", "score_type"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertEqual(actual_columns, expected_columns)
    
    def test_html_content_exists(self):
        """Test if html_content table exists in the database and is not empty."""
        table_name = "html_content" 
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
    
    def test_html_content_has_correct_columns(self):
        """Test if html_content table has the correct columns."""
        table_name = "html_content"  
        expected_columns = ["content", "md5hash"]  
        with db.cursor(self.connection) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name} LIMIT 0;""")
            actual_columns = [desc[0] for desc in cursor.description]
            self.assertEqual(actual_columns, expected_columns)

    def test_false_table_not_exists(self):
        """Test if false_table table does NOT exists in the database."""
        table_name = "false_table" 
        with db.cursor(self.connection) as cursor:
            with self.assertRaises(psycopg.errors.UndefinedTable):
                cursor.execute(f"""SELECT * FROM {table_name} LIMIT 1;""")

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
