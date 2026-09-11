import csv
import os
from database import get_attendance

def create_csv_report():
    os.makedirs("attendance", exist_ok=True)
    path = os.path.join("attendance", "attendance_report.csv")
    records = get_attendance()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Student ID", "Name", "Date", "Time", "Status"])
        for r in records:
            writer.writerow([
                r["student_id"], r["name"], r["date"],
                r["time"], r["status"]
            ])
    return path
