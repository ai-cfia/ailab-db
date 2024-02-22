"""
Script Purpose: This script generates questions based on provided prompts and
stores the responses as JSON files. It interacts with the AI model to create
questions and saves the relevant data for each question in a JSON file.

Usage: ./generate-qna.sh PROMPT_PATH

Parameters: - PROMPT_PATH: Directory containing the API prompt files
(qna_system_prompt.txt, qna_user_prompt.txt, and JSON template)
"""

import os
import json
from datetime import date
import argparse

import ailab.db as db
from ailab.models import openai
import ailab.db.finesse as finesse

from ailab.db.finesse.test_queries import get_random_chunk

# Constants
TEST_VERSION = date.today()
REQUIRED_QUESTIONS = 3
CHARACTER_LIMIT = 14383
DEFAULT_STORAGE_PATH = "../qna-test"
SYSTEM_PROMPT_FILENAME = "qna_system_prompt.txt"
USER_PROMPT_FILENAME = "qna_user_prompt.txt"


def load_prompts_and_template(
    prompt_path,
    system_prompt_filename=SYSTEM_PROMPT_FILENAME,
    user_prompt_filename=USER_PROMPT_FILENAME,
):
    """Loads prompts and template from provided path"""
    system_prompt = finesse.load_prompt(prompt_path, system_prompt_filename)
    user_prompt = finesse.load_prompt(prompt_path, user_prompt_filename)
    json_template = finesse.load_json_template(prompt_path)

    return system_prompt, user_prompt, json_template


def construct_user_prompt(user_prompt, random_chunk_str, json_template):
    """Constructs the user prompt using prompt, chunk and json template"""
    return (
        f"{user_prompt}\n\nHere is the JSON containing the search:\n{random_chunk_str}"
        f"\n\nAnd here is the JSON template:\n{json_template}"
    )

class NoChunkFoundError(Exception):
    pass

def generate_question(
    system_prompt, user_prompt, json_template, project_db, STORAGE_PATH
):
    """Generates a question and saves it to a file"""
    if project_db is None:
        print("Database connection failed.")
        return None

    average_character_length = 0

    with project_db.cursor() as cursor:
        for i in range(REQUIRED_QUESTIONS):
            # Access the AILAB_SCHEMA_VERSION environment variable
            schema_version = os.getenv("AILAB_SCHEMA_VERSION")

            random_chunk = get_random_chunk(cursor, schema_version)
            if not random_chunk:
                raise NoChunkFoundError("No chunk found in the database.")

            chunk_title = ""
            for chunk in random_chunk:
                chunk_title = chunk["title"]

            ### TO REMOVE ###
            words_to_check = [
                "This page is part",
                "Cette page fait partie",
                "Archivée",
                "archivée",
                "Archived",
                "archived",
            ]

            found_words = []

            for word in words_to_check:
                if word.lower() in chunk_title.lower():
                    found_words.append(word)

            if found_words:
                print("The following words were found in the string:")
                for found_word in found_words:
                    print("-", found_word)
                print("Skipping...")
            else:
                ### TO REMOVE ###

                constructed_user_prompt = construct_user_prompt(
                    user_prompt, str(random_chunk), json_template
                )
                total_length = len(system_prompt) + len(constructed_user_prompt)

                if total_length < CHARACTER_LIMIT:
                    average_character_length += total_length
                    response = openai.get_chat_answer(
                        system_prompt, constructed_user_prompt, 2000
                    )
                    data = json.loads(response.choices[0].message.content)
                    if isinstance(data, dict):
                        for chunk in random_chunk:
                            data["text_content"] = chunk["text_content"]
                        save_response_to_file(data, STORAGE_PATH)

    return average_character_length / REQUIRED_QUESTIONS


def save_response_to_file(data, STORAGE_PATH):
    """Saves the provided data to a new file"""
    file_number = 1
    while True:
        file_name = f"qna_{TEST_VERSION}_{file_number}.json"
        file_path = os.path.join(STORAGE_PATH, file_name)
        if not os.path.exists(file_path):
            break
        file_number += 1

    with open(file_path, "w") as json_file:
        print("File saved into: " + file_path)
        json.dump(data, json_file, ensure_ascii=False, indent=4)


class DirectoryNotFoundError(Exception):
    pass


class NoQuestionsGeneratedError(Exception):
    pass


def main(prompt_path, storage_path):
    if not os.path.exists(prompt_path):
        raise DirectoryNotFoundError(f"The directory '{prompt_path}' does not exist.")

    system_prompt, user_prompt, json_template = load_prompts_and_template(prompt_path)
    project_db = db.connect_db()

    average_tokens_per_chunk = generate_question(
        system_prompt, user_prompt, json_template, project_db, storage_path
    )

    if average_tokens_per_chunk is None:
        raise NoQuestionsGeneratedError("No questions were generated.")

    print("Average Tokens sent to the API: " + str(average_tokens_per_chunk))


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate questions based on prompts.")
    parser.add_argument("prompt_path", help="Directory containing the API prompt")
    parser.add_argument(
        "--storage_path", default=DEFAULT_STORAGE_PATH, help="Path to storage"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.prompt_path, args.storage_path)
