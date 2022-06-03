import cv2
import numpy as np
import time

#create Background Subtractor objects
#backSub = cv2.createBackgroundSubtractorKNN()
backSub = cv2.createBackgroundSubtractorMOG2()
#backSub.setDetectShadows(False)

capture = cv2.VideoCapture(0)
time.sleep(0.2)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
time.sleep(0.2)
capture.set(cv2.CAP_PROP_EXPOSURE,100)
time.sleep(0.2)
capture.set(cv2.CAP_PROP_AUTO_WB, 0)
time.sleep(0.2)
capture.set(cv2.CAP_PROP_AUTOFOCUS,0)
time.sleep(0.2)





pattern = cv2.imread('pattern1.png', cv2.IMREAD_GRAYSCALE)
edged = cv2.Canny(pattern, 30, 200)
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cv2.namedWindow("Geocaching", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Geocaching", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)



while True:
    ret, frame = capture.read()
    if frame is None:
        break
    cv2.imshow('Image', frame)
    blur = cv2.blur(frame,(20,20))    
    #update the background model
    fgMask = backSub.apply(blur, None, 0.0001)

    _, fgMask = cv2.threshold(fgMask, thresh=240, maxval=255, type=cv2.THRESH_BINARY)
    #cv2.imshow('Geocaching', fgMask)

    
    good_values = cv2.bitwise_and(pattern,fgMask)
    number_of_good_values = cv2.countNonZero(good_values)
    green = np.copy(frame)
    # boolean indexing and assignment based on mask
    green[(good_values==255)] = [0,255,0]

    inverted_pattern = cv2.bitwise_not(pattern)
    bad_values = cv2.bitwise_and(inverted_pattern, fgMask)
    number_of_bad_values = cv2.countNonZero(bad_values)
    red = np.copy(frame)
    # boolean indexing and assignment based on mask
    red[(bad_values==255)] = [0,0,255]
    
    pattern_size = cv2.countNonZero(pattern)
    inverted_pattern_size = cv2.countNonZero(inverted_pattern)
    #cv2.imshow('Good values', good_values)
    #cv2.imshow('Bad values', bad_values)
    #cv2.imshow('Pattern', pattern)
    #cv2.imshow('Inverted pattern', inverted_pattern)

    #print("Good coverage: " + str(int(round(100*number_of_good_values / pattern_size)))+"%")
    #print("Bad coverage: " + str(int(round(100*number_of_bad_values / inverted_pattern_size)))+"%")
    #print("#Bad values: " + str(number_of_bad_values))
    #print("#Good values: " + str(number_of_good_values))
    #print("Pattern size: " + str(pattern_size))
    #print("Inverted pattern size: " + str(inverted_pattern_size))
    
    
    green_hair_w = cv2.addWeighted(green, 0.3, frame, 0.7, 0)
    final = cv2.addWeighted(red, 0.3, green_hair_w, 0.7, 0)
    cv2.drawContours(final, contours, -1, (255, 0 , 0), 3)
    
    #show the current frame and the fg masks
    #cv2.imshow('Frame', frame)
    
    procent = int(round(100 * (number_of_good_values / pattern_size)    *    (1 - number_of_bad_values / inverted_pattern_size)))
    #print(procent)
    # org 
    org = (50, 50) 
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # fontScale 
    fontScale = 1
    
    # Blue color in BGR 
    color = (0, 0, 0) 
    
    # Line thickness of 2 px 
    thickness = 2
    
    # Using cv2.putText() method 
    final = cv2.putText(final, 'Try to cover the area', (140,30), font,  
                        fontScale, color, thickness, cv2.LINE_AA) 
        
    # Using cv2.putText() method
    final = cv2.putText(final, str(procent) + '% covered', (210,60), font,  
                        fontScale, color, thickness, cv2.LINE_AA) 
    if procent > 60:
        final = cv2.putText(final, 'Awesome, the code is 583!', (80,150), font,  
                            fontScale, (0,255,255), thickness, cv2.LINE_AA) 
    
    
    cv2.imshow('Geocaching', final)
    
    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
