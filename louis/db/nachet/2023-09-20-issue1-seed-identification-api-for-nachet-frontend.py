import dotenv
import os
import openai
import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
import json
dotenv.load_dotenv()

def load_prompt(filename):
    prompt_folder = "../louis/prompt"
    full_path = os.path.join(prompt_folder, filename)

    with open(full_path, 'r') as file:
        content = file.read()

    return content

def load_json_template():
    json_file_path = "../louis/prompt/json_template.json"

    with open(json_file_path, 'r') as file:
        data = json.load(file)  # Load the JSON data as a Python dictionary

    # Convert the dictionary back to a JSON-formatted string
    content = json.dumps(data, indent=4)  # Use 'indent' for pretty printing

    return content

### Step 1: Connect to the database
LOUIS_SCHEMA= os.environ.get('LOUIS_SCHEMA')
LOUIS_DSN = os.environ.get("LOUIS_DSN")
PGUSER=os.environ.get('PGUSER')

def connect_db():
    connection = psycopg.connect(
    conninfo=LOUIS_DSN,
    row_factory=dict_row,
    autocommit=False,
    options=f"-c search_path={LOUIS_SCHEMA},public")
    assert connection.info.encoding == 'utf-8', (
    'Encoding is not UTF8: ' + connection.info.encoding)
    register_vector(connection)
    return connection

database = connect_db()
cursor = database.cursor()

### Step 2: Get a list of all the seeds
seed_list = []
wanted_files_number = 1

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
      
### Step 3: Get the HTML pages of the seeds
pages_list = []

for seed in seed_list:
    query = """
        SELECT
            REGEXP_REPLACE(content, '<[^>]+>', '', 'g') AS cleaned_content
        FROM
            html_content
        WHERE content
            LIKE '%<h1 id="wb-cont" property="name">%<i lang="la">""" + seed + """</i>%</h1>%';
    """
    cursor.execute(query)
    web_pages_fr_en = cursor.fetchall()
    
    all_language_page = ""
    for row in web_pages_fr_en:
        web_text = row.get('cleaned_content')
        all_language_page += web_text
    pages_list.append(all_language_page)

cursor.close()
database.close()

### Step 4: Connect to the OpenAI Azure Chat
AZURE_OPENAI_ENDPOINT= os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_API_ENGINE=os.environ.get('OPENAI_API_ENGINE')

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = OPENAI_API_KEY

### Step 5: Ask ChatGPT to parse the files and give you JSON
directory_path = "../data"

def json_file_exists(directory_path, file_name):
    """
    Check if a JSON file exists in the specified directory.

    Args:
        directory_path (str): The directory path to check for the JSON file.
        file_name (str): The name of the JSON file (including the ".json" extension).

    Returns:
        bool: True if the JSON file exists, False otherwise.
    """
    file_path = os.path.join(directory_path, file_name)
    return os.path.exists(file_path)

compteur = 0
for element in seed_list:
    print("Current seed : " + element)
    seed_json_path = element + ".json"
    if json_file_exists(directory_path, seed_json_path):
        print(f"The JSON file {seed_json_path} exists in {directory_path}, skipping")
    else:    
        page = pages_list[compteur]
        print("Sending request for summary to Azure OpenAI endpoint...\n")
        response = openai.ChatCompletion.create(
            engine=OPENAI_API_ENGINE,
            temperature=0,
            max_tokens=600,
            messages = [
                {"role": "system", "content": load_prompt("system_prompt.txt")},
                {"role": "user", "content": load_prompt("user_prompt.txt") + "You have to return a JSON files that follow this template :\n\n" + load_json_template() + "\n\nhere is the text to parse" + page}
            ]
        )
        # Missing IMAGES and SOURCE, will use SQL for this.
        print("Chat answer: \n" + response.choices[0].message.content + "\n")

        ### Step 6: Translate the JSON into data for the database
        data = json.loads(response.choices[0].message.content)

        # Function to decode Unicode escape sequences in French text
        def decode_french_text(text):
            return text.encode('latin1').decode('unicode-escape')
        
        if isinstance(data, list) and len(data) > 0:
            first_dict = data[0]
            filename_key = "scientific_name"
            file_name = first_dict.get(filename_key, "no_data.json") 
            # Decode the file name if it contains Unicode escape sequences
            file_name = decode_french_text(file_name)
        else:
            # Use a default filename if there's no valid data
            file_name = "no_data"  
        file_name += ".json"
        file_path = f"{directory_path}/{file_name}"
        with open(file_path, "w") as json_file:
            # Use ensure_ascii=False to allow non-ASCII characters
            json.dump(data, json_file, ensure_ascii=False)  
        print(f"JSON data written to {file_path}")
    compteur = compteur + 1