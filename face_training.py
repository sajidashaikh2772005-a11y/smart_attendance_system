import cv2
import os
import numpy as np

DATASET = "dataset"
TRAINER = "trainer/trainer.yml"

def capture_faces(student_id, name, count=30):
    path = os.path.join(DATASET, f"{student_id}_{name.replace(' ', '_')}")
    os.makedirs(path, exist_ok=True)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    cam = cv2.VideoCapture(0)

    saved = 0
    while saved < count:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            saved += 1
            filename = os.path.join(path, f"{saved}.jpg")
            cv2.imwrite(filename, gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)

        cv2.putText(frame, f"Captured: {saved}/{count}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.imshow("Face Registration - Press Q to stop", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

def train_model():
    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "cv2.face is unavailable. Install opencv-contrib-python."
        )

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = []
    ids = []

    folders = [f for f in os.listdir(DATASET)
               if os.path.isdir(os.path.join(DATASET, f))]

    for folder in folders:
        student_id = folder.split("_", 1)[0]
        try:
            label = int(student_id)
        except ValueError:
            continue

        folder_path = os.path.join(DATASET, folder)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            detected = detector.detectMultiScale(img)
            if len(detected) == 0:
                faces.append(img)
                ids.append(label)
            else:
                for (x, y, w, h) in detected:
                    faces.append(img[y:y+h, x:x+w])
                    ids.append(label)

    if not faces:
        raise RuntimeError("No face images found. Register a student first.")

    os.makedirs("trainer", exist_ok=True)
    recognizer.train(faces, np.array(ids))
    recognizer.write(TRAINER)
