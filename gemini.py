import google.generativeai as genai
from vectordb import process_data_and_query

genai.configure(api_key='KEY')
model = genai.GenerativeModel('gemini-pro')

data_dir = "data/course_docs_emb.json"
query_texts = [str(input("Enter your query: "))]
n_results = 6
courses = process_data_and_query(data_dir, query_texts, n_results)

initial_prompt_1 = "You are an assistant helping talking to students directly to register for classes based on their degree requirements and interests. The student is currently studying:"
degrees = "Computer Science, Data Science"
initial_prompt_2 = ". For your reference, are a some relevant courses that may be suitable for the student:"
course_prompt = "\n".join(courses)
initial_prompt_3 = ". Please concisely describe a couple courses that you think would be the best fit for the student and why."

final_prompt = initial_prompt_1 + degrees + initial_prompt_2 + course_prompt + initial_prompt_3

response = model.generate_content(final_prompt)

print(response.text)
