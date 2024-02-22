import unittest
import json
import os
import sys
from unittest.mock import patch
import tempfile
import shutil

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bin.generate_qna import generate_question


class TestScript(unittest.TestCase):
    def setUp(self):
        self.prompt_path = "/ailab/db/finesse/prompt"

    @patch("bin.generate_qna.openai.get_chat_answer")
    @patch("bin.generate_qna.get_random_chunk")
    @patch("bin.generate_qna.db.connect_db")
    def test_generate_question(
        self, mock_connect_db, mock_get_random_chunk, mock_get_chat_answer
    ):
        system_prompt = "test system prompt"
        user_prompt = "test user prompt"
        json_template = "test json template"
        project_db = mock_connect_db.return_value

        mock_get_random_chunk.return_value = [
            {"title": "test title", "text_content": "test content"}
        ]

        class MockResponse:
            def __init__(self, choices):
                self.choices = choices

        class MockChoice:
            def __init__(self, message):
                self.message = message

        class MockMessage:
            def __init__(self, content):
                self.content = content

        mock_get_chat_answer.return_value = MockResponse(
            [MockChoice(MockMessage(json.dumps({"test_key": "test_value"})))]
        )

        # Create a temporary directory
        test_dir = tempfile.mkdtemp()

        try:
            self.assertIsNotNone(
                generate_question(system_prompt, user_prompt, json_template, project_db)
            )
            # Print the contents of the files
            # for filename in os.listdir(test_dir):
            #     with open(os.path.join(test_dir, filename), "r") as file:
            #         print(f"Contents of {filename}:")
            #         print(file.read())
        finally:
            # Remove the temporary directory after the test
            shutil.rmtree(test_dir)

    @patch("bin.generate_qna.openai.get_chat_answer")
    @patch("bin.generate_qna.get_random_chunk")
    @patch("bin.generate_qna.db.connect_db")
    def test_generate_question_db_connection_fail(
        self, mock_connect_db, mock_get_random_chunk, mock_get_chat_answer
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
