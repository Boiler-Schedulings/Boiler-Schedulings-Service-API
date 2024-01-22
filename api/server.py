from flask import Flask
from flask import request
import chromadb
import json
import google.generativeai as genai
genai.configure(api_key='AIzaSyCCrHwe8X7xKJYKpqQhJwBOqaMqB8R-GW8')
from past_grades_other import ExcelDataProcessorOther
from past_grades import ExcelDataProcessor

model = genai.GenerativeModel('gemini-pro')

chroma_client = chromadb.Client()
catalog_collection = chroma_client.create_collection(name="course_catalog")
data_dir = "../data/course_docs_emb.json"
with open(data_dir) as json_file:
    documents = json.load(json_file)
embeddings = [doc["embeddings"] for doc in documents]
docs = [doc["chunk"] for doc in documents]
ids = [str(i) for i in range(len(embeddings))]
half = len(embeddings) // 2

catalog_collection.add(
    embeddings=embeddings[:half],
    documents=docs[:half],
    ids=ids[:half]
)

catalog_collection.add(
    embeddings=embeddings[half:],
    documents=docs[half:],
    ids=ids[half:]
)

def query_course_catalog(query_texts, n_results=2):
    results = catalog_collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
    print(results)
    return results
    # return [course for course in results['documents'][0]]

data_processors = {
    'Spring 2023': ExcelDataProcessor,
    'Fall 2022': ExcelDataProcessorOther,
    #'Summer 2022': ExcelDataProcessorOther,
    'Spring 2022': ExcelDataProcessorOther,
    #'Fall 2021': ExcelDataProcessorOther,
    #'Sum16-Sum21': ExcelDataProcessorOther
}
def get_average_grade_by_teacher(course_code):
    results = {}
    teacher_name = "test"
    course_number = course_code.split(' ')[1]
    subject = course_code.split(' ')[0].upper()
    results = {}
    print(course_number)
    print(subject)
    for sheet_name, data_processor_class in data_processors.items():
        processor_instance = data_processor_class(r"Course Grade Distribution - Term Sum16 through Spring23.xlsx", sheet_name)
        result = processor_instance.sort_teachers_by_average_grade(int(course_number), subject)
        results[sheet_name] = result
    return results
# res = query_course_catalog("I want to study farming.")
# print(res)
prompt_1 = """
### Task
You are an expert at formatting questions for input into a course assistant AI. Given a user input, optimize it for retrieval of relevant courses from a vector database.

### Examples
Input: I'm interested in cs.
Output: Computer science courses covering topics like programming, algorithms, machine learning, and data structures. Suitable for various levels, from introductory to advanced.

Input: I want to learn about corn.
Output: Agricultural science courses focusing on crop cultivation, with an emphasis on corn - including its biology, cultivation techniques, and its role in the global economy.

Input: cs
Output: Comprehensive range of computer science courses, including introductory programming, software engineering, artificial intelligence, and cybersecurity.

Input: corn
Output: Courses related to agronomy and plant science, specifically targeting corn cultivation, genetics, pest management, and sustainable farming practices.

Input: I am a CS major, but I want to take some easy non-stem classes to explore other subjects. What are some classes that fit this description that are also 1 or 2 credits only?
Output: Non-STEM introductory courses, suitable for CS majors, 1-2 credit hours. Options include art history, basic psychology, and introductory economics.

Input: Is there a class about managing an industrial farming operation?
Output: Courses related to agriculture, focus on industrial farming management. Topics include farm management principles, modern agricultural technology, and sustainable practices.

Input: I need a course to improve my writing skills as an engineering student.
Output: Writing enhancement courses for engineering students, focus on technical and professional writing. Includes scientific communication, technical report writing, and research documentation.

Input: Looking for a beginner's course in psychology.
Output: Introductory courses in psychology, suitable for beginners. Topics may include fundamentals of human behavior, cognitive processes, and introductory social psychology.

User's query:
{query_str}
"""

