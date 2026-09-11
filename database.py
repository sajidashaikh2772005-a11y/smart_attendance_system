import sqlite3
import os

DB_PATH = os.path.join("database", "attendance.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs("database", exist_ok=True)
    con = connect()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            UNIQUE(student_id, date)
        )
    """)
    con.commit()
    con.close()

def add_student(student_id, name, department):
    con = connect()
    con.execute(
        "INSERT INTO students(student_id,name,department) VALUES(?,?,?)",
        (student_id, name, department)
    )
    con.commit()
    con.close()

def student_exists(student_id):
    con = connect()
    row = con.execute("SELECT 1 FROM students WHERE student_id=?", (student_id,)).fetchone()
    con.close()
    return row is not None

def get_students():
    con = connect()
    rows = con.execute(
        "SELECT student_id,name,department,created_at FROM students ORDER BY id DESC"
    ).fetchall()
    con.close()
    return [
        {"student_id": r[0], "name": r[1], "department": r[2], "created_at": r[3]}
        for r in rows
    ]

def get_student_by_id(student_id):
    con = connect()
    row = con.execute(
        "SELECT student_id,name,department FROM students WHERE student_id=?",
        (student_id,)
    ).fetchone()
    con.close()
    if not row:
        return None
    return {"student_id": row[0], "name": row[1], "department": row[2]}

def mark_attendance(student_id, name):
    from datetime import datetime
    now = datetime.now()
    con = connect()
    con.execute("""
        INSERT OR IGNORE INTO attendance(student_id,name,date,time,status)
        VALUES(?,?,?,?,?)
    """, (student_id, name, now.strftime("%Y-%m-%d"),
          now.strftime("%H:%M:%S"), "Present"))
    con.commit()
    con.close()

def get_attendance():
    con = connect()
    rows = con.execute(
        "SELECT student_id,name,date,time,status FROM attendance ORDER BY date DESC,time DESC"
    ).fetchall()
    con.close()
    return [
        {"student_id": r[0], "name": r[1], "date": r[2],
         "time": r[3], "status": r[4]}
        for r in rows
    ]
