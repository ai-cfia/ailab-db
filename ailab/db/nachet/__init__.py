import os
import json

def load_prompt(filename, prompt_path):
    full_path = os.path.join(prompt_path, filename)

    with open(full_path, 'r') as file:
        content = file.read()

    return content

def load_json_template(json_path):
    json_file_path = json_path + "/json_template.json"

    with open(json_file_path, 'r') as file:
        data = json.load(file)  # Load the JSON data as a Python dictionary

    # Convert the dictionary back to a JSON-formatted string
    content = json.dumps(data, indent=4)  # Use 'indent' for pretty printing

    return content

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

def decode_french_text(text):
    return text.encode('latin1').decode('unicode-escape')