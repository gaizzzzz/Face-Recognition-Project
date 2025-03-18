from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type = int, default = 100,
    help = "# of frames to loop over for FPS test")

ap.add_argument("-d", "--display", type = int, default = -1,
    help = "Whether or not frames should be displayed")

args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

# loop over some frames
while True:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)
    
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    
    cv2.imshow("Demo fps cam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # update the FPS counter
    fps.update()
    
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()

# class FPS:
#     def __init__(self):
#         self._start = None
#         self._end = None
#         self._numFrames = 0
    
#     def start(self):
#         self._start = datetime.datetime.now()
#         return self

#     def end(self):
#         self._start = datetime.datetime.now()
    
#     def update(self):
#         self._numFrames += 1
    
#     def elapsed(self):
#         return (self._end - self._start).total_seconds()
    
#     def fps(self):
#         return self._numFrames / self.elapsed()

# class WebcamVideoStream:
#     def __init__(self, src = 0):
#         self.stream = cv2.VideoCapture(src)
#         (self.grabbed, self.frame) = self.stream.read()

#         self.stopped = False
    
#     def start(self):
#         Thread(target = self.update, args = ()).start()
#         return self
    
#     def update(self):
#         while True:
#             if self.stopped:
#                break
            
#             (self.grabbed, self.frame) = self.stream.read()
    
#     def read(self):
#         return self.frame
    
#     def stop(self):
#         self.stopped = True