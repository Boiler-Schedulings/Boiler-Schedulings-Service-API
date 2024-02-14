from flask import Flask
from flask import request
import chromadb
import json
import google.generativeai as genai
genai.configure(api_key='AIzaSyCCrHwe8X7xKJYKpqQhJwBOqaMqB8R-GW8')
model = genai.GenerativeModel('gemini-pro')



chroma_client = chromadb.Client()
catalog_collection = chroma_client.create_collection(name="course_catalog")
data_dir = "data/course_docs_emb.json"
with open(data_dir) as json_file:
    documents = json.load(json_file)
embeddings = [doc["embeddings"] for doc in documents]
docs = [doc["chunk"] for doc in documents]
ids = [str(i) for i in range(len(embeddings))]
catalog_collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=ids
)
def query_course_catalog(query_texts, n_results=2):
    results = catalog_collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
    # return results
    return [course for course in results['documents'][0]]


# res = query_course_catalog("I want to study farming.")
# print(res)
# prompt_1 = """
# ### Task
# You are an expert at formatting questions for input into a course assistant AI. Given a user input format it to be optimized for retrieval of relevant courses from a vector database.

# ### Examples
# Input: I am a CS major, but I want to take some easy non-stem classes to explore other subjects. What are some classes that fit this description that are also 1 or 2 credits only?
# Output: I want to take some classes in fields such as philosophy, social science, the arts, finance, and other non-stem related fields. 1 - 2 credits.
# Input: Is there a class about managing an industrial farming operation?
# Output: Industrial farming operations,
# """
prompt_2 = """
You are a friendly course scheduling assistant for Purdue University. Given a user query, and some relevant classes to their query answer their question as best as posisble.
Here are some classes that may be relevant to the user's query:
{context_str}
If you are not provided enough context, please ask the user to expand on their request and provide more details.
Here is the user's query:
{query_str}
"""
chat = model.start_chat(history=[])
def send_message(query):
    courses = query_course_catalog(query)
    courses_str = "\n".join(courses)
    response = chat.send_message(
        prompt_2.format(context_str=courses_str, query_str=query)
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

from flask import Flask, jsonify, request
from past_grades_other import ExcelDataProcessorOther
from past_grades import ExcelDataProcessor
from rate_my_professor import professor
import json

app = Flask(__name__)
CORS(app)


data_processors = {
    'Spring 2023': ExcelDataProcessor,
    'Fall 2022': ExcelDataProcessorOther,
    #'Summer 2022': ExcelDataProcessorOther,
    'Spring 2022': ExcelDataProcessorOther,
    #'Fall 2021': ExcelDataProcessorOther,
    #'Sum16-Sum21': ExcelDataProcessorOther
}

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@app.route('/get_average_grade_by_teacher', methods=['GET', 'POST'])
def get_average_grade_by_teacher():
    if request.method == 'GET':
        teacher_name = request.args.get('teacher_name')
        course_number = request.args.get('course_number')
        subject = request.args.get('subject')
    elif request.method == 'POST':
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        course_number = data.get('course_number')
        subject = data.get('subject')
    else:
        return jsonify({'error': 'Invalid request method.'}), 400

    results = {}

    for sheet_name, data_processor_class in data_processors.items():
        processor_instance = data_processor_class(r"Course Grade Distribution - Term Sum16 through Spring23.xlsx", sheet_name)
        result = processor_instance.get_average_grade_by_teacher(teacher_name, course_number, subject)
        results[sheet_name] = result

    # Convert the results to a JSON-formatted string with the set_default function
    json_results = json.dumps(results, default=set_default)

    return jsonify(json_results)

@app.route('/sort_teachers_by_average_grade', methods=['GET', 'POST'])
def sort_teachers_by_average_grade():
    if request.method == 'GET':
        teacher_name = request.args.get('teacher_name')
        course_number = request.args.get('course_number')
        subject = request.args.get('subject')
    elif request.method == 'POST':
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        course_number = data.get('course_number')
        subject = data.get('subject')
    else:
        return jsonify({'error': 'Invalid request method.'}), 400

    results = {}

    for sheet_name, data_processor_class in data_processors.items():
        processor_instance = data_processor_class(r"Course Grade Distribution - Term Sum16 through Spring23.xlsx", sheet_name)
        result = processor_instance.sort_teachers_by_average_grade(course_number, subject)
        results[sheet_name] = result

    json_results = json.dumps(results, default=set_default)

    return jsonify(json_results)

@app.route('/get_average_grade_of_class', methods=['GET', 'POST'])
def get_average_grade_of_class():
    if request.method == 'GET':
        teacher_name = request.args.get('teacher_name')
        course_number = request.args.get('course_number')
        subject = request.args.get('subject')
    elif request.method == 'POST':
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        course_number = data.get('course_number')
        subject = data.get('subject')
    else:
        return jsonify({'error': 'Invalid request method.'}), 400

    results = {}

    for sheet_name, data_processor_class in data_processors.items():
        processor_instance = data_processor_class(r"Course Grade Distribution - Term Sum16 through Spring23.xlsx", sheet_name)
        result = processor_instance.get_average_grade_of_class(course_number, subject)
        results[sheet_name] = result

    json_results = json.dumps(results, default=set_default)

    return jsonify(json_results)

@app.route('/rate_my_professor', methods=['GET', 'POST'])
def rate_my_professor():
    if request.method == 'GET':
        teacher_name = request.args.get('teacher_name')
        teacher_name = teacher_name.replace(',', ' ')
    elif request.method == 'POST':
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        teacher_name = teacher_name.replace(',', ' ')
    else:
        return jsonify({'error': 'Invalid request method.'}), 400

    results = professor(teacher_name)

    json_results = json.dumps(results, default=set_default)

    return jsonify(json_results)

@app.route("/catalog", methods=['GET', 'POST'])
def catalog():
    print("test")
    query = request.args.get('query')
    topk = request.args.get('topk', default=2)
    return query_course_catalog(query, int(topk))

@app.route("/thread", methods=['GET'])
def thread():
    user_message = request.args.get('message')
    res = send_message(user_message)
    print(chat.history)
    return {
        "response": res,
        "history": [{"message": obj.parts[0].text, "role": obj.role} for obj in chat.history]
    }

if __name__ == '__main__':
    app.run(debug=True, port=8001, host="0.0.0.0")