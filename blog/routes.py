from flask import Flask, render_template, url_for, request
from blog import app

#app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")