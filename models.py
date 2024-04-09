from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Initialize the Flask application and the SQLAlchemy database.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classviewer.db'

db = SQLAlchemy(app)

admin = Admin(app, name="classviewer", template_mode="bootstrap3")
app.secret_key = 'key'

#Association table between Classes and Students (a many-to-many relationship).
#Note each association includes a student, a class, and a grade the student has in the class.
student_class_table = db.Table("student_class_table",
                                db.Column("class_id", db.Integer, db.ForeignKey("Class.id"), primary_key=True),
                                db.Column("student_id", db.Integer, db.ForeignKey("Student.id"), primary_key=True),
                                db.Column("grade", db.Integer, nullable=False)
)

'''
Class Database table. Contains:
class_id: database class id. This is the primary key.
name: the name of the class (ex. CSE 108)
time: the time the class is held (ex. MWF 2:00-2:50 PM)
max_students: the maximum occupancy of the class. An integer. (Should be greater than 0)
teacher_id: foreign key to the ID of the teacher teaching the class.
students: points to all students in the student_class_table that are associated with the class. This is an association.
'''
class Class(db.Model):
    __tablename__ = "Class"
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String, nullable=False)
    time         = db.Column(db.String, nullable=False)
    max_students = db.Column(db.Integer, nullable=False)
    teacher_id   = db.Column(db.Integer, db.ForeignKey("Teacher.id"))
    teacher      = db.relationship("Teacher", backref=db.backref("classes", lazy=True))
    students     = db.relationship("Student", secondary=student_class_table, lazy="subquery")
admin.add_view(ModelView(Class, db.session))

'''
Student Database table. Contains:
student_id: database student id. This is the primary key.
name: the name of the student (ex. Chuck Norris)
password: the password of the student. Should be used with Flask's 'Login' system.
classes: points to all classes in the student_class_table that the student is enrolled in. This is an association.
'''
class Student(UserMixin, db.Model):
    __tablename__ = "Student"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String, nullable=False)
    password   = db.Column(db.String, nullable=False) #This needs to be made more secure via Flask Login
    classes    = db.relationship("Class", secondary=student_class_table, overlaps="students", lazy="subquery")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

admin.add_view(ModelView(Student, db.session))

'''
Teacher Database table. Contains:
teacher_id: database teacher id. This is the primary key.
name: the name of the teacher (ex. Ammon Hepworth)
password: the password of the teacher. Should be used with Flask's 'Login' system.
'''
class Teacher(UserMixin, db.Model):
    __tablename__ = "Teacher"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String, nullable=False)
    password   = db.Column(db.String, nullable=False) #This needs to be made more secure via Flask Login

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

admin.add_view(ModelView(Teacher, db.session))

#Ensures the correct file is run.
if __name__ == "__main__":
    print("Wrong file! Please run 'main.py'.")