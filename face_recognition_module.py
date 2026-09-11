import cv2
import os
from database import get_student_by_id, mark_attendance

TRAINER = "trainer/trainer.yml"

def recognize_faces():
    if not os.path.exists(TRAINER):
        raise RuntimeError("Trainer file not found. Register a student first.")

    if not hasattr(cv2, "face"):
        raise RuntimeError("Install opencv-contrib-python.")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)
    marked = set()

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            student = get_student_by_id(str(label))
            if student and confidence < 75:
                name = student["name"]
                student_id = student["student_id"]
                mark_attendance(student_id, name)
                marked.add(student_id)
                text = f"{name} - Present"
            else:
                text = "Unknown"

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.putText(frame, "Press Q to stop", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.imshow("Smart Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
