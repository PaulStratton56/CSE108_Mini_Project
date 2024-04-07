from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():    
    return redirect(url_for("login"))

@app.route("/student/myClasses")
def studentMyClasses():
    return render_template("studentMyClasses.html")

@app.route("/student/allClasses")
def studentAllClasses():
    return render_template("studentAllClasses.html")

@app.route("/teacher/myClasses")
def teacherMyClasses():
    return render_template("teacherMyClasses.html")

@app.route("/teacher/class/students")
def teacherStudents():
    return render_template("teacherStudents.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()