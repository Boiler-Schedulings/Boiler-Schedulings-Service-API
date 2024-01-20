#pip install -q -U google-generativeai

import google.generativeai as genai

genai.configure(api_key='API_KEY')

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("What is the meaning of life?")

print(response.text)