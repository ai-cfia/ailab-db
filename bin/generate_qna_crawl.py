"""
Script Purpose: This script generates questions based on provided prompts and
stores the responses as JSON files. It interacts with the AI model to create
questions and saves the relevant data for each question in a JSON file.

Usage: ./generate_qna_crawl.sh PROMPT_PATH

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

from ailab.db.finesse.test_queries import get_random_crawl

# Constants
TEST_VERSION = date.today()
REQUIRED_QUESTIONS = 10
CHARACTER_LIMIT = 14383
MAX_TOKEN = 2000
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
    json_template = finesse.load_json_template("json_template_crawl", prompt_path)

    return system_prompt, user_prompt, json_template


def construct_user_prompt(user_prompt, random_chunk_str, json_template):
    """Constructs the user prompt using prompt, chunk and json template"""
    return (
        f"{user_prompt}\n\nHere is the JSON containing the search:\n{random_chunk_str}"
        f"\n\nAnd here is the JSON template:\n{json_template}"
    )


class NoChunkFoundError(Exception):
    pass


def generate_question(system_prompt, user_prompt, json_template, project_db):
    """Generates a question and saves it to a file"""
    if project_db is None:
        print("Database connection failed.")
        return None

    average_character_length = 0

    with project_db.cursor() as cursor:
        responses = []  # create an empty list to hold the responses
        compteur = 0

        while compteur < REQUIRED_QUESTIONS:
            schema_version = "louis_v005"

            print("----------" + str(compteur) + "------------")
            random_crawls = get_random_crawl(cursor, schema_version)
            if not random_crawls:
                raise NoChunkFoundError("No chunk found in the database.")

            # Get the first element
            first_chunk = random_crawls[0]
            crawl_id = str(
                first_chunk["crawl_id"]
            )  # Convertir l'UUID en chaîne de caractères
            crawl_url = first_chunk["crawl_url"]
            html_content = first_chunk["html_content"]

            # Get the score
            crawl_string = "crawl_id: " + crawl_id + "; crawl_url: " + crawl_url
            for crawl in random_crawls:
                crawl_string += "; " + crawl["score_type"] + ": "
                crawl_string += str(
                    crawl["score"]
                )  # Assurez-vous que le score est également une chaîne de caractères
            crawl_string += "; html_content: " + html_content

            constructed_user_prompt = construct_user_prompt(
                user_prompt, crawl_string, json_template
            )
            total_length = len(system_prompt) + len(constructed_user_prompt)

            if total_length < CHARACTER_LIMIT:
                average_character_length += total_length
                response = openai.get_chat_answer(
                    system_prompt, constructed_user_prompt, MAX_TOKEN
                )
                data = json.loads(response.choices[0].message.content)
                if isinstance(data, dict):
                    compteur += 1
                    responses.append(data)  # add the data to the responses list

    return responses, average_character_length / REQUIRED_QUESTIONS


def save_response_to_file(data, STORAGE_PATH):
    """Saves the provided data to a new file"""
    file_number = 1
    while True:
        file_name = f"qna_{TEST_VERSION}_{file_number}.json"
        file_path = os.path.join(STORAGE_PATH, file_name)

        # Check if the directory exists, if not, create it
        if not os.path.exists(STORAGE_PATH):
            os.makedirs(STORAGE_PATH)

        # Check if the file exists, if not, create it
        if not os.path.exists(file_path):
            with open(file_path, "w") as json_file:
                print("New file created at: " + file_path)
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            break

        file_number += 1

    if file_number == 1:
        print("File saved into: " + file_path)
    else:
        print("File appended into: " + file_path)


class DirectoryNotFoundError(Exception):
    pass


class NoQuestionsGeneratedError(Exception):
    pass


def main(prompt_path, storage_path):
    if not os.path.exists(prompt_path):
        raise DirectoryNotFoundError(f"The directory '{prompt_path}' does not exist.")

    system_prompt, user_prompt, json_template = load_prompts_and_template(prompt_path)
    project_db = db.connect_db()

    # Call generate_question function
    responses, average_tokens_per_chunk = generate_question(
        system_prompt, user_prompt, json_template, project_db
    )

    # If no questions were generated, raise an error
    if average_tokens_per_chunk is None:
        raise NoQuestionsGeneratedError("No questions were generated.")

    # Save each response to a file
    for response in responses:
        save_response_to_file(response, storage_path)

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
