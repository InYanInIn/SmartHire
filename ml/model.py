import google.generativeai as genai
import json

from backend.services import document_parser

class ExtractModel:
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)


    def extract_data(self, file_path: str):
        resume_text = document_parser.extract_text(file_path)

        prompt = f"""
        Extract the following fields from the resume text below:
        - Name
        - Location
        - Phone(just numbers, no symbols)
        - Email
        - Education(Just institutions, degree and field of study)
        - Skills(Each skill should be separate, dont group them)
        - Languages(Each language should be separate, dont group them, just names)
        - Experience(Company, Position, Start Date, End Date, Description. If project company name set to PROJECT)

        If you dont find any of these fields, just return an empty string for this field.

        Respond ONLY in JSON like this:
        {{
          "Name": "...",
          "Location": "...",
          "Phone": "...",
          "Email": "...",
          "Education": [
            {{
              "University": "...",
              "Degree": "...",
              "FieldOfStudy": "...",
              "StartDate": "...",
              "EndDate": "..."
            }}
          ],
          "Skills": ["..."],
          "Languages": "...",
          "Experience": [
            {{
              "Company": "...",
              "Position": "...",
              "Description": "...",
              "StartDate": "...",
              "EndDate": "..."
            }}
          ]
        }}


        TEXT:
        \"\"\"{resume_text}\"\"\"
        """

        # Запрос к Gemini
        response = self.model.generate_content(prompt)

        response_text = response.text.strip('`').strip('json')
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response. Please check the output format."}

