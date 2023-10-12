import os
import json

import ailab.db as db
import ailab.db.nachet as nachet
from ailab.models import openai

root_path = os.path.abspath(os.sep)
seed_data_path = "/workspaces/louis-db-1/seed-data"
prompt_path = "/workspaces/louis-db-1/nachet-data/prompt"
wanted_files_number = 1
seed_list = []

database = db.connect_db()
cursor = db.cursor(database)

### Get a list of all the seeds
query = f"""
    SELECT
        REGEXP_REPLACE(UNNEST(REGEXP_MATCHES
        (content, '<i lang="la">(.*?)</i>', 'g')),'<[^>]+>','','g') AS seed_name
    FROM
        html_content
    WHERE md5hash = '1a365c39a8afd80d438ddf1bd3c9afed'
    LIMIT {wanted_files_number};
"""
cursor.execute(query)
list_seeds_scientific_name = cursor.fetchall()

for rows in list_seeds_scientific_name:
    seed_list.append(rows['seed_name'])

print("\nList of selected seeds :")
for seed in seed_list:
    print(seed)

def seed_identification_api(system_prompt, user_prompt, json_template):
    """
    Process seed data using Azure OpenAI endpoint and save results as JSON files.

    Args:
        system_prompt (str): A system prompt for the OpenAI conversation.
        user_prompt (str): A user prompt for the OpenAI conversation.
        json_template (json): A JSON template for the OpenAI request.

    This function performs the following steps:
    1. Iterates through a list of seed values.
    2. Checks if a JSON file for each seed exists and skips if it does.
    3. Constructs an SQL query to retrieve data related to the seed from a database.
    4. Sends the query to the database and fetches the retrieved data.
    5. Concatenates the cleaned content into a single 'page.'
    6. Sends a request to the Azure OpenAI endpoint to get a response.
    7. Processes the response, extracting the scientific name and saving it as a JSON file.
    """
    for seed in seed_list:
        print("\nCurrent seed : " + seed)
        seed_json_path = seed + ".json"

        if nachet.json_file_exists(seed_data_path, seed_json_path):
            print(f"The JSON file {seed_json_path} exists in {seed_data_path}, skipping")
        else:
            query = """
                SELECT
                    REGEXP_REPLACE(content, '<[^>]+>', '', 'g') AS cleaned_content
                FROM
                    html_content
                WHERE content
                    LIKE'%<h1 id="wb-cont" property="name">%<i lang="la">""" + seed + """</i>%</h1>%';
            """
            cursor.execute(query)
            web_pages_fr_en = cursor.fetchall()
            
            all_language_seed_page = ""
            for row in web_pages_fr_en:
                web_text = row.get('cleaned_content')
                all_language_seed_page += web_text
            page = all_language_seed_page

            print("Sending request for summary to Azure OpenAI endpoint...\n")
            response = openai.get_chat_answer(system_prompt, user_prompt, json_template, page)

            # print("Chat answer: \n" + response.choices[0].message.content + "\n")
            data = json.loads(response.choices[0].message.content)

            if isinstance(data, dict):
                filename_key = "scientific_name"
                file_name = data.get(filename_key, "no_data.json")
                file_name = nachet.decode_french_text(file_name)
                file_name += ".json"

                file_path = os.path.join(seed_data_path, file_name)
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, ensure_ascii=False)
                    
                print(f"JSON data written to {file_path}")

if __name__ == '__main__':
    system_prompt = nachet.load_prompt("system_prompt.txt", prompt_path)
    user_prompt = nachet.load_prompt("user_prompt.txt", prompt_path)
    json_template = nachet.load_json_template(prompt_path)

    seed_identification_api(system_prompt, user_prompt, json_template)

    cursor.close()
    database.close()