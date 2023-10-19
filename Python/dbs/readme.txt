How to launch the api through venv:

cd Python
py -3 -m venv venv
venv\Scripts\activate
$env:FLASK_APP = "appName.py"
$env:FLASK_ENV = "development"
flask run