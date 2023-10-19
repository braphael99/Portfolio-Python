import sqlite3
from sqlite3 import Error

def create_tables(conn):
    create_family_table = """ 
        CREATE TABLE IF NOT EXISTS FamilyMembers (
            id INTEGER PRIMARY KEY,
            first TEXT,
            last TEXT,
            dob TEXT
        );
    """
    cursor = conn.cursor()
    cursor.execute(create_family_table)
    conn.commit()

def insert_famMember(conn, first, last, dob):
    insert_student_sql = """
        INSERT INTO FamilyMembers (first, last, dob) VALUES (?, ?, ?);
    """

    cursor = conn.cursor()
    cursor.execute(insert_student_sql, (first, last, dob))
    conn.commit()

    return cursor.lastrowid

def display_famAlphabetically(conn):
    display_famAlphabetically_sql = """
        SELECT first, last FROM FamilyMembers ORDER BY last, first;
    """

    cursor = conn.cursor()
    cursor.execute(display_famAlphabetically_sql)
        
    rows = cursor.fetchall()
    for row in rows:
        for columnName in row.keys():
            print(f"Column: {columnName} Value: {row[columnName]}")
        print()

def display_famAge(conn):
    display_famAge_sql = """
        SELECT first, last, dob FROM FamilyMembers ORDER BY dob;
    """

    cursor = conn.cursor()
    cursor.execute(display_famAge_sql)
    
    rows = cursor.fetchall()
    for row in rows:
        for columnName in row.keys():
            print(f"Column: {columnName} Value: {row[columnName]}")
        print()

def main():
    conn = None
    firstName = ""
    lastName = ""
    dob = ""
    select = ""
    try:
        conn = sqlite3.connect("./dbs/familyMembers.db")
        conn.row_factory = sqlite3.Row

        create_tables(conn)

        while select != "q":
            select = input("i for insert, a for displaying alphabetically, b for displaying by age, q for quit: ")

            if select == "i":
                firstName = input("Please enter a first name: ")
                lastName = input("Please enter a last name: ")
                dob = input("Please enter a birthdate in YYYY-MM-DD format: ")
                tempID = insert_famMember(conn, firstName, lastName, dob)
            elif select == "a":
                display_famAlphabetically(conn)
            elif select == "b":
                display_famAge(conn)
            elif select == "q":
                print("Quitting...")
            else:
                print("Please select a valid character...")

    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()
