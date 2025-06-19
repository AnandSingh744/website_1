import json
import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.marks = {}

    def add_marks(self, subject, mark):
        self.marks[subject] = mark

    def calculate_grade(self):
        try:
            if not self.marks:
                raise ZeroDivisionError("No marks entered for grade calculation.")
            average = sum(self.marks.values()) / len(self.marks)
            if average >= 90:
                return 'A'
            elif average >= 80:
                return 'B'
            elif average >= 70:
                return 'C'
            elif average >= 60:
                return 'D'
            else:
                return 'F'
        except ZeroDivisionError:
            return None

    def to_dict(self):
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "marks": self.marks,
            "grade": self.calculate_grade()
        }

class StudentGradeManagementSystem:
    def __init__(self, filename="students_data.json"):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                students = {item["roll_number"]: Student(item["name"], item["roll_number"]) for item in data}
                for item in data:
                    students[item["roll_number"]].marks = item["marks"]
                return students
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump([student.to_dict() for student in self.students.values()], file)

    def add_student(self, name, roll_number):
        if roll_number in self.students:
            return False
        self.students[roll_number] = Student(name, roll_number)
        self.save_data()
        return True

    def add_marks(self, roll_number, subject, mark):
        if roll_number not in self.students:
            return False
        try:
            mark = float(mark)
            self.students[roll_number].add_marks(subject, mark)
            self.save_data()
            return True
        except ValueError:
            return False

    def view_student(self, roll_number):
        if roll_number not in self.students:
            return None
        return self.students[roll_number]

    def update_student(self, roll_number, name=None):
        if roll_number not in self.students:
            return False
        if name:
            self.students[roll_number].name = name
        self.save_data()
        return True

class StudentGradeManagementApp:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Student Grade Management System")

        # Add Student Frame
        self.add_frame = tk.LabelFrame(root, text="Add Student")
        self.add_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.add_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.add_frame, text="Roll Number:").grid(row=1, column=0)
        self.roll_entry = tk.Entry(self.add_frame)
        self.roll_entry.grid(row=1, column=1)

        tk.Button(self.add_frame, text="Add Student", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=5)

        # Add Marks Frame
        self.marks_frame = tk.LabelFrame(root, text="Add Marks")
        self.marks_frame.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(self.marks_frame, text="Roll Number:").grid(row=0, column=0)
        self.marks_roll_entry = tk.Entry(self.marks_frame)
        self.marks_roll_entry.grid(row=0, column=1)

        tk.Label(self.marks_frame, text="Subject:").grid(row=1, column=0)
        self.subject_entry = tk.Entry(self.marks_frame)
        self.subject_entry.grid(row=1, column=1)

        tk.Label(self.marks_frame, text="Marks:").grid(row=2, column=0)
        self.marks_entry = tk.Entry(self.marks_frame)
        self.marks_entry.grid(row=2, column=1)

        tk.Button(self.marks_frame, text="Add Marks", command=self.add_marks).grid(row=3, column=0, columnspan=2, pady=5)

        # View Student Frame
        self.view_frame = tk.LabelFrame(root, text="View Student")
        self.view_frame.grid(row=2, column=0, padx=10, pady=10)

        tk.Label(self.view_frame, text="Roll Number:").grid(row=0, column=0)
        self.view_roll_entry = tk.Entry(self.view_frame)
        self.view_roll_entry.grid(row=0, column=1)

        tk.Button(self.view_frame, text="View Details", command=self.view_student).grid(row=1, column=0, columnspan=2, pady=5)

    def add_student(self):
        name = self.name_entry.get().strip()
        roll_number = self.roll_entry.get().strip()

        if not name or not roll_number:
            messagebox.showerror("Error", "Please enter all details.")
            return

        if self.system.add_student(name, roll_number):
            messagebox.showinfo("Success", "Student added successfully!")
        else:
            messagebox.showerror("Error", "Student already exists.")
        
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)

    def add_marks(self):
        roll_number = self.marks_roll_entry.get().strip()
        subject = self.subject_entry.get().strip()
        marks = self.marks_entry.get().strip()

        if not roll_number or not subject or not marks:
            messagebox.showerror("Error", "Please enter all details.")
            return

        if self.system.add_marks(roll_number, subject, marks):
            messagebox.showinfo("Success", "Marks added successfully!")
        else:
            messagebox.showerror("Error", "Invalid data or student not found.")
        
        self.marks_roll_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    def view_student(self):
        roll_number = self.view_roll_entry.get().strip()
        
        student = self.system.view_student(roll_number)
        if student is None:
            messagebox.showerror("Error", "Student not found.")
        else:
            details = f"Name: {student.name}\nRoll Number: {student.roll_number}\nMarks:\n"
            for subject, mark in student.marks.items():
                details += f"  {subject}: {mark}\n"
            details += f"Grade: {student.calculate_grade()}"
            messagebox.showinfo("Student Details", details)
        
        self.view_roll_entry.delete(0, tk.END)

# Initialize the application
if __name__ == "__main__":
    root = tk.Tk()
    system = StudentGradeManagementSystem()
    app = StudentGradeManagementApp(root, system)
    root.mainloop()
