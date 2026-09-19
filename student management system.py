# Student Information & Academic Records Manager (Console App)

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Student:
    student_id: str
    name: str
    major: str
    email: str
    courses: Dict[str, List[float]] = field(default_factory=dict)

    def add_grade(self, course: str, grade: float) -> None:
        self.courses.setdefault(course, []).append(grade)

    def course_average(self, course: str) -> float | None:
        if course not in self.courses or not self.courses[course]:
            return None
        grades = self.courses[course]
        return sum(grades) / len(grades)

    def overall_average(self) -> float | None:
        all_grades = [g for grades in self.courses.values() for g in grades]
        if not all_grades:
            return None
        return sum(all_grades) / len(all_grades)


class StudentManager:
    def init(self):
        self.students: Dict[str, Student] = {}

    def add_student(self) -> None:
        sid = input("Student ID: ").strip()
        if sid in self.students:
            print("Student ID already exists.")
            return

        name = input("Name: ").strip()
        major = input("Major: ").strip()
        email = input("Email: ").strip()

        self.students[sid] = Student(student_id=sid, name=name, major=major, email=email)
        print("Student added successfully.")

    def update_student(self) -> None:
        sid = input("Enter Student ID to update: ").strip()
        student = self.students.get(sid)
        if not student:
            print("Student not found.")
            return

        print("Leave fields blank to keep current values.")
        new_name = input(f"Name [{student.name}]: ").strip()
        new_major = input(f"Major [{student.major}]: ").strip()
        new_email = input(f"Email [{student.email}]: ").strip()

        if new_name:
            student.name = new_name
        if new_major:
            student.major = new_major
        if new_email:
            student.email = new_email

        print("Student updated successfully.")

    def remove_student(self) -> None:
        sid = input("Enter Student ID to remove: ").strip()
        if sid in self.students:
            del self.students[sid]
            print("Student removed successfully.")
        else:
            print("Student not found.")

    def add_grade(self) -> None:
        sid = input("Enter Student ID: ").strip()
        student = self.students.get(sid)
        if not student:
            print("Student not found.")
            return

        course = input("Course name (e.g., Math 101): ").strip()
        try:
            grade = float(input("Grade (0-100): ").strip())
        except ValueError:
            print("Invalid grade. Use a number like 88.5")
            return

        if not (0 <= grade <= 100):
            print("Grade must be between 0 and 100.")
            return

        student.add_grade(course, grade)
        print("Grade added.")

    def view_student(self) -> None:
        sid = input("Enter Student ID to view: ").strip()
        student = self.students.get(sid)
        if not student:
            print("Student not found.")
            return

        print("\n--- Student Details ---")
        print(f"ID   : {student.student_id}")
        print(f"Name : {student.name}")
        print(f"Major: {student.major}")
        print(f"Email: {student.email}")

        print("\n--- Academic Records ---")
        if not student.courses:
            print("No courses/grades yet.")
        else:
            for course, grades in student.courses.items():
                avg = student.course_average(course)
                grades_str = ", ".join(f"{g:.2f}" for g in grades)
                print(f"{course}: Grades [{grades_str}] | Average: {avg:.2f}")

        overall = student.overall_average()
        if overall is None:
            print("\nOverall Average: N/A")
        else:
            print(f"\nOverall Average: {overall:.2f}")

    def list_students(self) -> None:
        if not self.students:
            print("No students in the system.")
            return

        print("\n--- All Students ---")
        for sid, s in self.students.items():
            overall = s.overall_average()
            overall_text = "N/A" if overall is None else f"{overall:.2f}"
            print(f"{sid} | {s.name} | {s.major} | Overall Avg: {overall_text}")

    def run(self) -> None:
        while True:
            print("\n" + "=" * 40)
            print("Student Manager - Menu")
            print("1. Add Student")
            print("2. Update Student Info")
            print("3. Add Grade (Academic Record)")
            print("4. View Student")
            print("5. List All Students")
            print("6. Remove Student")
            print("0. Exit")
            print("=" * 40)

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.update_student()
            elif choice == "3":
                self.add_grade()
            elif choice == "4":
                self.view_student()
            elif choice == "5":
                self.list_students()
            elif choice == "6":
                self.remove_student()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")


if name == "main":
    StudentManager().run()