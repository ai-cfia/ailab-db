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
PGHOST= os.environ.get('PGHOST')
PGBASE=os.environ.get('PGBASE')
PGUSER=os.environ.get('PGUSER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')

LOUIS_SCHEMA= os.environ.get('LOUIS_SCHEMA')
LOUIS_DSN = os.environ.get("LOUIS_DSN")
PGUSER=os.environ.get('PGUSER')

def connect_db():
    """Connect to the postgresql database and return the connection."""
    # print(f"Connecting to {LOUIS_SCHEMA}")
    connection = psycopg.connect(
    conninfo=LOUIS_DSN,
    row_factory=dict_row,
    autocommit=False,
    options=f"-c search_path={LOUIS_SCHEMA},public")
    assert connection.info.encoding == 'utf-8', (
    'Encoding is not UTF8: ' + connection.info.encoding)
    # psycopg.extras.register_uuid()
    register_vector(connection)
    return connection

database = connect_db()
cursor = database.cursor()

### Step 2: Get a list of all the seeds
seed_list = []
cursor.execute("SELECT REGEXP_REPLACE(UNNEST(REGEXP_MATCHES(content, '<i lang=\"la\">(.*?)</i>', 'g')),'<[^>]+>','','g') AS seed_name FROM html_content WHERE md5hash = '1a365c39a8afd80d438ddf1bd3c9afed' LIMIT 5;")
list_seeds_scientific_name = cursor.fetchall()
for rows in list_seeds_scientific_name:
    seed_list.append(rows['seed_name'])

for element in seed_list:
    print(element)

### Step 3: Get the HTML pages of the seeds
pages_list = []

for element in seed_list:
    cursor.execute("SELECT REGEXP_REPLACE(content, '<[^>]+>', '', 'g') AS cleaned_content FROM html_content WHERE content LIKE '%<h1 id=\"wb-cont\" property=\"name\">%<i lang=\"la\">" + element + "</i>%</h1>%';")
    web_pages_fr_en = cursor.fetchall()
    all_language_page = ""

    for row in web_pages_fr_en:
        web_text = row.get('cleaned_content')
        all_language_page += web_text
    pages_list.append(all_language_page)

cursor.close()
database.close()

### Step 3: Connect to the OpenAI Azure Chat
AZURE_OPENAI_ENDPOINT= os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_API_ENGINE=os.environ.get('OPENAI_API_ENGINE')

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = OPENAI_API_KEY

### Step 4: Ask ChatGPT to parse the files and give you JSON
for page in pages_list:
    print("Sending request for summary to Azure OpenAI endpoint...\n\n")
    response = openai.ChatCompletion.create(
        engine=OPENAI_API_ENGINE,
        temperature=0,
        max_tokens=300,
        messages = [
            {"role": "system", "content": load_prompt("system_prompt.txt")},
            {"role": "user", "content": load_prompt("user_prompt.txt") + page + ". The template : " + load_json_template()}
        ]
    )
    ## Missing IMAGES and SOURCE, will use SQL for this.

    ## TXT then check if exist
    ## Try 5 request at one time

    print("Chat answer: " + response.choices[0].message.content + "\n")

### Step 5: Translate the JSON into data for the database
