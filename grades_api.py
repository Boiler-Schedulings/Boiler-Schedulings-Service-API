from flask import Flask, jsonify, request
from past_grades_other import ExcelDataProcessorOther
from past_grades import ExcelDataProcessor
import json

app = Flask(__name__)

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
# Add more routes for other functions as needed

if __name__ == '__main__':
    app.run(debug=True)
