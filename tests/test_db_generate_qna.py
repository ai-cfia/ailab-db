import unittest
import json
import sys
from unittest.mock import patch

from bin.generate_qna import generate_question


# Assuming the test script is located in the same directory as the project root
# This adds the current directory to the path
sys.path.append("..")

class TestScript(unittest.TestCase):
    def setUp(self):
        self.prompt_path = "/ailab/db/finesse/prompt"

    @patch("bin.generate_qna.db")
    @patch("ailab.models.openai")
    @patch("ailab.db.finesse.test_queries.get_random_chunk")
    @patch("bin.generate-qna.openai.ChatCompletion.create")
    def test_generate_question(self, mock_openai_chat_completion, mock_get_random_chunk, mock_openai, mock_db):
        system_prompt = "test system prompt"
        user_prompt = "test user prompt"
        json_template = "test json template"
        project_db = mock_db.connect_db.return_value

        mock_get_random_chunk.return_value = [
            {"title": "test title", "text_content": "test content"}
        ]

        # Mocking the behavior of ChatGPT response
        mock_openai_chat_completion.return_value = {
            'choices': [{'message': {'content': 'mocked_response'}}]
        }

        mock_openai.get_chat_answer.return_value = json.dumps({"test_key": "test_value"})

        self.assertIsNotNone(
            generate_question(system_prompt, user_prompt, json_template, project_db)
        )

if __name__ == "__main__":
    unittest.main()