prompt_2 = """
You are a course scheduling AI for Purdue University. Your task is to provide a structured response to the user's query, focusing on generating data that can be easily parsed for different APIs. The response should include specific course details, relevant majors, credit hours, and any other pertinent information based on the user's query and the provided context.

Here are some classes and majors that may be relevant to the user's query:
{context_str}
{majors_str}

User's query:
{query_str}

Structured response for API parsing:
"""
prompt_3 = """
Based on the structured data provided by the first prompt, this task involves summarizing the actions taken by various APIs. The summary should reflect what the first prompt identified as important, including course enrollment actions, schedule adjustments, or information retrieval.

Structured response for API parsing:
{structured_response_str}

API call data:
{api_call_data_str}

Summary of actions taken:
"""

prompt_4 = """
This task is to provide a conversational summary based on the context of the user's query and the actions taken as per the API calls. The summary should be concise and informative, delivered in a few sentences to give the user a clear understanding of the results and actions taken.

User's query:
{query_str}

Summary of actions taken:
{actions_taken_str}

Conversational summary:
"""


def gen_context_str(course_strs, teachers_info):
    res = ""
    for i in range(len(course_strs)):
        course_str = course_strs[i]
        res += course_str + "\n"
        if i >= len(teachers_info): continue
        teachers = teachers_info[i]
        first_key = list(teachers.keys())[0]
        teachers = teachers[first_key]
        if teachers == None: continue
        teacher_str = " ; ".join([f"Name: {teacher_obj['Instructor']}, Average GPA: {round(teacher_obj['Average GPA'], 2)}" for teacher_obj in teachers])
        res += "| TEACHER_INFORMATION: " + teacher_str + "\n"
    return res
        
chat = model.start_chat(history=[])
def send_message(query, degrees):
    print(degrees)
    majors_str = "These are the degrees I am pursuing: " + ",".join(degrees)
    relevant_docs = query_course_catalog(query)
    course_doc_objs = [documents[int(id)] for id in relevant_docs['ids'][0]]
    course_codes = [obj['code'] for obj in course_doc_objs]
    course_strs = [course for course in relevant_docs['documents'][0]]

    teachers_info = [get_average_grade_by_teacher(course_code) for course_code in course_codes]
    context_str = gen_context_str(course_strs, teachers_info)
    print(teachers_info)
    print()
    print(prompt_2.format(context_str=context_str, majors_str=majors_str, query_str=query))
    print()
    response = chat.send_message(
        prompt_2.format(context_str=context_str, majors_str=majors_str, query_str=query)
    )
    return response.text
# while True:
#     query = input("Query: ")
#     courses = query_course_catalog(query)
#     courses_str = "\n".join(courses)
#     # print(prompt.format(context_str=courses, query_str=query))
#     print()
#     response = chat.send_message(
#         prompt_2.format(context_str=courses_str, query_str=query)
#     )
#     print(response.text)
#     print(chat.history[0].parts[0].text)

# """
# Test Queries
# I am a CS major, but I want to take some easy non-stem classes to explore other subjects. What are some classes that fit this description that are also 1 or 2 credits only?


# """

from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/catalog", methods=['GET', 'POST'])
def catalog():
    print("test")
    query = request.args.get('query')
    topk = request.args.get('topk', default=2)
    return query_course_catalog(query, int(topk))

@app.route("/thread", methods=['GET'])
def thread():
    user_message = request.args.get('message')
    user_degrees = request.args.get('degrees')
    res = send_message(user_message, user_degrees)
    print(chat.history)
    return {
        "response": res,
        "history": [{"message": obj.parts[0].text, "role": obj.role} for obj in chat.history]
    }

if __name__ == '__main__':
    app.run(debug=True, port=8001, host="0.0.0.0")

# print(get_average_grade_by_teacher("CS 18200"))
# print(send_message("I want to explore computer science. I am a first year student. Do you know any good courses that are not too hard?"))
