import os  
import sys  
import json  
from datetime import date  
  
import ailab.db as db  
from ailab.models import openai  
import ailab.db.finesse as finesse  
  
from ailab.db.finesse.test_queries import get_random_chunk  
  
# Constants  
TEST_VERSION = date.today()  
REQUIRED_QUESTIONS = 1  
CHARACTER_LIMIT = 14383  
STORAGE_PATH = "/home/vscode/finesse-data-2/qna"  
  
def load_prompts_and_template(prompt_path):  
    """Loads prompts and template from provided path"""  
    system_prompt = finesse.load_prompt(prompt_path, "qna_system_prompt.txt")  
    user_prompt = finesse.load_prompt(prompt_path, "qna_user_prompt.txt")  
    json_template = finesse.load_json_template(prompt_path)  
      
    return system_prompt, user_prompt, json_template  
  
def construct_user_prompt(user_prompt, random_chunk_str, json_template):    
    """Constructs the user prompt using the user prompt, random chunk and json template"""    
    return (f"{user_prompt}\n\nHere is the JSON containing the search:\n{random_chunk_str}"  
           f"\n\nAnd here is the JSON template:\n{json_template}")  

  
def generate_question(system_prompt, user_prompt, json_template, project_db):    
    """Generates a question and saves it to a file"""    
    average_tokens = 0    
    for i in range(REQUIRED_QUESTIONS):    
        with project_db.cursor() as cursor:    
            random_chunk = get_random_chunk(cursor)    
            if not random_chunk:    
                print("No chunk found in the database.")    
                sys.exit(1) # exit the program if chunk is empty  
    
        constructed_user_prompt = construct_user_prompt(user_prompt, str(random_chunk), json_template)    
        total_length = len(system_prompt) + len(constructed_user_prompt)    
        average_tokens += total_length    
    
        if total_length < CHARACTER_LIMIT:    
            response = openai.get_chat_answer(system_prompt, constructed_user_prompt, 2000)    
            data = json.loads(response.choices[0].message.content)    
            if isinstance(data, dict):    
                for chunk in random_chunk:    
                    data["text_content"] = chunk["text_content"]    
                save_response_to_file(data)    
    
    return average_tokens / REQUIRED_QUESTIONS    

  
def save_response_to_file(data):  
    """Saves the provided data to a new file"""  
    file_number = 1  
    while True:  
        file_name = f"qna_{TEST_VERSION}_{file_number}.json"  
        file_path = os.path.join(STORAGE_PATH, file_name)  
        if not os.path.exists(file_path):  
            break  
        file_number += 1  
  
    with open(file_path, "w") as json_file:  
        print("File saved into: " + file_path)  
        json.dump(data, json_file, ensure_ascii=False, indent=4)  
  
def main():  
    if len(sys.argv) < 2:  
        print(f"Usage: {sys.argv[0]} PROMPT_PATH")  
        print("PROMPT_PATH: Directory containing the API prompt")  
        sys.exit(1)  
  
    prompt_path = sys.argv[1]  
    if not os.path.exists(prompt_path):  
        print(f"The directory '{prompt_path}' does not exist.")  
        sys.exit(1)  
  
    system_prompt, user_prompt, json_template = load_prompts_and_template(prompt_path)  
    project_db = db.connect_db()  

      
    average_tokens_per_chunk = generate_question(system_prompt, user_prompt, json_template, project_db)  
    if average_tokens_per_chunk is None:  
        print("No questions were generated.")  
        sys.exit(1)  
      
    print("Average Tokens sent to the API : " + str(average_tokens_per_chunk))  
  
if __name__ == "__main__":  
    main()  
