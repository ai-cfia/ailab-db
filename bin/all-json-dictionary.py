import os
import json
import sys

# Define the directory where your JSON files are located
if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " SEED_DATA_PATH PROMPT_PATH")
    print("SEED_DIRECTORY_PATH: Directory for storing seeds")
    sys.exit(1)

SEED_DIRECTORY_PATH = sys.argv[1]

if not os.path.exists(SEED_DIRECTORY_PATH):
    print(f"The directory '{SEED_DIRECTORY_PATH}' does not exist.")
    sys.exit(1)

# Initialize an empty dictionary to store the combined data
combined_data = {}

# Iterate through the JSON files in the directory
for filename in os.listdir(SEED_DIRECTORY_PATH):
    if filename.endswith(".json"):
        file_path = os.path.join(SEED_DIRECTORY_PATH, filename)
        scientific_name = os.path.splitext(filename)[
            0
        ]  # Extract the scientific name from the filename

        # Read and parse the JSON data from the file with 'utf-8' encoding
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        # Add the parsed JSON data to the combined dictionary
        combined_data[scientific_name] = json_data

# Write the combined dictionary to a new file named "all.json"
with open(
    os.path.join(SEED_DIRECTORY_PATH, "all.json"), "w", encoding="utf-8"
) as output_file:
    json.dump(combined_data, output_file, indent=4, ensure_ascii=False)

print("Combined data has been saved to all.json")
