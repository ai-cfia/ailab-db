import os
import json

# Define the directory where your JSON files are located
current_working_directory = os.getcwd()
directory = current_working_directory + "/seed-data"

# Initialize an empty dictionary to store the combined data
combined_data = {}

# Iterate through the JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        scientific_name = os.path.splitext(filename)[
            0
        ]  # Extract the scientific name from the filename

        # Read and parse the JSON data from the file with 'utf-8' encoding
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        # Add the parsed JSON data to the combined dictionary
        combined_data[scientific_name] = json_data

# Write the combined dictionary to a new file named "all.json"
with open(os.path.join(directory, "all.json"), "w", encoding="utf-8") as output_file:
    json.dump(combined_data, output_file, indent=4, ensure_ascii=False)

print("Combined data has been saved to all.json")
