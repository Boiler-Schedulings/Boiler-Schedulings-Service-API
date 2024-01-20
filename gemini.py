import google.generativeai as genai
from vectordb import process_data_and_query

genai.configure(api_key='Key')
model = genai.GenerativeModel('gemini-pro')

data_dir = "data/course_docs_emb.json"
query_texts = ["I want a course about the software development working with a team."]
n_results = 2
courses = process_data_and_query(data_dir, query_texts, n_results)

initial_prompt_1 = "You are an assistant helping students register for classes based on their degree requirements and interests. The student is currently studying"
degrees = "Computer Science, Data Science"
initial_prompt_2 = ". Here are a some relevant courses that may be suitable for the student:"
course_prompt = "\n".join(courses)

final_prompt = initial_prompt_1 + degrees + initial_prompt_2 + course_prompt

response = model.generate_content(final_prompt)

print(response.text)
