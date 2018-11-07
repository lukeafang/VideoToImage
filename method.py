import os
import cv2
import numpy as np

def loadVideo(fileName):
    cap = cv2.VideoCapture(fileName)
    if cap.isOpened(): 
        # get vcap property 
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float 3
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float 4
        # it gives me 0.0 :/
        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()  
    return height, width, fps, length

def convertToImage(fileName, freq, fileType, outputFileName):
    cap = cv2.VideoCapture(fileName)
    
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float 3
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float 4

    count = 0
    index = 0
    dirPath = os.path.dirname(os.path.realpath(__file__)) + '/output'
    ret, frame = cap.read()
    while True:
        if count >= freq:
            saveFileName = "%s_%d.jpeg" % (outputFileName, index)
            fullOutputPath = dirPath + '/' + saveFileName
            cv2.imwrite(fullOutputPath, frame)
            index += 1
            count = 0
        else:
            count += 1

        #No more new frame, exit loop
        if ret == False:
            break     
        #grab next frame
        ret, frame = cap.read()
    cap.release() 
    return
