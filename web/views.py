from flask import render_template
from app import app
from app import db

@app.route('/')
def homepage():
    return render_template('home.html')
