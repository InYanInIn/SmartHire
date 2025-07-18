import os

from ml.model import ExtractModel
import json

api_key="AIzaSyCNyNfBc9i_aAE1JJ7s_VExM_GEY3aKKRY"
model_name = "gemini-2.0-flash-lite"


print("Welcome to SmartHire Resume Extractor!")
print("Give me your file and I will extract all the data from it and save")
print("it in the same folder as the file with the same name but .json extension")
print("Supported file formats: PDF, DOCX, TXT")

file_path = input("Enter path to your file: ").strip()


model = ExtractModel(api_key, model_name)
result = model.extract_data(file_path)

print(result)

output_file = os.path.splitext(file_path)[0] + ".json"

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=4, ensure_ascii=False)


print(f"JSON data saved to {output_file}")