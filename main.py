from flask import Flask, render_template
from models import app, db

@app.route("/")
def index():    
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()