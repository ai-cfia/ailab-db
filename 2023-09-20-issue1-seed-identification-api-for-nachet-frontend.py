import os
import json

import ailab.db as db
import ailab.db.nachet as nachet
from ailab.models import openai

root_path = os.getcwd()
seed_data_path = root_path + "/seed-data"
prompt_path = root_path + "/nachet-data/prompt"
wanted_files_number = 1
url_to_seed_mapping = {}

database = db.connect_db()
cursor = db.cursor(database)

### Get a list of all seeds URL
query = """
    SELECT DISTINCT
        (regexp_matches(filtered_content,
        'href="([^"]*seeds-identification[^"]*)"', 'g'))[1] AS seeds_url
    FROM (
        SELECT content AS filtered_content
        FROM html_content
        WHERE md5hash = '1a365c39a8afd80d438ddf1bd3c9afed'
    ) AS filtered_data;
"""
cursor.execute(query)
list_seed_url = cursor.fetchall()

### Get a name from the seed URL
for rows in list_seed_url:
    seed_full_url = "https://inspection.canada.ca" + rows['seeds_url']
    
    query = (
    f"SELECT regexp_replace("
    f"'{seed_full_url}', '.*seeds-identification/([^/]+).*', '\\1') AS seed_name;"
    )
    cursor.execute(query)
    seed_name_query = cursor.fetchall()
    
    if seed_name_query:
        seed_name = seed_name_query[0]['seed_name']
        url_to_seed_mapping[seed_full_url] = seed_name

# Now you have a dictionary where the keys are URLs and the values are seed names
print("\nList of selected seeds :")
for url, seed_name in url_to_seed_mapping.items():
    print(f"{seed_name}")

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
    for url, seed_name in url_to_seed_mapping.items():
        print("\nCurrent seed : " + seed_name)
        seed_json_path = seed_name + ".json"

        if nachet.json_file_exists(seed_data_path, seed_json_path):
            print(f"The JSON file {seed_json_path} exists in {seed_data_path}, skipping")
        else:
            query = """
            SELECT
                REGEXP_REPLACE(hc.content, '<[^>]+>', '', 'g') AS cleaned_content
            FROM
                html_content hc
            INNER JOIN
                crawl c ON hc.md5hash = c.md5hash
            WHERE
                c.url = '""" + url + """';
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
                file_name = seed_name
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