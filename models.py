from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classviewer.db'
db = SQLAlchemy(app)

student_class_table = db.Table("student_class_table",
                                db.Column("class_id", db.Integer, primary_key=True),
                                db.Column("student_id", db.Integer, primary_key=True),
                                db.Column("grade", db.Integer, nullable=False)
)

class Class(db.Model):
    __tablename__ = "Class"
    class_id     = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String, nullable=False)
    time         = db.Column(db.String, nullable=False)
    max_students = db.Column(db.Integer, nullable=False)
    teacher_id   = db.relationship("Teacher", backref=db.backref("classes", lazy=True))
    students     = db.relationship("Student", secondary=student_class_table, lazy="subquery", backref=db.backref("classes", lazy=True))

class Student(db.Model):
    __tablename__ = "Student"
    student_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String, nullable=False)
    password   = db.Column(db.String, nullable=False) #This needs to be made more secure via Flask Login
    classes    = db.relationship("Class", backref=db.backref("students", lazy=True))

class Teacher(db.Model):
    __tablename__ = "Teacher"
    teacher_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String, nullable=False)
    password   = db.Column(db.String, nullable=False) #This needs to be made more secure via Flask Login

if __name__ == "__main__":
    print("Wrong file! Please run 'main.py'.")