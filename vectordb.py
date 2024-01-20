import json
data_path = "data/courses.md"
documents = []
with open(data_path, "r") as file:
    next_line_is_description = False
    course_title = ""
    course_description = ""
    for line in file:
        if line == "\n":
            continue
        print(line)
        if "##" in line:
            course_title = line.lstrip("## ").rstrip("\n")
            next_line_is_description = True
            continue
        if next_line_is_description:
            course_description = line.rstrip("\n")
            documents.append({
                "title": course_title,
                "description": course_description
            })
            course_title = ""
            course_description = ""
            next_line_is_description = False

# Specify the path to the JSON file
json_file_path = "data/course_docs.json"

# Write the list of dictionaries to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(documents, json_file, indent=2)
