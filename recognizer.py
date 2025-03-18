# face recognition
import face_recognition
import cv2
from pathlib import Path
import pickle
import numpy as np

# user interface
import argparse

# for FPS
import imutils
from imutils.video import FPS
from imutils.video import WebcamVideoStream

# parameters
DEFAULT_ENCODINGS_PATH = "output/encoding.pkl"

# define args
parser = argparse.ArgumentParser(description = "Recognize faces on video stream")
parser.add_argument("--train", action = "store_true", help = "Train on input data")
parser.add_argument(
    "--recognize", action = "store_true", help = "Recognize faces on video stream"
)
parser.add_argument(
    "-m",
    action = "store",
    default = "hog",
    choices = ["hog", "cnn"],
    help = "Which model to use for training: hog (CPU), cnn (GPU)",
)
args = parser.parse_args()

# load known faces and names
def encode_known_faces(model: str = "hog") -> None:
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
    with open(DEFAULT_ENCODINGS_PATH, mode = "wb") as f:
        pickle.dump(name_encodings, f)

# # load encodings
def load_encodings():
    with open(DEFAULT_ENCODINGS_PATH, mode = "rb") as f:
        name_encodings = pickle.load(f) # load encodings from directory
    
    return name_encodings

# access webcam
def display(known_faces):
    video_capture = WebcamVideoStream(src = 0).start()
    fps = FPS().start()

    while True:
        frame = video_capture.read()

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

        fps.update()

    fps.stop()

    cv2.destroyAllWindows()
    video_capture.stop()

if __name__ == "__main__":
    if args.train:
        encode_known_faces(model = args.m)
    if args.recognize:
        known_faces = load_encodings()
        display(known_faces)

