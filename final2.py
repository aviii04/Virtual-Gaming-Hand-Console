# -*- coding: utf-8 -*-
"""                            
Created on Wed Apr 17 17:45:17 2019

@author: Aviii
"""

from keras.preprocessing import image
import numpy as np
import pickle
import cv2
from pynput.keyboard import Key, Controller
keyboard = Controller()


#from appscript import app

# Environment:
# OS    : Mac OS EL Capitan
# python: 3.5
# opencv: 2.4.13

# parameters
cap_region_x_begin=1  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0
track_threshold=10


# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

with open('Model1_back_sub_5epo','rb') as f:
    mp=pickle.load(f)

def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res
                            
# Camera
camera = cv2.VideoCapture(1)
camera.set(10,200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)

arr=[]
track=0
while camera.isOpened():
    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    cv2.imshow('original', frame)

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        img = removeBG(frame)
        cv2.imshow('mask', img)
        cropped=img[:360,:640]
        
        cv2.imwrite('Dataset/Manual1/Temp/image.jpg', cropped)
        test_image = image.load_img('Dataset/Manual1/Temp/image.jpg', target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = mp.predict(test_image)
#        if result[0][0] == 1:
#           print('ThumbToPalm')
#        else:
#           print('IndexToPalm')
#        ===========Controling output================
        count=0
        ans=0
        if result[0][0]==1:
            arr.append(1)
        else:
            arr.append(0)
        track=track+1
        
        if track==track_threshold:
            track=0
            for x in arr:
                if x==1:
                    count=count+1
            ans=(count/track_threshold)*100
            arr.clear()
            if ans>60:
                print('ThumbToPalm')
                keyboard.press('q')
                keyboard.release('q')
            else:
                print('IndexToPalm')
                keyboard.press(Key.space)                  
                keyboard.release(Key.space)

                
            
#        ============================================

# Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1
        print( '!!!Background Captured!!!')
    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')
    elif k == ord('n'):
        triggerSwitch = True
        print ('!!!Trigger On!!!')