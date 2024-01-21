import json
data_path = "data/courses.md"
documents = []
with open(data_path, "r") as file:
    next_line_is_description = False
    course_title = ""
    course_description = ""
    course_code = ""
    for line in file:
        if line == "\n":
            continue
        # print(line)
        if "##" in line:
            line = line.lstrip("## ").rstrip("\n").split(" - ")
            if (len(line) < 2): continue
            print(line)
            course_code = line[0]
            course_title = line[1]
            next_line_is_description = True
            continue
        if next_line_is_description:
            line = line.rstrip("\n")
            second_period_idx = line.find('.', line.find('.') + 1)
            course_description = line[second_period_idx + 1:].strip()
            course_description_split = course_description.split('.')
            course_description_split
            # print(course_description)
            credit_hours_sentence = line[:second_period_idx]
            # print(credit_hours_sentence)
            first_colon_idx = credit_hours_sentence.find(':')
            credit_hours = credit_hours_sentence[first_colon_idx + 1:].strip().replace("to", "-")
            documents.append({
                "code": course_code,
                "title": course_title,
                "credit_hours": credit_hours,
                "description": course_description,
                "chunk": f"COURSE_TITLE: {course_title} | COURSE_CODE: {course_code} | DESCRIPTION: {line}",
            })
            course_title = ""
            course_description = ""
            course_code = ""
            next_line_is_description = False

# Specify the path to the JSON file
json_file_path = "data/course_docs_2.json"

# Write the list of dictionaries to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(documents, json_file, indent=2)
