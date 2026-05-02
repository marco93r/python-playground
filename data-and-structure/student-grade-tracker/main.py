class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average(self):
        overall = 0
        for g in self.grades:
            overall += g

        average = overall / len(self.grades)
        return average
    
    def get_best(self):
        return max(self.grades)

    def get_worst(self):
        return min(self.grades)
    
    def __repr__(self):
        return self.name

def print_menu():
        print("=== Grade Tracker ===")
        print("1. Add student")
        print("2. Add grade")
        print("3. Show student stats")
        print("4. Quit")

def main():
    students = []
    user_input = ''
    while user_input != '4':

        print_menu()
        user_input = input("Choose: ")

        if user_input == '1':
            s = Student(input("Student name: "))
            students.append(s)

        elif user_input == '2':
            print(students)
            s = input("Enter student to add grade to: ")
            grade = input("Enter grade: ")
            for student in students:
                if student.name == s:
                    student.add_grade(int(grade))
                    break
            else:
                print('Student not found!')

        elif user_input == '3':
            s = input("Enter student to show stats from: ")
            for student in students:
                if student.name == s:
                    print('Average:', student.get_average())
                    print('Best grade:', student.get_best())
                    print('Worst grade:', student.get_worst())
                    break
            else:
                print('Student not found!')

        elif user_input == '4':
            print('Quitting...')

        else:
            print("not a valid option! - try again")

main()