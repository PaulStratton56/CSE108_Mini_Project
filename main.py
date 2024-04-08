from flask import Flask, render_template
from models import app, db

#Home page routing - right now nothing, but we should consider moving the login page here (so it's the first thing they see).
@app.route("/")
def index():    
    return render_template("index.html")

#Login page routing - routes to Alex's login page.
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/teacher")
def teacherView():
    return render_template("teacherView.html")
@app.route("/course")
def courseView():
    return render_template("courseRosterTeacher.html")
@app.route("/student")
def studentView():
    return render_template("studentview.html")

#Initialize the database tables for the application's use.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()