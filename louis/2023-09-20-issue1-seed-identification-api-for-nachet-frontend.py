### For environment variables
import dotenv
dotenv.load_dotenv()

### For API
import os
import openai

### Step 1: Get all the HTML pages of the seeds

### Step 2: Connect to the OpenAI Azure Chat
AZURE_OPENAI_ENDPOINT= os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_API_ENGINE=os.environ.get('OPENAI_API_ENGINE')

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = OPENAI_API_KEY

### Step 3: Ask ChatGPT to parse the files and give you JSON
print("Sending request for summary to Azure OpenAI endpoint...\n\n")
response = openai.ChatCompletion.create(
    engine=OPENAI_API_ENGINE,
    temperature=0.7,
    max_tokens=120,
    messages=[
       {"role": "system", "content": "You are a helpful assistant. Please answer the question asked by user."},
        {"role": "user", "content": "What is the color of the sea"}
    ]
)

print("Chat answer: " + response.choices[0].message.content + "\n")

### Step 4: Translate the JSON into data for the database
