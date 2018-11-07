#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 5 13:24:13 2018

@author: lukefang
"""
import os
import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,QComboBox,
                             QPushButton, QFileDialog, QSizePolicy, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt

from method import loadVideo, convertToImage


"""
MainWindow of application
"""
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # gobal data

        self.initUI()

    def initUI(self):
        self.resize(250, 300)
        self.setWindowTitle('Video To Image Application')

        itemX = 10
        itemY = 20
        # load Video Btn
        self.loadVideo_Btn = QPushButton('Load Video', self)
        self.loadVideo_Btn.clicked.connect(self.loadVideo_Btn_Clicked)
        self.loadVideo_Btn.move(itemX, itemY)

        itemY += 30
        tempItemX = itemX + 5
        itemW = 70
        itemH = 20
        self.videoFileName_label = QLabel('File Name: ', self)
        self.videoFileName_label.resize(itemW, itemH)
        self.videoFileName_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.videoFileName_text = QLineEdit('', self)
        self.videoFileName_text.resize(itemW, itemH)
        self.videoFileName_text.setReadOnly(True)
        self.videoFileName_text.move(tempItemX, itemY)

        tempItemX = itemX + 5
        itemY += 20
        itemW = 70
        self.videoFrameSize_label = QLabel('Size (HxW): ', self)
        self.videoFrameSize_label.resize(itemW, itemH)
        self.videoFrameSize_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.videoFrameSize_text = QLineEdit('', self)
        self.videoFrameSize_text.resize(itemW, itemH)
        self.videoFrameSize_text.setReadOnly(True)
        self.videoFrameSize_text.move(tempItemX, itemY)         

        tempItemX = itemX + 5
        itemY += 20
        itemW = 70
        self.videoNFrame_label = QLabel('n Frames: ', self)
        self.videoNFrame_label.resize(itemW, itemH)
        self.videoNFrame_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.videoNFrame_text = QLineEdit('', self)
        self.videoNFrame_text.resize(itemW, itemH)
        self.videoNFrame_text.setReadOnly(True)
        self.videoNFrame_text.move(tempItemX, itemY)    

        tempItemX = itemX + 5
        itemY += 20
        itemW = 70
        self.videoFPS_label = QLabel('FPS: ', self)
        self.videoFPS_label.resize(itemW, itemH)
        self.videoFPS_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.videoFPS_text = QLineEdit('', self)
        self.videoFPS_text.resize(itemW, itemH)
        self.videoFPS_text.setReadOnly(True)
        self.videoFPS_text.move(tempItemX, itemY) 

        #output UI
        itemY += 40
        # load Video Btn
        self.convertToImage_Btn = QPushButton('Convert to Images', self)
        self.convertToImage_Btn.clicked.connect(self.convertToImage_Clicked)
        self.convertToImage_Btn.move(itemX, itemY)   

        itemY += 30
        tempItemX = itemX + 5
        itemW = 70
        itemH = 20
        self.convertImageFrequence_label = QLabel('Frequence: ', self)
        self.convertImageFrequence_label.resize(itemW, itemH)
        self.convertImageFrequence_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.convertImageFrequence_text = QLineEdit('10', self)
        self.convertImageFrequence_text.resize(itemW, itemH)
        self.convertImageFrequence_text.move(tempItemX, itemY)

        itemY += 25
        tempItemX = itemX + 5
        itemW = 70
        itemH = 20
        self.convertImageName_label = QLabel('Name: ', self)
        self.convertImageName_label.resize(itemW, itemH)
        self.convertImageName_label.move(tempItemX, itemY)
        tempItemX += (itemW+5)

        itemW = 110
        self.convertImageName_text = QLineEdit('', self)
        self.convertImageName_text.resize(itemW, itemH)
        self.convertImageName_text.move(tempItemX, itemY)

        tempItemX = itemX + 5
        itemY += 25
        itemW = 50
        itemH = 20
        self.convert_format_label = QLabel('Format:', self)
        self.convert_format_label.resize(itemW, itemH)
        self.convert_format_label.move(tempItemX, itemY)

        tempItemX += (itemW+5)
        itemW = 100
        self.convert_format_cb = QComboBox(self)
        self.convert_format_cb.addItem("jpeg")
        self.convert_format_cb.addItem("bmp")
        self.convert_format_cb.addItem("png")
        self.convert_format_cb.resize(itemW, itemH)
        self.convert_format_cb.move(tempItemX, itemY)
  

    def keyPressEvent(self, e):    
        if e.key() == Qt.Key_Escape:
            self.close()
        
    def loadVideo_Btn_Clicked(self):
        filename, _ = QFileDialog.getOpenFileName( None, 'Buscar Imagen', '.', 'video Files (*.mp4 *.avi *.mov)')
        if filename:
            self.videoFilePath = filename

            height, width, fps, length = loadVideo(filename)
            tempStr = "%.2f" % fps
            self.videoFPS_text.setText(tempStr)
            tempStr = "%d x %d" % (height, width)
            self.videoFrameSize_text.setText(tempStr)
            tempStr = "%d" % length
            self.videoNFrame_text.setText(tempStr)

            self.videoFileName_text.setText(os.path.basename(filename))
            tempFilename = os.path.basename(filename)
            tempFilename = os.path.splitext(tempFilename)[0]
            self.convertImageName_text.setText(tempFilename)

        return

    def convertToImage_Clicked(self):
        if len(self.videoFilePath) == 0:
            return
        tempStr = self.convertImageFrequence_text.text()
        freq = 10
        if len(tempStr) == 0:
            freq = 10
        else:
            freq = int(tempStr)

        extension = str(self.convert_format_cb.currentText())
        if extension == 'jpeg':
            fileType = extension
        elif extension == 'bmp':
            fileType = extension
        else:
            fileType = extension
        
        outputFileName = self.convertImageName_text.text()
        if len(outputFileName) == 0:
            outputFileName = 'output'
        convertToImage(self.videoFilePath, freq, fileType, outputFileName)
        QMessageBox.about(self, "Title", 'Finished')
        return



if __name__ == "__main__":
    # create output folder
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory = dir_path + '/output'
    if not os.path.exists(directory):
        os.makedirs(directory)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
