import pandas as pd
import numpy as np

class ExcelDataProcessor:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.load_data()

    def load_data(self):
        try:
            self.excel_data = pd.read_excel(self.file_path, self.sheet_name, header=7)
            selected_columns = ['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E', 'F', 'I',
                                'N', 'NS', 'P', 'PI', 'S', 'SI', 'U', 'W', 'WF', 'WN']

            self.excel_data[selected_columns] = self.excel_data[selected_columns].fillna(0)
            self.excel_data = self.excel_data.ffill(axis=0)
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            self.excel_data = None

    def get_info_by_subject_and_course(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        course_subject_rows = (self.excel_data['Course Number'] == course_number) & (self.excel_data['Subject'].str.strip().str.lower() == subject.lower())
        selected_info = self.excel_data.loc[course_subject_rows, ['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E', 'F']].values
        return selected_info

    def get_distribution_by_subject_and_course(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        course_subject_rows = (self.excel_data['Course Number'] == course_number) & (self.excel_data['Subject'].str.strip().str.lower() == subject.lower())
        selected_info = self.excel_data.loc[course_subject_rows, ['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E', 'F']].values
        avg_arr = np.mean(selected_info, axis=0)
        return avg_arr

    def get_average_grade_by_teacher(self, teacher_name, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        teacher_rows = self.excel_data['Instructor'].str.strip().str.lower() == teacher_name.lower()
        course_subject_rows = (self.excel_data['Course Number'] == course_number) & (self.excel_data['Subject'].str.strip().str.lower() == subject.lower())
        selected_rows = self.excel_data[teacher_rows & course_subject_rows]

        if selected_rows.empty:
            print(f"Error: No data found for teacher '{teacher_name}', course '{course_number}', and subject '{subject}'.")
            return None
        selected_grades = selected_rows[['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E', 'F']].fillna(0).values
        grade_to_gpa = np.array([4.0, 3.7, 4.0, 4.0, 3.0, 2.7, 3.3, 2.0, 1.7, 2.3, 1.0, 0.7, 1.3, 0.0, 0.0])

        # Calculate average GPA using the dot product

        average_gpa = (selected_grades * grade_to_gpa).sum().sum()/len(selected_grades)
        return average_gpa

    def sort_teachers_by_average_grade(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        # Get unique teachers for the specified course and subject
        teachers = self.excel_data.loc[(self.excel_data['Course Number'] == course_number) & (
                    self.excel_data['Subject'].str.strip().str.lower() == subject.lower()), 'Instructor'].unique()

        if len(teachers) == 0:
            print(f"Error: No teachers found for course '{course_number}' and subject '{subject}'.")
            return None  # No teachers found for the specified course and subject

        teacher_avg_gpas = []

        for teacher in teachers:
            average_gpa = self.get_average_grade_by_teacher(teacher, course_number, subject)
            if average_gpa is not None:
                teacher_avg_gpas.append({'Instructor': teacher, 'Average GPA': average_gpa})

        # Sort teachers by average GPA in descending order
        sorted_teachers = sorted(teacher_avg_gpas, key=lambda x: x['Average GPA'], reverse=True)

        return sorted_teachers

    def get_average_grade_of_class(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        teachers = self.excel_data.loc[(self.excel_data['Course Number'] == course_number) & (
                    self.excel_data['Subject'].str.strip().str.lower() == subject.lower()), 'Instructor'].unique()

        if len(teachers) == 0:
            print(f"Error: No teachers found for course '{course_number}' and subject '{subject}'.")
            return None  # No teachers found for the specified course and subject

        total_average_gpa = 0
        total_teachers = 0

        for teacher in teachers:
            average_gpa = self.get_average_grade_by_teacher(teacher, course_number, subject)
            if average_gpa is not None:
                total_average_gpa += average_gpa
                total_teachers += 1
        if total_teachers == 0:
            print(
                f"Error: No data found for calculating the average grade of the class for course '{course_number}' and subject '{subject}'.")
            return None
        return total_average_gpa / total_teachers


file_path = r"Course Grade Distribution - Term Sum16 through Spring23.xlsx"
sheet_name = 'Spring 2023'


data_processor = ExcelDataProcessor(file_path, sheet_name)
info = data_processor.get_info_by_subject_and_course(35201, 'AAE')
info_avg = data_processor.get_distribution_by_subject_and_course(35201, 'AAE')
#average_class_grade = data_processor.get_average_grade_of_class(35201, 'AAE')
#teacher = data_processor.get_average_grade_by_teacher('Mishra, Ritik K.', 20401,'AAE')
print(info)
print('xxxxxxxxxxxx')
print(info_avg)
"""if average_class_grade is not None:
    print(f"Average GPA of the Class: {average_class_grade}")

sorted_teachers = data_processor.sort_teachers_by_average_grade(35201, 'AAE')
if sorted_teachers is not None:
    print("Sorted Teachers by Average GPA:")
    for teacher_info in sorted_teachers:
        print(f"Instructor: {teacher_info['Instructor']}, Average GPA: {teacher_info['Average GPA']}")
"""