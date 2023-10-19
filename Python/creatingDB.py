import sqlite3
from sqlite3 import Error

def create_tables(conn):
    create_students_table = """ 
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY,
            first TEXT,
            last TEXT,
            dob TEXT
        );
    """
    cursor = conn.cursor()
    cursor.execute(create_students_table)

    create_computers_table = """ 
        CREATE TABLE IF NOT EXISTS Computers (
            id INTEGER PRIMARY KEY,
            os TEXT,
            RAM REAL,
            studentId INTEGER,
            FOREIGN KEY (studentId) REFERENCES Students(id)
        );
    """
    cursor.execute(create_computers_table)
    conn.commit()

def insert_student(conn, first, last, dob):
    insert_student_sql = """
        INSERT INTO Students (first, last, dob) VALUES (?, ?, ?);
    """

    cursor = conn.cursor()
    cursor.execute(insert_student_sql, (first, last, dob))
    conn.commit()

    return cursor.lastrowid

def update_student(conn, first, last, dob, studentId):
    update_student_sql = """
        UPDATE Students SET first = ?, last = ?, dob = ? WHERE id = ?;
    """

    cursor = conn.cursor()
    cursor.execute(update_student_sql, (first, last, dob, studentId))
    conn.commit()

    return cursor.lastrowid

def delete_student(conn, studentId):
    delete_student_sql = """
        DELETE FROM Students WHERE id = ?;
    """

    cursor = conn.cursor()
    cursor.execute(delete_student_sql, (studentId, ))
    conn.commit()

    return cursor.lastrowid

def insert_computer(conn, os, ram):
    insert_computer_sql = """
        INSERT INTO Computers (os, RAM) VALUES (?, ?);
    """

    cursor = conn.cursor()
    cursor.execute(insert_computer_sql, (os, ram))
    conn.commit()

    return cursor.lastrowid

def assign_computer_to_student(conn, studentId, computerId):
    update_computer_sql = """
        UPDATE Computers SET studentId = ? WHERE id = ?;
    """

    cursor = conn.cursor()
    cursor.execute(update_computer_sql, (studentId, computerId))
    conn.commit()

    return cursor.lastrowid

def delete_all_computers(conn):
    delete_computers_sql = """
        DELETE FROM Computers;
    """

    cursor = conn.cursor()
    cursor.execute(delete_computers_sql)
    conn.commit()

    return cursor.lastrowid

def get_all_students_and_computers(conn):
    cursor = conn.cursor()
    select_sql = """
        SELECT Students.last, Students.first, Computers.os, Computers.RAM
        FROM Students, Computers
        WHERE Students.id = Computers.studentId
    """
    rows = cursor.execute(select_sql)
    for row in rows:
        print(f"Student: {row['last']}, {row['first']} -- Computer: {row['os']} {row['RAM']} GB RAM")

def main():
    conn = None
    try:
        conn = sqlite3.connect("./dbs/studentsComputers.db")
        conn.row_factory = sqlite3.Row

        create_tables(conn)

        studentId1 = insert_student(conn, "Mark", "Mahoney", "1973/03/19")
        studentId2 = insert_student(conn, "Laura", "Mahoney", "1973/11/01")
        studentId3 = insert_student(conn, "Buddy", "Mahoney", "2004/11/05")
        studentId4 = insert_student(conn, "Patrick", "Mahoney", "2007/10/31")

        computerId1 = insert_computer(conn, "MAC OSX", "32")
        computerId2 = insert_computer(conn, "WIN10", "16")
        
        assign_computer_to_student(conn, studentId1, computerId1)
        assign_computer_to_student(conn, studentId2, computerId2)
        
        studentId5 = insert_student(conn, "Willy", "Mahoney", "2007/01/01")
        print(f"New Student ID: {studentId5}")
        studentId5 = update_student(conn, "William", "The Cat", "2007/01/01", studentId5)
        print(f"Updated Student ID: {studentId5}")
        studentId5 = delete_student(conn, studentId5)
        print(f"Deleted Student ID: {studentId5}")

        get_all_students_and_computers(conn)
        delete_all_computers(conn)
    except Error as e:
        print(f"Error opening the database {e}")
    finally:
        if conn:
            conn.close()

main()
