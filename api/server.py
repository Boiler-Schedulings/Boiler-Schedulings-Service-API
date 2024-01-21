from flask import Flask
from flask import request
import chromadb
import json
import google.generativeai as genai
genai.configure(api_key='AIzaSyCCrHwe8X7xKJYKpqQhJwBOqaMqB8R-GW8')
model = genai.GenerativeModel('gemini-pro')

chroma_client = chromadb.Client()
catalog_collection = chroma_client.create_collection(name="course_catalog")
data_dir = "../data/course_docs_emb.json"
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
{context_str}\n
{majors_str}
If you are not provided enough context, please ask the user to expand on their request and provide more details.
Here is the user's query:
{query_str}
"""
chat = model.start_chat(history=[])
def send_message(query, degrees):
    courses = query_course_catalog(query)
    courses_str = "\n".join(courses)
    majors_str = "These are the degrees I am pursuing: ".join(degrees)
    response = chat.send_message(
        prompt_2.format(context_str=courses_str,majors_str=majors_str, query_str=query)
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