# Smart Attendance System Using OpenCV

A college-project attendance system using Python, Flask, HTML, CSS, JavaScript, OpenCV, LBPH face recognition, and SQLite.

## Features

- Student registration
- Webcam face capture
- Face recognition using OpenCV LBPH
- Automatic attendance marking
- Duplicate attendance prevention for the same student/date
- SQLite student and attendance database
- Attendance report in CSV
- Flask web dashboard
- HTML/CSS/JavaScript frontend

## Installation

Open PyCharm Terminal / Command Prompt inside this folder:

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open the address shown by Flask in your browser.

## Student registration

1. Open Register Student.
2. Enter Student ID, Name and Department.
3. Click Register & Capture Face.
4. A webcam window will open.
5. Look at the camera while about 30 face images are captured.
6. Press Q to stop early if required.
7. The LBPH model is trained automatically.

## Attendance

1. Open Start Attendance.
2. A webcam window opens.
3. Registered students are recognized.
4. Attendance is stored in SQLite.
5. The same student is not inserted twice for the same date.

## Data storage

- Student database: `database/attendance.db`
- Face images: `dataset/`
- Trained model: `trainer/trainer.yml`
- CSV report: `attendance/attendance_report.csv`

## Important

This is an academic prototype. LBPH face recognition is not a high-security biometric system and can be affected by lighting, camera quality, pose, and spoofing. For real deployments, add liveness/anti-spoofing, stronger face embeddings, access control, and appropriate privacy/consent measures.
