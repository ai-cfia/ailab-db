import unittest
import json
import sys
from unittest.mock import patch

from bin.search_function_test_utilizing_llm import (
    load_prompts_and_template,
    construct_user_prompt,
    generate_question,
    save_response_to_file,
)

# Assuming the test script is located in the same directory as the project root
# This adds the current directory to the path
sys.path.append("..")


class TestScript(unittest.TestCase):
    def setUp(self):
        self.prompt_path = "/ailab/db/finesse/prompt"

    @patch("bin.search_function_test_utilizing_llm.finesse")
    def test_load_prompts_and_template(self, mock_finesse):
        mock_finesse.load_prompt.return_value = "test prompt"
        mock_finesse.load_json_template.return_value = "test template"

        system_prompt, user_prompt, json_template = load_prompts_and_template(
            self.prompt_path
        )

        self.assertEqual(system_prompt, "test prompt")
        self.assertEqual(user_prompt, "test prompt")
        self.assertEqual(json_template, "test template")

    def test_construct_user_prompt(self):
        user_prompt = "test prompt"
        random_chunk_str = "test chunk"
        json_template = "test template"

        expected_output = f"{user_prompt}\n\nHere is the JSON containing the search:\n{random_chunk_str}\n\nAnd here is the JSON template:\n{json_template}"

        self.assertEqual(
            construct_user_prompt(user_prompt, random_chunk_str, json_template),
            expected_output,
        )

    @patch("bin.search_function_test_utilizing_llm.db")
    @patch("ailab.models.openai")
    @patch("ailab.db.finesse.test_queries.get_random_chunk")
    def test_generate_question(self, mock_get_random_chunk, mock_openai, mock_db):
        system_prompt = "test system prompt"
        user_prompt = "test user prompt"
        json_template = "test json template"
        project_db = mock_db.connect_db.return_value

        mock_get_random_chunk.return_value = [
            {"title": "test title", "text_content": "test content"}
        ]
        mock_openai.get_chat_answer.return_value = mock_openai.get_chat_answer.choices[
            0
        ].message.content.return_value = json.dumps({"test_key": "test_value"})

        self.assertIsNotNone(
            generate_question(system_prompt, user_prompt, json_template, project_db)
        )

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_response_to_file(self, mock_open):
        data = {"test_key": "test_value"}

        save_response_to_file(data)

        mock_open.assert_called_once_with(unittest.mock.ANY, "w")
        file_handle = mock_open.return_value
        file_handle.write.assert_called_once_with(
            json.dumps(data, ensure_ascii=False, indent=4)
        )


if __name__ == "__main__":
    unittest.main()
