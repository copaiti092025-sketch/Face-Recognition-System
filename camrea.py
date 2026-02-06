import cv2
from face_recognition import get_face_embedding
from attendance import mark_attendance

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    emb = get_face_embedding(frame)

    if emb is not None:
        student = mark_attendance(emb)
        if student:
            cv2.putText(frame, "Attendance Marked", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Smart Attendance", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
