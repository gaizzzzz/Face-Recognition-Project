import easygui.boxes
import face_recognition
import cv2
from pathlib import Path
import pickle
import numpy as np
import easygui

# parameters
DEFAULT_ENCODINGS_PATH = "output/encoding.pkl"

# load known faces and names
def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH # hog = histogram of oriented gradients
) -> None:
    names = []
    encodings = []

    for filepath in Path("training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model = model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
        
    name_encodings = {"names": names, "encodings": encodings}

    return name_encodings

known_faces = encode_known_faces()

# access webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video_capture.isOpened():
    easygui.msgbox("Error: Cannot access webcam!")
    exit()

while True:
    ret, frame = video_capture.read()

    if not ret:
        easygui.msgbox("Error: Failed to grab frame!")
        break

    # convert into RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # process detected faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces["encodings"], face_encoding)
        name = "Unknown"

        # use the closest match
        face_distances = face_recognition.face_distance(known_faces["encodings"], face_encoding)
        best_match_idx = np.argmin(face_distances)

        if matches[best_match_idx]:
            name = known_faces["names"][best_match_idx]
        
        # draw bounding box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


