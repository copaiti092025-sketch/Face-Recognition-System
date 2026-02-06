import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name="buffalo_l",
    root="./models/insightface_model"
)
app.prepare(ctx_id=0, det_size=(640,640))


def get_face_embedding(frame):
    faces = app.get(frame)
    if len(faces) == 0:
        return None
    return faces[0].embedding
