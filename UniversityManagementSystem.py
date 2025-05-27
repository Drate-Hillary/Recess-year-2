from typing import List, Dict

class Person:
    def __init__(self, name: str, id_number: str):
        self.name = name
        self.id_number = id_number

    def display_info(self)-> str:
        return f"Name: {self.name}, \nID: {self.id_number}"
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "id_number": self.id_number}
    

class Contactable:
    def __init__(self, email: str, phone: str):
        self.email = email
        self.phone = phone

    def display_info(self) -> str:
        return f"Email: {self.email}, \nPhone Number: {self.phone}"
    

class Student(Person, Contactable):
    def __init__(self, name: str, id_number:str, major: str, year: int, email: str, phone: str):
        Person.__init__(self, name, id_number)
        Contactable.__init__(self, email, phone)
        self.major = major
        self.year = year
        self.courses: List[str] = []
        self.grades: Dict[str, str] = {}

    def enroll_course(self, course: str) -> str:
        if course in self.courses:
            return f"{self.name} is already enrolled in {course}"
        self.courses.append(course)
        return f"{self.name} successfully enrolled in {course}"
    
    def receive_grade(self, course: str, grade: str) -> str:
        if course not in self.courses:
            return f"{self.name} is not enrolled in {course}"
        self.grades[course] = grade
        return f"Grade {grade} assigned to {self.name} for {course}"
    
    def display_info(self) -> str:
        person_info = super().display_info()
        contact_info = Contactable.display_info(self)
        courses_info = f"Courses: {', '.join(self.courses) if self.courses else 'None'}"
        grade_info = f"Grades: {self.grades if self.grades else 'None'}"
        return f"Student: \n{person_info} \n{contact_info} \nMajor: {self.major} \nYear: {self.year} \n{courses_info} \n{grade_info}"
    
    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({"type": "Student", "major": self.major, "year": self.year, "courses": self.courses, "grades": self.grades, "email": self.email, "phone": self.phone})
        return base
    

class Lecturer(Person, Contactable):
    def __init__(self, name: str, id_number: str, department: str, subject: str, email: str, phone: str):
        Person.__init__(self, name, id_number)
        Contactable.__init__(self, email, phone)
        self.department = department
        self.subject = subject
        self.courses_taught: List[str] = []

    def assign_course(self, course: str):
        if course in self.courses_taught:
            return f"{self.name} is already teaching {course}"
        self.courses_taught.append(course)
        return f"{self.name} is now teaching {course}"
    
    def assign_grade(self, student: 'Student', course: str, grade: str) -> str:
        if course not in self.courses_taught:
            return f"{self.name} does not teach {course}"
        return student.receive_grade(course, grade)
    
    def display_info(self) -> str:
        person_info = super().display_info()
        contact_info = Contactable.display_info(self)
        courses_info = f"Courses taught: {', '.join(self.courses_taught) if self.courses_taught else 'None'}"

        return f"\nLecturer \n{person_info} \n{contact_info} \nDepartment: {self.department} \nSubject: {self.subject} \n{courses_info}"
    
    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({"type": "Lecturer", "department": self.department, "subject": self.subject, "courses_taught": self.courses_taught, "email": self.email, "phone": self.phone})
        return base
    

class Admin(Person):
    def __init__(self, name: str, id_number: str, role: str, department: str):
        super().__init__(name, id_number)
        self.role = role
        self.department = department
        self.tasks: List[str] = []

    def add_task(self, task: str) -> str:
        self.tasks.append(task)
        return f"Task {task} assigned to {self.name}"
    
    def display_info(self) -> str:
        tasks_info = f"Tasks: {', '.join(self.tasks) if self.tasks else 'None'}"

        return f"\nStaff \n{super().display_info()} \nRole: {self.role} \nDepartment: {self.department} \n{tasks_info}"
    
    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({"type": "Admin", "role": self.role, "department": self.department, "task": self.tasks})
        return base
    

class UniversitySystem:
    def __init__(self):
        self.students: List[Student] = []
        self.lecturers: List[Lecturer] = []
        self.admin: List[Admin] = []

    def add_person(self, person: Person) -> str:
        if isinstance(person, Student):
            if any(student.id_number == person.id_number for student in self.students):
                return f"ID: {person.id_number} already exists in students"
            self.students.append(person)
            return f"{person.name} has been added as a student"
        
        elif isinstance(person, Lecturer):
            if any(lecturer.id_number == person.id_number for lecturer in self.lecturers):
                return f"ID: {person.id_number} already exists in lecturers"
            self.lecturers.append(person)
            return f"{person.name} has been added as a lecturer"
        
        elif isinstance(person, Admin):
            if any(admin.id_number == person.id_number for admin in self.admin):
                return f"ID: {person.id_number} already exists in Admin"
            self.admin.append(person)
            return f"{person.name} has been added as an admin"
        
        return "Unauthenticated person type"

    def find_Person(self, id_number: str) -> str:
        for student in self.students:
            if student.id_number == id_number:
                return student.display_info()
        
        for lecturer in self.lecturers:
            if lecturer.id_number == id_number:
                return lecturer.display_info()
            
        for admin in self.admin:
            if admin.id_number == id_number:
                return admin.display_info()
        
        return f"No person found with ID {id_number}"
    
    def display_all(self) -> None:
        if not(self.students or self.lecturers or self.admin):
            print("No people in the system")
            return
        
        print("\nAll members in the University System")
        print('-----------------------------------------')
        for student in self.students:
            print(student.display_info())
        for lecturer in self.lecturers:
            print(lecturer.display_info())
        for admin in self.admin:
            print(admin.display_info())
        

def main():
        uni = UniversitySystem()

        student = Student("Alice Johnson", "S1234", "Software Engineering", 4, "alice@university.edu", "123-456-7890")
        lecturer = Lecturer("Dr. Smith", "L98765", "Mathematics", "Calculus", "bob@university.edu", "987-654-3210")
        admin = Admin("Dave", "AD45678", "Administrator", "Admissions")

        print(uni.add_person(student))
        print(uni.add_person(lecturer))
        print(uni.add_person(admin))

        print(student.enroll_course("Calculus"))

        print(lecturer.assign_course("Calculus"))
        print(lecturer.assign_grade(student, "Calculus", "A"))

        print(admin.add_task("Schedule exams"))

        uni.display_all()

        print("\nSearching for ID: S1234") 
        print(uni.find_Person("S1234"))

    
if __name__ == "__main__":
    main()