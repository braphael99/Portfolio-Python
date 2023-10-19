import sqlite3
from sqlite3 import Error

from flask import Flask
from flask import abort
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route("/persons/new", methods = ["POST"])
def newPersons():
    newPerson= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        firstName = jsonPostData["firstName"]
        lastName = jsonPostData["lastName"]
        phoneNumber = jsonPostData["phoneNumber"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO Persons (firstName, lastName, phoneNumber) VALUES (?, ?, ?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (firstName, lastName, phoneNumber))
        conn.commit()
        conn.close()
        return redirect(f"/persons")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/tests/new", methods = ["POST"])
def newTests():
    newTest= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        name = jsonPostData["name"]
        diseaseName = jsonPostData["diseaseName"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO Tests (name, diseaseName) VALUES (?, ?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (name, diseaseName))
        conn.commit()
        conn.close()
        return redirect(f"/tests")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/symptoms/new", methods = ["POST"])
def newSymptoms():
    newSymptom= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        description = jsonPostData["description"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO Symptoms (description) VALUES (?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (description, ))
        conn.commit()
        conn.close()
        return redirect(f"/symptoms")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/interactions/new", methods = ["POST"])
def newInteractions():
    newInteraction= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        timestamp = jsonPostData["timestamp"]
        contactOneID = jsonPostData["contactOneID"]
        contactTwoID = jsonPostData["contactTwoID"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO Interactions (timestamp, contactOneID, contactTwoID) VALUES (?,?,?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (timestamp, contactOneID, contactTwoID))
        conn.commit()
        conn.close()
        return redirect(f"/interactions")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/symptomoccurences/new", methods = ["POST"])
def newOccurences():
    newOccurence= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        timestamp = jsonPostData["timestamp"]
        personID = jsonPostData["personID"]
        symptomID = jsonPostData["symptomID"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO SymptomOccurences (timestamp, personID, symptomID) VALUES (?,?,?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (timestamp, personID, symptomID))
        conn.commit()
        conn.close()
        return redirect(f"/symptomoccurences")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/testresults/new", methods = ["POST"])
def newTestResults():
    newResult= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        timestamp = jsonPostData["timestamp"]
        result = jsonPostData["result"]
        personID = jsonPostData["personID"]
        testID = jsonPostData["testID"]
        
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO TestResults (timestamp, result, personID, testID) VALUES (?,?,?,?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (timestamp, result, personID, testID))
        conn.commit()
        conn.close()
        return redirect(f"/testresults")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/persons")
def getPersons():
    persons = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Persons.id, Persons.firstName, Persons.lastName, Persons.phoneNumber
            FROM Persons
            ORDER BY Persons.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            person = {"id": row["id"], "firstName": row["firstName"], "lastName": row["lastName"], "phoneNumber": row["phoneNumber"]}
            persons.append(person)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"persons": persons}

@app.route("/testresults/<diseaseName>/<int:days>")
def testResultWithinTime(diseaseName, days):
    result = {"count": ""}
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT COUNT(Persons.id) AS numPositives
            FROM Persons, Tests, TestResults
            WHERE Persons.id = TestResults.personID
            AND Tests.id = TestResults.testID
            AND TestResults.result = "positive"
            AND Tests.diseaseName = ?
            AND (julianday('now') - julianday(TestResults.timestamp)) <= ?

        """
        cursor = conn.cursor()
        cursor.execute(sql, (diseaseName, days))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            firstRow = True
            for row in rows:
                if(firstRow):
                    result["count"] = row["numPositives"]
                    firstRow = False

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return result

@app.route("/symptomoccurences/<int:id>/<diseaseName>")
def specificSymptoms(id, diseaseName):
    symptomDescriptions = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Symptoms.description
            FROM Persons, Tests, TestResults, Symptoms, SymptomOccurences
            WHERE Persons.id = TestResults.personID
            AND Tests.id = TestResults.testID
            AND Symptoms.id = SymptomOccurences.symptomID
            AND SymptomOccurences.personID = Persons.id
            AND TestResults.result = "positive"
            AND Persons.id = ?
            AND Tests.diseaseName = ?

        """
        cursor = conn.cursor()
        cursor.execute(sql, (id, diseaseName))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            for row in rows:
                symptomDescription = {"description": row["description"]}
                symptomDescriptions.append(symptomDescription)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"symptomDescriptions": symptomDescriptions}

@app.route("/interactions/<int:id>/<int:day>")
def interactionDetails(id, day):
    whoInteracts = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Persons.firstName, Persons.lastName
            FROM Persons
            WHERE Persons.id IN (
	            SELECT Interactions.contactTwoID
	            FROM Interactions
	            WHERE contactOneID = ?
	            AND (julianday('now') - julianday(Interactions.timestamp)) <= ?
	        )
	
            UNION

            SELECT Persons.firstName, Persons.lastName
            FROM Persons
            WHERE Persons.id IN (
	            SELECT Interactions.contactOneID
	            FROM Interactions
	            WHERE contactTwoID = ?
	            AND (julianday('now') - julianday(Interactions.timestamp)) <= ?
	        )

        """
        cursor = conn.cursor()
        cursor.execute(sql, (id, day, id, day))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            for row in rows:
                interaction = {"firstName": row["firstName"], "lastName": row["lastName"]}
                whoInteracts.append(interaction)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"Named-Interactions": whoInteracts}

@app.route("/interactions")
def getInteractions():
    interactions = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Interactions.id, Interactions.timestamp, Interactions.contactOneID, Interactions.contactTwoID
            FROM Interactions
            ORDER BY Interactions.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            interaction = {"id": row["id"], "timestamp": row["timestamp"], "contactOneID": row["contactOneID"], "contactTwoID": row["contactTwoID"]}
            interactions.append(interaction)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"interactions": interactions}

@app.route("/symptomoccurences")
def getSymptomOccurences():
    symptomOccurences = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT SymptomOccurences.id, SymptomOccurences.timestamp, SymptomOccurences.personID, SymptomOccurences.symptomID
            FROM SymptomOccurences
            ORDER BY SymptomOccurences.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            occurence = {"id": row["id"], "timestamp": row["timestamp"], "personID": row["personID"], "symptomID": row["symptomID"]}
            symptomOccurences.append(occurence)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"Symptom-Occurences": symptomOccurences}

@app.route("/symptoms")
def getSymptoms():
    symptoms = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Symptoms.id, Symptoms.description
            FROM Symptoms
            ORDER BY Symptoms.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            symptom = {"id": row["id"], "description": row["description"]}
            symptoms.append(symptom)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"Symptoms": symptoms}

@app.route("/testresults")
def getTestResults():
    results = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT TestResults.id, TestResults.timestamp, TestResults.result, TestResults.personID, TestResults.testID
            FROM TestResults
            ORDER BY TestResults.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            testResult = {"id": row["id"], "timestamp": row["timestamp"], "result": row["result"], "personID": row["personID"], "testID": row["testID"]}
            results.append(testResult)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"TestResults": results} 

@app.route("/tests")
def getTests():
    tests = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/contactTracing.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT Tests.id, Tests.name, Tests.diseaseName
            FROM Tests
            ORDER BY Tests.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            test = {"id": row["id"], "name": row["name"], "diseaseName": row["diseaseName"]}
            tests.append(test)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"Tests": tests} 