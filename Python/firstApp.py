import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return f"Welcome to my app! This code is running from: {__name__}"

@app.route("/helloworld")
def hw():
    return "Hello World!!!!"

@app.route("/anotherRoute")
def anotherRoute():
    return "Here is another route"

@app.route("/csstudent/<name>")
def showStudentName(name):
    return f"Hello {name}, you are a fine Computer Science student!"

@app.route("/csstudent/<firstName>/<lastName>")
def showStudentFullName(firstName, lastName):
    return f"Hello {firstName} {lastName}, you are a fine Computer Science student!"

@app.route("/csstudent/<name>/birthyear/<int:birthyear>")
def showStudentNameAndAge(name, birthyear):
    age = datetime.date.today().year - birthyear
    return f"{name}, born {age} years ago, is a fine CS student!"