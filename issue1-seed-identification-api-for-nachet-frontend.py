import os
import json

import ailab.db as db
import ailab.db.nachet as nachet
from ailab.models import openai

from ailab.db.nachet.seed_queries import query_seeds_urls
from ailab.db.nachet.seed_queries import query_get_seed_name
from ailab.db.nachet.seed_queries import query_get_webpage
from ailab.db.nachet.seed_queries import query_get_images 

website_url = "https://inspection.canada.ca"

def create_seed_url_mapping(cursor, list_seed_url):
    ### Get a name from the seed URL
    url_to_seed_mapping = {}

    for rows in list_seed_url:
        seed_full_url = website_url + rows["seeds_url"]
        seed_name_query = query_get_seed_name(cursor, seed_full_url)

        if seed_name_query:
            seed_name = seed_name_query[0]["sd_nme"]
            url_to_seed_mapping[seed_full_url] = seed_name
    return url_to_seed_mapping

def transform_seed_data_into_json(
    cursor, url_to_seed_mapping, system_prompt, load_user_prompt, json_template, SEED_DATA_PATH
):
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
    7. Processes the response, extracting the name and saving it as a JSON file.
    """
    for url, seed_name in url_to_seed_mapping.items():
        print("\nCurrent seed : " + seed_name)
        seed_json_path = seed_name + ".json"

        file_path = os.path.join(SEED_DATA_PATH, seed_json_path)
    
        if (os.path.exists(file_path)):
            print(f"JSON file {seed_json_path} exists in {SEED_DATA_PATH}, skipping")
        else:
            web_pages = query_get_webpage(cursor, url)

            all_language_seed_page = ""
            for row in web_pages:
                web_text = row.get("cleaned_content")
                all_language_seed_page += web_text
            page = all_language_seed_page
            md5hash = row.get("md5hash")

            ### Get the images corresponding to the current page
            images_fetch = query_get_images(cursor, md5hash)

            image_information = ""

            for row in images_fetch:
                image_links = row["photo_link"]
                image_descriptions = row["photo_description"]
                image_information += f"Image link: {image_links}"
                image_information += f"\nImage description: {image_descriptions}\n\n"

            print("Sending request for summary to Azure OpenAI endpoint...\n")

            user_prompt = (
                load_user_prompt
                + "Return a JSON file that follows this template:\n\n"
                + json_template
                + "\n\nhere is the text to parse:\n"
                + page
                + "\n\nAnd here is the images descriptions:\n"
                + image_information
            )

            response = openai.get_chat_answer(system_prompt, user_prompt, 2000)

            data = json.loads(response.choices[0].message.content)

            if isinstance(data, dict):
                file_name = seed_name
                file_name = nachet.decode_french_text(file_name)
                file_name += ".json"

            file_path = os.path.join(SEED_DATA_PATH, file_name)
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"JSON data written to {file_path}")


if __name__ == "__main__":
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    SEED_DATA_PATH = CURRENT_WORKING_DIRECTORY + "/seed-data"
    PROMPT_PATH = CURRENT_WORKING_DIRECTORY + "/nachet-data/prompt"

    system_prompt = nachet.load_prompt("system_prompt.txt", PROMPT_PATH)
    load_user_prompt = nachet.load_prompt("user_prompt.txt", PROMPT_PATH)
    json_template = nachet.load_json_template(PROMPT_PATH)

    nachet_db = db.connect_db()
    with nachet_db.cursor() as cursor:
        list_seed_url = seed_urls = query_seeds_urls(cursor, 1)
        url_to_seed_mapping = create_seed_url_mapping(cursor, list_seed_url)
        print(url_to_seed_mapping)

        print("\nList of selected seeds :")
        for url, seed_name in url_to_seed_mapping.items():
            print(f"{seed_name}")

        transform_seed_data_into_json(
            cursor, url_to_seed_mapping, system_prompt, load_user_prompt, json_template, SEED_DATA_PATH
        )
