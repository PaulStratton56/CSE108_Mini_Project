from flask import Flask, render_template, request, redirect, url_for
from models import *
from helperFunctions import *
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

CONFIRM_COLOR = "green"
ERROR_COLOR = "red"
NONE_COLOR = "black"

login_manager = LoginManager()
login_manager.init_app(app) # getting a squiggly here but app should be imported from models -- check this
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(user_id) or Teacher.query.get(user_id)


#Home page routing - right now nothing, but we should consider moving the login page here (so it's the first thing they see).
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/student/<student_id>/myClasses")
@login_required
def studentMyClasses(student_id):
    student = getStudent(int(student_id))
    classes = getStudentClasses(student)
    return render_template("studentMyClasses.html", classes = classes, student = student, getTeacherName = getTeacherName, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents)

@app.route("/student/<student_id>/allClasses")
@login_required
def studentAllClasses(student_id):
    student = getStudent(int(student_id))
    classes = Class.query.all()
    return render_template("studentAllClasses.html", classes = classes, student = student, getTeacherName = getTeacherName, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents, enrolled = enrolled)

@app.route("/teacher/<teacher_id>/myClasses")
@login_required
def teacherMyClasses(teacher_id):
    teacher = getTeacher(int(teacher_id))
    classes = getTeacherClasses(teacher)
    return render_template("teacherView.html", classes = classes, teacher = teacher, getNumberOfEnrolledStudents = getNumberOfEnrolledStudents)

@app.route("/teacher/<teacher_id>/class/<class_id>/students")
@login_required
def teacherStudents(teacher_id, class_id):
    teacher = getTeacher(int(teacher_id))
    currentClass = getClass(int(class_id))
    students = getClassStudents(currentClass)
    return render_template("courseRosterTeacher.html", students = students, currentClass = currentClass, teacher = teacher, getStudentGrade = getStudentGrade, setGrade = setGrade)

#Login page routing - routes to Alex's login page.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        message = None
        messageColor = NONE_COLOR
        username = request.form.get('username')
        password = request.form.get('password')

        if username.upper() == "Admin".upper() and password == "Password":
            return redirect('/admin')
        
        
        user = Student.query.filter_by(name=username).first() or Teacher.query.filter_by(name=username).first()

        if user and user.check_password(password):
            login_user(user)
        
            if isinstance(user, Student):
                message="Welcome, student " + student.name + "!"
                messageColor = CONFIRM_COLOR
                return redirect(url_for('studentMyClasses', student_id=user.id))
            
            elif isinstance(user, Teacher):
                message="Welcome, teacher " + teacher.name + "!"
                messageColor = CONFIRM_COLOR
                return redirect(url_for('teacherMyClasses', teacher_id=user.id))
            
            else:
                message = "ERROR: Incorrect username or password. Please try again."
                messageColor = ERROR_COLOR

        else:
            message="ERROR: No user found by the name of " + username + ". Please try again."
            messageColor = ERROR_COLOR
        
        return render_template("login.html", message = message, messageColor = messageColor)
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/setGrade/<student_id>/<class_id>", methods=["POST"])
def setGrade(student_id, class_id):
    enrollment = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()
    newGrade = int(json.loads(request.data)["grade"])
    if enrollment:
        enrollment.grade = newGrade
        db.session.commit()
    return "Success"

@app.route("/dropClass", methods=["POST"])
def dropClass():
    requestBody = json.loads(request.data)
    enrollmentToDrop = Enrollment.query.filter_by(student_id=requestBody["student_id"], class_id=requestBody["class_id"]).first()
    if enrollmentToDrop:
        print("Found enrollment!")
        db.session.delete(enrollmentToDrop)
        db.session.commit()
    return "Success"

@app.route("/joinClass", methods=["POST"])
def joinClass():
    requestBody = json.loads(request.data)
    enrolledClass = getClass(requestBody["class_id"])
    enrolledStudent = getStudent(requestBody["student_id"])
    if getNumberOfEnrolledStudents(enrolledClass) < enrolledClass.max_students: #There's space!
        enrollment = Enrollment(class_id = enrolledClass.id, student_id = enrolledStudent.id, grade = 100)
        db.session.add(enrollment)
        db.session.commit()
    return "Success"

@app.route("/debug", methods=["GET"])
def debug():
    class3 = Class.query.filter_by(name = "BIO").first()
    class3.max_students = 2
    class3.teacher_id = getTeacher().id
    db.session.commit()
    return render_template("login.html", message = "Debug completed.", messageColor = 'green')

# @app.route("/debug", methods=["GET"])
# def debug():
#     enrollments = Enrollment.query.all()
#     students = Student.query.all()
#     teachers = Teacher.query.all()
#     classes = Class.query.all()

#     enrollments[0].student_id = students[0].id
#     enrollments[1].student_id = students[1].id
#     enrollments[2].student_id = students[2].id
#     enrollments[3].student_id = students[1].id
#     enrollments[4].student_id = students[2].id
#     enrollments[5].student_id = students[0].id
    
#     enrollments[0].class_id = classes[0].id
#     enrollments[1].class_id = classes[0].id
#     enrollments[2].class_id = classes[1].id
#     enrollments[3].class_id = classes[1].id
#     enrollments[4].class_id = classes[2].id
#     enrollments[5].class_id = classes[2].id

#     classes[0].teacher_id = teachers[0].id
#     classes[1].teacher_id = teachers[1].id
#     classes[2].teacher_id = teachers[2].id

#     db.session.commit()

#     return render_template("login.html", message = "Debug complete.", messageColor = "green")

@app.route("/teacher")
def teacherView():
    return render_template("teacherView.html")
@app.route("/course")
def courseView():
    return render_template("courseRosterTeacher.html")
@app.route("/student")
def studentView():
    return render_template("studentview.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Initialize the database tables for the application's use.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()