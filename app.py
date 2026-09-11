from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import os
import csv
from datetime import datetime
from database import init_db, add_student, get_students, get_attendance, student_exists
from face_training import capture_faces, train_model
from face_recognition_module import recognize_faces
from report import create_csv_report

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    students = get_students()
    attendance = get_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [a for a in attendance if a["date"] == today]
    present = len(today_records)
    return render_template("index.html", students=students, present=present, total=len(students))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        name = request.form["name"].strip()
        department = request.form["department"].strip()

        if not student_id or not name:
            return render_template("register.html", error="Student ID and name are required.")

        if student_exists(student_id):
            return render_template("register.html", error="Student ID already exists.")

        add_student(student_id, name, department)
        capture_faces(student_id, name)
        train_model()
        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/start_attendance")
def start_attendance():
    recognize_faces()
    return redirect(url_for("attendance"))

@app.route("/records")
def records():
    records = get_attendance()
    return render_template("records.html", records=records)

@app.route("/api/students")
def api_students():
    return jsonify(get_students())

@app.route("/export")
def export():
    path = create_csv_report()
    return send_file(path, as_attachment=True, download_name="attendance_report.csv")

if __name__ == "__main__":
    app.run(debug=True)
