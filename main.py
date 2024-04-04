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

#Initialize the database tables for the application's use.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()