from models import *

def getStudent(username):
    return Student.query.filter_by(name=username).first()

def getStudentClasses(student):
    enrollments = Enrollment.query.filter_by(student_id = student.id).all()
    return [enrollment.enrolledClass for enrollment in enrollments]

def getClassStudents(aClass):
    enrollments = Enrollment.query.filter_by(class_id = aClass.id).all()
    return [enrollment.student for enrollment in enrollments]

def getTeacher(username = None):
    if username == None:
        return Teacher.query.first()
    elif type(username) == str:
        return Teacher.query.filter_by(name=username).first()
    elif type(username) == int:
        return Teacher.query.filter_by(id=username).first()

def getTeacherName(teacher_id):
    return Teacher.query.filter_by(id=teacher_id).first().name

def getTeacherClasses(teacher):
    return Class.query.filter_by(teacher_id=teacher.id).all()

def getClass(className = None):
    if className == None:
        return Class.query.first()
    elif type(className) == str:
        return Class.query.filter_by(name=className).first()
    elif type(className) == int:
        return Class.query.filter_by(id=className).first()

def getStudentGrade(student, givenClass):
    enrollment = Enrollment.query.filter_by(student_id = student.id, class_id = givenClass.id).first()
    if enrollment:
        return enrollment.grade

def enrolled(student, studentClass):
    enrollment = Enrollment.query.filter_by(student_id = student.id, class_id = studentClass.id).first()
    if enrollment:
        return True
    return False

def getStudent(username = None):
    if username == None:
        return Student.query.first()
    elif type(username) == str:
        return Student.query.filter_by(name=username).first()
    elif type(username) == int:
        return Student.query.filter_by(id=username).first()

def getNumberOfEnrolledStudents(givenClass):
    students = getClassStudents(givenClass)
    return len(students)
