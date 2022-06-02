import cv2
import urllib.request
import numpy as np

stream = urllib.request.urlopen("http://192.168.4.1/")

data = bytearray()

while True:

    data.extend(stream.read(1024))
    a = data.find(b'\xff\xd8')
    b = data.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = data[a:b+2]
        data = data[b+2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), 1)
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
