import sqlite3
from sqlite3 import Error

from flask import Flask
from flask import abort
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route("/cslegends")
def getLegends():
    legends = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName 
            FROM CSLegends
            ORDER BY CSLegends.lastName, CSLegends.firstName
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            legend = {"id": row["id"], "firstName": row["firstName"], "lastName": row["lastName"]}
            legends.append(legend)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"legends": legends}

@app.route("/cslegends/living")
def getLivingLegends():
    livingLegends = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName 
            FROM CSLegends
            WHERE CSLegends.death = ''
            ORDER BY CSLegends.lastName, CSLegends.firstName
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            legend = {"id": row["id"], "firstName": row["firstName"], "lastName": row["lastName"]}
            livingLegends.append(legend)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"livingLegends": livingLegends}

@app.route("/cslegends/<int:legendId>")
def legendById(legendId):
    legend = {"id": "", "firstName": "", "lastName": "", "accomplishments": []}
    conn = None
    try:
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName, Accomplishments.description 
            FROM CSLegends, Accomplishments
            WHERE CSLegends.id = Accomplishments.legendId
            AND CSLegends.id = ?
            ORDER BY CSLegends.lastName, CSLegends.firstName
        """
        cursor = conn.cursor()
        cursor.execute(sql, (legendId, ))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            firstRow = True
            for row in rows:
                if(firstRow):
                    legend["id"] = row["id"]
                    legend["firstName"] = row["firstName"]
                    legend["lastName"] = row["lastName"]
                    firstRow = False
                legend["accomplishments"].append(row["description"])

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return legend

@app.route("/cslegends/search/<name>")
def legendByName(name):
    legend = {"id": "", "firstName": "", "lastName": "", "accomplishments": []}
    conn = None
    try:
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName, Accomplishments.description 
            FROM CSLegends, Accomplishments
            WHERE CSLegends.id = Accomplishments.legendId
            AND (CSLegends.lastName = ? COLLATE NOCASE
            OR CSLegends.firstName = ? COLLATE NOCASE)
            ORDER BY CSLegends.lastName, CSLegends.firstName
        """
        cursor = conn.cursor()
        cursor.execute(sql, (name, name))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            firstRow = True
            for row in rows:
                if(firstRow):
                    legend["id"] = row["id"]
                    legend["firstName"] = row["firstName"]
                    legend["lastName"] = row["lastName"]
                    firstRow = False
                legend["accomplishments"].append(row["description"])

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return legend

@app.route("/cslegends/born/between/<int:startYear>/and/<int:endYear>")
def getLegendsBornInTimeframe(startYear, endYear):
    legends = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName
            FROM CSLegends
            WHERE date(CSLegends.birth) >= date(?)
            AND date(CSLegends.birth) <= date(?)
            ORDER BY CSLegends.lastName, CSLegends.firstName
        """
        cursor = conn.cursor()
        cursor.execute(sql, (f"{startYear}-01-01", f"{endYear}-12-31"))
        rows = cursor.fetchall()  

        for row in rows:
            legends.append({"id": row["id"], "firstName": row["firstName"], "lastName": row["lastName"]})

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"legends": legends}

@app.route("/cslegends/new", methods = ["POST"])
def addLegend():
    newLegend= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        firstName = jsonPostData["firstName"]
        lastName = jsonPostData["lastName"]
        birth = jsonPostData["birth"]
        death = jsonPostData["death"]
        
        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO CSLegends (firstName, lastName, birth, death) VALUES (?, ?, ?, ?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (firstName, lastName, birth, death))
        conn.commit()
        sql = """
            SELECT CSLegends.id, CSLegends.firstName, CSLegends.lastName, CSLegends.birth, CSLegends.death
            FROM CSLegends
            WHERE CSLegends.id = ?
        """
        cursor.execute(sql, (cursor.lastrowid,))
        row = cursor.fetchone()
        newLegend["id"] = row["id"]
        newLegend["firstName"] = row["firstName"]
        newLegend["lastName"] = row["lastName"]
        newLegend["birth"] = row["birth"]
        newLegend["death"] = row["death"]
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return newLegend

@app.route("/cslegends/<int:legendId>/accomplishment/new", methods = ["POST"])
def updateLegend(legendId):
    conn = None
    try:
        jsonPostData = request.get_json()
        accomplishment = jsonPostData["accomplishment"]

        conn = sqlite3.connect("./dbs/csLegends.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO Accomplishments (description, legendId) VALUES (?, ?)  
        """
        cursor = conn.cursor()
        cursor.execute(sql, (accomplishment, legendId))
        conn.commit()
        conn.close()
        return redirect(f"/cslegends/{legendId}")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()