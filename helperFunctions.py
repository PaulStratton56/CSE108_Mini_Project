from models import *

def getStudent(username):
    return Student.query.filter_by(name=username).first()

def getStudentClasses(student):
    return Class.query.join(student_class_table).filter_by(student_id = student.id).all()

def getClassStudents(aClass):
    return Student.query.join(student_class_table).filter_by(class_id = aClass.id).all()

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
    grade = db.session.query(student_class_table.c.grade).filter_by(student_id=student.id, class_id=givenClass.id).scalar()
    return grade

def enrolled(student, studentClass):
    if len(Class.query.join(student_class_table).filter_by(class_id = studentClass.id, student_id = student.id).all()) != 0:
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
