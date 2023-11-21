import os
import sys
import json

import ailab.db as db
import ailab.db.finesse as finesse
from ailab.models import openai
from ailab.db.finesse.test_queries import get_random_chunk

def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " PROMPT_PATH")
        print("PROMPT_PATH: Directory containing the API prompt")
        sys.exit(1)

    prompt_path = sys.argv[1]

    if not os.path.exists(prompt_path):
        print(f"The directory '{prompt_path}' does not exist.")
        sys.exit(1)

    project_db = db.connect_db()

    system_prompt = finesse.load_prompt(prompt_path, "qna_system_prompt.txt")
    user_prompt = finesse.load_prompt(prompt_path, "qna_user_prompt.txt")
    json_template = finesse.load_json_template(prompt_path)

    print("\nSystem Prompt:", system_prompt)
    print("\nUser Prompt:", user_prompt)
    print("\n")

    # Fetch a random chunk from the database
    with project_db.cursor() as cursor:
        random_chunk = get_random_chunk(cursor)
        print("Random Chunk:", random_chunk)

    # Ensure random_chunk is converted to a string
    if random_chunk is not None:
        random_chunk_str = str(random_chunk)
    else:
        print("Random Chunk is NONE")
        # Handle the absence of random chunk appropriately

    # Construct the user prompt
    if random_chunk_str:
        user_prompt += (
            f"\n\nHere is the JSON containing the search:\n{random_chunk_str}"
            f"\n\nAnd here is the JSON template:\n{json_template}"
        )

        # Proceed with the API call
        response = openai.get_chat_answer(system_prompt, user_prompt, 2000)
        print("\nResponse from OpenAI:")
        print(response.choices[0].message.content)
        print("\n\n")

        # Assuming response is the API response received
        # response_content = response.choices[0].message.content

        # Parse the JSON string into a Python dictionary
        # generated_data = json.loads(response_content)

if __name__ == "__main__":
    main()
