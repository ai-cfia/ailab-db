## How to install postgresl-client-15
```
./bin/install-postgresl-client-15.sh
```

## How to generate question
Usage:
```
./bin/generate_qna_chunk.sh PROMPT_PATH

or

./bin/generate_qna_crawl.sh PROMPT_PATH
```
PROMPT_PATH: path were you can find the user and system prompt for the openai API and the JSON template.

### Example command
```
./bin/generate_qna_crawl.sh ailab/db/finesse/prompt
```

Question generation occurs in three parts. First, we retrieve a random "crawl" page from the database (random but sorted based on a specific score value). Then, we instruct ChatGPT on what to do (in our case, gather and analyze data, then generate a question and an answer). Once these steps are completed, we store all the data in a JSON file and process the next document. This code is highly useful for generating various tests, designed to be as reusable as possible. If we want to change the instructions or models, we can simply call others during function execution with PROMPT_PATH (preferably using the script in bash rather than Python to call the code).  
We can run the code to search based on "chunks" or "crawls." I strongly recommend using crawl-based search since, without found scores for chunks (I cannot guarantee their existence), crawl-based search generates better questions.  
Regarding data retrieval, it may be necessary to modify the code to best fit a new scenario. As for the number of generated questions, simply modify the global variable at the top of the script.

<span style="color:red"> Don't forgot to setup environnement variable or secret before use </span>

### Environnement variable or secret

You will need the following to run the OpenAI service:

  * OPENAI_API_KEY: The API key required for authentication when making requests to the OpenAI API. It can be found [here](https://portal.azure.com/#home).

  * OPENAI_ENDPOINT: The link used to call into Azure OpenAI endpoints. It can be found at the same place as the OPENAI_API_KEY.

  * OPENAI_API_ENGINE: The name of the model deployment you want to use (ex:ailab-gpt-35-turbo).



