import cv2

# pre-requisites
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# access webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # show DirectShow instead of MSMF

if not video_capture.isOpened():
    print("Error: Could not open camera!")
    exit()

# identify faces in video stream
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor = 1.1, minNeighbors = 5, minSize = (40, 40)) 

    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), color = (0, 255, 0), thickness = 4) # (0, 255, 0) : color of bbox, 4 : thickness
    
# create a loop for real-time face detection
while True:
    result, video_frame = video_capture.read()

    if not result:
        print("Error: Failed to grab frame")
        break

    faces = detect_bounding_box(video_frame)

    cv2.imshow("Face Detection", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()

