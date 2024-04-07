from flask import Flask, render_template, request, redirect, url_for
from models import *
from helperFunctions import *
import json

CONFIRM_COLOR = "green"
ERROR_COLOR = "red"
NONE_COLOR = "black"

#Home page routing - right now nothing, but we should consider moving the login page here (so it's the first thing they see).
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/student/<student_id>/myClasses")
def studentMyClasses(student_id):
    student = getStudent(int(student_id))
    classes = getStudentClasses(student)
    return render_template("studentMyClasses.html", classes = classes, student = student, getTeacherName = getTeacherName, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents)

@app.route("/student/<student_id>/allClasses")
def studentAllClasses(student_id):
    student = getStudent(int(student_id))
    classes = Class.query.all()
    return render_template("studentAllClasses.html", classes = classes, student = student, getTeacherName = getTeacherName, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents, enrolled = enrolled)

@app.route("/teacher/<teacher_id>/myClasses")
def teacherMyClasses(teacher_id):
    teacher = getTeacher(int(teacher_id))
    classes = getTeacherClasses(teacher)
    return render_template("teacherMyClasses.html", classes = classes, teacher = teacher, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents)

@app.route("/teacher/<teacher_id>/class/<class_id>/students")
def teacherStudents(teacher_id, class_id):
    teacher = getTeacher(int(teacher_id))
    currentClass = getClass(int(class_id))
    students = getClassStudents(currentClass)
    return render_template("teacherStudents.html", students = students, currentClass = currentClass, teacher = teacher, getStudentGrade = getStudentGrade, setGrade = setGrade)

#Login page routing - routes to Alex's login page.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message = None)
    if request.method == "POST":
        message = None
        messageColor = NONE_COLOR
        username = request.form.get('username')
        password = request.form.get('password')

        if getStudent(username) != None:
            student = getStudent(username)
            if student.password == password:
                message="Welcome, student " + student.name + "!"
                messageColor = CONFIRM_COLOR
                return redirect(url_for("studentMyClasses", student_id = getStudent(username).id))
            else:
                message="ERROR: Incorrect password. Please try again."
                messageColor = ERROR_COLOR
        elif getTeacher(username) != None:
            teacher = getTeacher(username)
            if teacher.password == password:
                message="Welcome, teacher " + teacher.name + "!"
                messageColor = CONFIRM_COLOR
                return redirect(url_for("teacherMyClasses", teacher_id = getTeacher(username).id))
            else:
                message="ERROR: Incorrect password. Please try again."
                messageColor = ERROR_COLOR
        else:
            message="ERROR: No user found by the name of " + username + ". Please try again."
            messageColor = ERROR_COLOR
        return render_template("login.html", message = message, messageColor = messageColor)

@app.route("/setGrade/<student_id>/<class_id>", methods=["POST"])
def setGrade(student_id, class_id):
    enrollment = db.session.query(student_class_table).filter_by(student_id=student_id, class_id=class_id).first()
    newGrade = int(json.loads(request.data)["grade"])
    if enrollment:
        currentGrade = enrollment.grade
        print("Student is enrolled! Changing grade from " + str(currentGrade) + " to " + str(newGrade))
    return "Success"

@app.route("/debug", methods=["GET"])
def debug():
    class3 = Class.query.filter_by(name = "BIO").first()
    class3.max_students = 2
    class3.teacher_id = getTeacher().id
    db.session.commit()
    return render_template("login.html", message = "Debug completed.", messageColor = 'green')

#Initialize the database tables for the application's use.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()