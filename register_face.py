import cv2
import pickle
from database import get_db_connection
from face_recognition import get_face_embedding

cap = cv2.VideoCapture(0)
name = input("Enter Student Name: ")

while True:
    ret, frame = cap.read()
    emb = get_face_embedding(frame)

    cv2.imshow("Register Face", frame)

    if emb is not None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, embedding) VALUES (%s, %s)",
            (name, pickle.dumps(emb))
        )
        conn.commit()
        conn.close()
        print("✅ Face Registered Successfully")
        break

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
