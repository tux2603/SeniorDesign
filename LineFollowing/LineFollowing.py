# Copied from: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html

# Working draft
import numpy as np
import cv2
from threading import Thread

class LineFollower:
    def __init__(self, left_margin=180, right_margin=140, show_debug_window=False):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

        # Set to true to terminate the thread
        self._terminate = False

        # Internal variables to get line following data from the thread
        self._steering = 0
        self._is_line_acquired = False

        # Set the margins
        self._left_margin = left_margin
        self._right_margin = right_margin

        self._show_debug_window = show_debug_window

        # Start the thread
        self._thread = Thread(target=self._processing_thread)
        self._thread.start()

    @property
    def steering(self):
        # TODO: Check to see if there's a lock needed here
        return self._steering

    @property
    def is_line_acquired(self):
        # TODO: Check to see if there's a lock needed here
        return self._is_line_acquired

    def stop(self):
        self._terminate = True
        self._thread.join()

    def _processing_thread(self):
        while not self._terminate:
            # print('LineFollower: Processing thread running')
            # Capture the frames
            ret, frame = self.video_capture.read()
            
            # Crop the image 
            crop_img = frame[0:480, 0:480]

            # Convert to grayscale
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            # Gaussian blur
            blur = cv2.GaussianBlur(gray,(5,5),0)

            # Color thresholding
            ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

            # Find the contours of the frame
            contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

            # Find the biggest contour (if detected - might need to be edited)
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            # Values below will also need to be edited
                if cx >= self._left_margin:
                    self._steering = -1
                if cx < self._left_margin and cx > self._right_margin:
                    self._steering = 0
                if cx <= self._right_margin:
                    self._steering = 1

                self._is_line_acquired = True

            else:
                self._is_line_acquired = False
                self._steering = 0

            if self._show_debug_window:
                # Display the resulting frame
                cv2.imshow('frame',crop_img)

            # press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    # Creare a demo line follower
    line_follower = LineFollower(show_debug_window=True)

    while True:
        try:
            if not line_follower.is_line_acquired:
                print('No line detected')
            elif line_follower.steering == -1:
                print('Turn left')
            elif line_follower.steering == 0:
                print('Go straight')
            elif line_follower.steering == 1:
                print('Turn right')
        except KeyboardInterrupt:
            print('\nExiting...')
            line_follower.stop()
            break