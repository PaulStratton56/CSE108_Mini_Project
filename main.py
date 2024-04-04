from flask import Flask, render_template, request, redirect, url_for
from models import *

CONFIRM_COLOR = "green"
ERROR_COLOR = "red"
NONE_COLOR = "black"

#Home page routing - right now nothing, but we should consider moving the login page here (so it's the first thing they see).
@app.route("/")
def index():    
    return render_template("index.html")

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
            else:
                message="ERROR: Incorrect password. Please try again."
                messageColor = ERROR_COLOR
        elif getTeacher(username) != None:
            teacher = getTeacher(username)
            if teacher.password == password:
                message="Welcome, teacher " + teacher.name + "!"
                messageColor = CONFIRM_COLOR
            else:
                message="ERROR: Incorrect password. Please try again."
                messageColor = ERROR_COLOR
        else:
            message="ERROR: No user found by the name of " + username + ". Please try again."
            messageColor = ERROR_COLOR
        return render_template("login.html", message = message, messageColor = messageColor)

def getStudent(username):
    return Student.query.filter_by(name=username).first()

def getTeacher(username):
    return Teacher.query.filter_by(name=username).first()

#Initialize the database tables for the application's use.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()