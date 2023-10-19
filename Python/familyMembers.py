import sqlite3
from sqlite3 import Error

from flask import Flask
from flask import abort
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route("/family-members")
def getFamilyMembers():
    familyMems = []
    conn = None
    try:
        conn = sqlite3.connect("./dbs/familyMembers.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT FamilyMembers.id, FamilyMembers.first, FamilyMembers.last
            FROM FamilyMembers
            ORDER BY FamilyMembers.id
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  
        for row in rows:
            familyMem = {"id": row["id"], "first": row["first"], "last": row["last"]}
            familyMems.append(familyMem)

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return {"family-members": familyMems}

@app.route("/family-members/<int:id>")
def familyMemID(id):
    family = {"id": "", "first": "", "last": ""}
    conn = None
    try:
        conn = sqlite3.connect("./dbs/familyMembers.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            SELECT FamilyMembers.id, FamilyMembers.first, FamilyMembers.last
            FROM FamilyMembers
            WHERE FamilyMembers.id = ?

        """
        cursor = conn.cursor()
        cursor.execute(sql, (id, ))
        rows = cursor.fetchall()  

        if(len(rows) == 0):
            abort(404)
        else:
            firstRow = True
            for row in rows:
                if(firstRow):
                    family["id"] = row["id"]
                    family["first"] = row["first"]
                    family["last"] = row["last"]
                    firstRow = False

    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

    return family

@app.route("/family-members/new", methods = ["POST"])
def addFamily():
    newFamilyMem= {}
    conn = None
    try:
        jsonPostData = request.get_json()
        first = jsonPostData["first"]
        last = jsonPostData["last"]
        
        conn = sqlite3.connect("./dbs/familyMembers.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            INSERT INTO FamilyMembers (first, last) VALUES (?, ?)    
        """
        cursor = conn.cursor()
        cursor.execute(sql, (first, last))
        conn.commit()
        conn.close()
        return redirect(f"/family-members")
    except Error as e:
        print(f"Error opening the database {e}")
        abort(500)
    finally:
        if conn:
            conn.close()

@app.route("/family-members/<int:id>", methods = ["DELETE"])
def deleteFamilyMem(id):
    family = {"id": "", "first": "", "last": ""}
    conn = None
    try:
        conn = sqlite3.connect("./dbs/familyMembers.db")
        conn.row_factory = sqlite3.Row
        sql = """ 
            DELETE FROM FamilyMembers WHERE FamilyMembers.id = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id, ))
        conn.commit()
        conn.close() 
        abort(204)
    except Error as e:
        print(f"Error opening the database {e}")
        abort(404)