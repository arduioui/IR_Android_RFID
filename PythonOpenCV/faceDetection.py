# Arduioui
# To communicate with Arduino by Serial
from serial import Serial

# OpenCV for Face detection
import cv2

serial_port = Serial(port="/dev/cu.usbmodem1411", baudrate=9600)

print("Waiting for infrared signal to launch Face Dectection...")

while True:
    strEcho = serial_port.readline()
    #print(strEcho)
    if "IR" in strEcho:

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        video_capture = cv2.VideoCapture(0)
        RFID = "unknow"
        count = 0

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            maxSquare = 0

            saveWidth = 0
            saveHeight = 0
            saveX = 0
            saveY = 0

            count = 0
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                count = count + 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if w*h > maxSquare:
                    maxSquare = w * h
                    saveX = x
                    saveY = y
                    saveWidth = w
                    saveHeight = h

            cv2.putText(frame, RFID, (saveX, saveY+saveHeight), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,64,255))

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if count == 0:
                break

            serialReading = serial_port.readline()
            print(serialReading)
            if "discard" in serialReading or "IR" in serialReading:
                continue
            else:
                RFID = serialReading

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
