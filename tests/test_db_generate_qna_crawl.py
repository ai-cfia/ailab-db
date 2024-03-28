import os
import sys
import unittest
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
from datetime import date

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # noqa: E402
from bin.generate_qna_crawl import generate_question, NoChunkFoundError


class TestScript(unittest.TestCase):
    TEST_VERSION = date.today()

    def setUp(self):
        self.prompt_path = "/ailab/db/finesse/prompt"

    @patch("bin.generate_qna_crawl.openai.get_chat_answer")
    @patch("bin.generate_qna_crawl.get_random_crawl")
    @patch("bin.generate_qna_crawl.db.connect_db")
    def test_generate_question(
        self, mock_connect_db, mock_get_random_crawl, mock_get_chat_answer
    ):
        system_prompt = "test system prompt"
        user_prompt = "test user prompt"
        json_template = "test json template"
        project_db = mock_connect_db.return_value

        # Simuler un crawl aléatoire avec les clés nécessaires
        mock_get_random_crawl.return_value = [
            {
                "crawl_id": "123456",
                "crawl_url": "http://example.com",
                "title": "test title",
                "text_content": "test content",
                "html_content": "<html><body>This is HTML content</body></html>",
                "score_type": "test_score_type",
                "score": 10,
            }
        ]

        # Simuler une réponse JSON valide de openai.get_chat_answer
        mock_get_chat_answer.return_value.choices[0].message.content = json.dumps(
            {"test_key": "test_value"}
        )

        # Assurez-vous que la fonction generate_question retourne une valeur différente de None
        responses, average_character_length = generate_question(
            system_prompt, user_prompt, json_template, project_db
        )
        self.assertIsNotNone(responses)
        self.assertIsInstance(responses, list)
        self.assertIsInstance(average_character_length, float)

    @patch("bin.generate_qna_crawl.openai.get_chat_answer")
    @patch("bin.generate_qna_crawl.get_random_crawl")
    @patch("bin.generate_qna_crawl.db.connect_db")
    def test_generate_question_db_connection_fail(
        self, mock_connect_db, mock_get_random_crawl, mock_get_chat_answer
    ):
        system_prompt = "test system prompt"
        user_prompt = "test user prompt"
        json_template = "test json template"
        mock_connect_db.return_value = None  # Simulate a failed DB connection

        # Create a temporary directory
        test_dir = tempfile.mkdtemp()

        try:
            self.assertIsNone(
                generate_question(
                    system_prompt,
                    user_prompt,
                    json_template,
                    mock_connect_db.return_value,
                )
            )
        finally:
            # Remove the temporary directory after the test
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    unittest.main()
