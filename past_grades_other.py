import pandas as pd
import numpy as np

class ExcelDataProcessorOther:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.load_data()

    def load_data(self):
        try:
            self.excel_data = pd.read_excel(self.file_path, self.sheet_name, header=[7,8])

            self.excel_data = self.excel_data.ffill(axis=0)
            self.excel_data = self.excel_data.fillna(0)
            self.excel_data = self.excel_data.ffill(axis=1)

        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            self.excel_data = None

    def get_info_by_subject_and_course(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        course_subject_rows = (self.excel_data[('Unnamed: 2_level_0', 'Course Number')]== course_number) & (self.excel_data[('Unnamed: 0_level_0', 'Subject')].str.strip().str.lower() == subject.lower())
        print(course_subject_rows)
        selected_info = self.excel_data.loc[
            course_subject_rows, (['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E',
                                  'F'], '% of Total')].values
        return selected_info

    def get_average_grade_by_teacher(self, teacher_name, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        teacher_rows = self.excel_data[('Unnamed: 8_level_0', 'Instructor')].str.strip().str.lower() == teacher_name.lower()
        course_subject_rows = (self.excel_data[('Unnamed: 2_level_0', 'Course Number')]== course_number) & (self.excel_data[('Unnamed: 0_level_0', 'Subject')].str.strip().str.lower() == subject.lower())
        selected_rows = self.excel_data[teacher_rows & course_subject_rows]
        if selected_rows.empty:
            print(f"Error: No data found for teacher '{teacher_name}', course '{course_number}', and subject '{subject}'.")
            return None
        grade_columns = ['A', 'A-', 'A+', 'AU', 'B', 'B-', 'B+', 'C', 'C-', 'C+', 'D', 'D-', 'D+', 'E', 'F']
        grade_patterns = [(grade, '% of Total') for grade in grade_columns]
        selected_info = selected_rows[grade_patterns]
        grade_to_gpa = np.array([4.0, 3.7, 4.0, 4.0, 3.0, 2.7, 3.3, 2.0, 1.7, 2.3, 1.0, 0.7, 1.3, 0.0, 0.0])
        average_gpa = (selected_info * grade_to_gpa).sum().sum()/len(selected_info)
        return average_gpa

    def sort_teachers_by_average_grade(self, course_number, subject):
        if self.excel_data is None:
            print("Error: Data not loaded.")
            return None

        teachers = self.excel_data.loc[(self.excel_data[('Unnamed: 2_level_0', 'Course Number')] == course_number) & (
                    self.excel_data[('Unnamed: 0_level_0', 'Subject')].str.strip().str.lower() == subject.lower()), ('Unnamed: 8_level_0', 'Instructor')].unique()

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

        teachers = self.excel_data.loc[(self.excel_data[('Unnamed: 2_level_0', 'Course Number')] == course_number) & (
                self.excel_data[('Unnamed: 0_level_0', 'Subject')].str.strip().str.lower() == subject.lower()), ('Unnamed: 8_level_0', 'Instructor')].unique()

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
"""
# Example usage:
file_path = r"Course Grade Distribution - Term Sum16 through Spring23.xlsx"
sheet_name = 'Fall 2022'

data_processor = ExcelDataProcessorOther(file_path, sheet_name)
course_number = 20300
subject = 'AAE'

teacher = data_processor.get_average_grade_by_teacher('Hassan, Hashim', 20300, 'AAE')
print('......')
print(teacher)
average_class_grade = data_processor.get_average_grade_of_class(20300, 'AAE')
if average_class_grade is not None:
    print(f"Average GPA of the Class: {average_class_grade}")

sorted_teachers = data_processor.sort_teachers_by_average_grade(20300, 'AAE')
if sorted_teachers is not None:
    print("Sorted Teachers by Average GPA:")
    for teacher_info in sorted_teachers:
        print(f"Instructor: {teacher_info['Instructor']}, Average GPA: {teacher_info['Average GPA']}")"""