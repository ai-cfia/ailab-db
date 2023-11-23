import os
import json


def load_prompt(prompt_path, filename):
    full_path = os.path.join(prompt_path, filename)

    with open(full_path, "r") as file:
        content = file.read()

    return content


def load_json_template(json_path):
    json_file_path = json_path + "/json_template.json"

    with open(json_file_path, "r") as file:
        data = json.load(file)  # Load the JSON data as a Python dictionary

    # Convert the dictionary back to a JSON-formatted string
    content = json.dumps(data, indent=4)  # Use 'indent' for pretty printing

    return content