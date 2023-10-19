from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return f"Welcome to my app! This code is running from: {__name__}"
