import os
import sys
import json
from datetime import date

import ailab.db as db
from ailab.models import openai
import ailab.db.finesse as finesse

from ailab.db.finesse.test_queries import get_random_chunk

TEST_VERSION = date.today()
WANTED_GENERATED_QUESTIONS = 5
CHARACTER_LIMIT = 14383


def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " PROMPT_PATH")
        print("PROMPT_PATH: Directory containing the API prompt")
        sys.exit(1)
    prompt_path = sys.argv[1]
    if not os.path.exists(prompt_path):
        print(f"The directory '{prompt_path}' does not exist.")
        sys.exit(1)

    system_prompt = finesse.load_prompt(prompt_path, "qna_system_prompt.txt")
    user_prompt = finesse.load_prompt(prompt_path, "qna_user_prompt.txt")
    json_template = finesse.load_json_template(prompt_path)

    project_db = db.connect_db()


    AVERAGE_TOKENS_BY_CHUNK = 0

    
    for i in range(WANTED_GENERATED_QUESTIONS):
        random_chunk = ""

        # Fetch a random chunk from the database
        with project_db.cursor() as cursor:
            random_chunk = get_random_chunk(cursor)

        random_chunk_str = ""
        if random_chunk is not None:
            random_chunk_str = str(random_chunk)
        else:
            print("Random Chunk is NONE")
            # Handle the absence of random chunk appropriately

        if random_chunk_str:
            constructed_user_prompt = ""
            constructed_user_prompt += user_prompt
            constructed_user_prompt += (
                f"\n\nHere is the JSON containing the search:\n{random_chunk_str}"
                f"\n\nAnd here is the JSON template:\n{json_template}"
            )

            total_length = len(system_prompt) + len(constructed_user_prompt)
            AVERAGE_TOKENS_BY_CHUNK += total_length
            if total_length < CHARACTER_LIMIT:
                response = openai.get_chat_answer(
                    system_prompt, constructed_user_prompt, 2000
                )
                print("\nResponse from OpenAI:")
                print(response.choices[0].message.content)
                print("\n\n")

                data = json.loads(response.choices[0].message.content)
                storage_path = "/home/vscode/finesse-data-2/qna"
                if isinstance(data, dict):
                    file_number = 1
                    while True:
                        file_name = f"qna_{TEST_VERSION}_{file_number}.json"
                        file_path = os.path.join(storage_path, file_name)
                        if not os.path.exists(file_path):
                            break
                        file_number += 1
                    for chunk in random_chunk:
                        data["text_content"] = chunk["text_content"]

                    file_path = os.path.join(storage_path, file_name)
                    with open(file_path, "w") as json_file:
                        print("File saved into: " + file_path)
                        json.dump(data, json_file, ensure_ascii=False, indent=4)

    AVERAGE_TOKENS_BY_CHUNK = AVERAGE_TOKENS_BY_CHUNK / WANTED_GENERATED_QUESTIONS
    print("Average Tokens send to the API : " + str(AVERAGE_TOKENS_BY_CHUNK))



if __name__ == "__main__":
    main()
