import http.client
import json
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.COLOR = QColor(255, 0, 4)
        self.INTENSITY = 0
        self.IP = "127.0.0.1"
        self.WAIT = 0.01
        self.CONNECTION = http.client.HTTPConnection('192.168.1.223', 8080)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(242, 581)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.mainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.solidGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.solidGroup.setGeometry(QtCore.QRect(10, 150, 221, 141))
        self.solidGroup.setObjectName("solidGroup")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.solidGroup)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 201, 112))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.solidLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.solidLayout.setContentsMargins(0, 0, 0, 0)
        self.solidLayout.setObjectName("solidLayout")
        self.colorPickerButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.colorPickerButton.setObjectName("colorPickerButton")
        self.solidLayout.addWidget(self.colorPickerButton)
        self.solidColorButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.solidColorButton.setObjectName("solidColorButton")
        self.solidLayout.addWidget(self.solidColorButton)
        self.fromScreenStaticButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.fromScreenStaticButton.setObjectName("fromScreenStaticButton")
        self.solidLayout.addWidget(self.fromScreenStaticButton)
        self.loopFromBackButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.loopFromBackButton.setObjectName("loopFromBackButton")
        self.solidLayout.addWidget(self.loopFromBackButton)
        self.rainbowGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.rainbowGroup.setGeometry(QtCore.QRect(10, 300, 221, 131))
        self.rainbowGroup.setObjectName("rainbowGroup")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.rainbowGroup)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 201, 101))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.rainbowLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.rainbowLayout.setContentsMargins(0, 0, 0, 0)
        self.rainbowLayout.setObjectName("rainbowLayout")
        self.rainbowSequenceButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.rainbowSequenceButton.setObjectName("rainbowSequenceButton")
        self.rainbowLayout.addWidget(self.rainbowSequenceButton)
        self.rainbowCycleButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.rainbowCycleButton.setObjectName("rainbowCycleButton")
        self.rainbowLayout.addWidget(self.rainbowCycleButton)
        self.rainbowColorsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.rainbowColorsButton.setObjectName("rainbowColorsButton")
        self.rainbowLayout.addWidget(self.rainbowColorsButton)
        self.intensityGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.intensityGroup.setGeometry(QtCore.QRect(10, 10, 221, 131))
        self.intensityGroup.setObjectName("intensityGroup")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.intensityGroup)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 201, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.IntensityLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.IntensityLayout.setContentsMargins(0, 0, 0, 0)
        self.IntensityLayout.setObjectName("IntensityLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.intensitySlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.intensitySlider.setMaximum(255)
        self.intensitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.intensitySlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.intensitySlider.setObjectName("intensitySlider")
        self.horizontalLayout.addWidget(self.intensitySlider)
        self.intensityLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.intensityLabel.setObjectName("intensityLabel")
        self.horizontalLayout.addWidget(self.intensityLabel)
        self.IntensityLayout.addLayout(self.horizontalLayout)
        self.intensityButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.intensityButton.setObjectName("intensityButton")
        self.IntensityLayout.addWidget(self.intensityButton)
        self.animateIntensityButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.animateIntensityButton.setObjectName("animateIntensityButton")
        self.IntensityLayout.addWidget(self.animateIntensityButton)
        self.miscGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.miscGroup.setGeometry(QtCore.QRect(10, 440, 221, 131))
        self.miscGroup.setObjectName("miscGroup")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.miscGroup)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 19, 201, 41))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.miscLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.miscLayout.setContentsMargins(0, 0, 0, 0)
        self.miscLayout.setObjectName("miscLayout")
        self.fromScreenAnimate = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.fromScreenAnimate.setObjectName("fromScreenAnimate")
        self.miscLayout.addWidget(self.fromScreenAnimate)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.miscLayout.addWidget(self.line)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.miscGroup)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 201, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.waitLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.waitLabel.setObjectName("waitLabel")
        self.horizontalLayout_2.addWidget(self.waitLabel)
        self.waitLine = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.waitLine.setInputMask("")
        self.waitLine.setObjectName("waitLine")
        self.horizontalLayout_2.addWidget(self.waitLine)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.miscGroup)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 90, 201, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ipLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.ipLabel.setObjectName("ipLabel")
        self.horizontalLayout_3.addWidget(self.ipLabel)
        self.ipLine = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.ipLine.setObjectName("ipLine")
        self.horizontalLayout_3.addWidget(self.ipLine)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.intensitySlider.valueChanged['int'].connect(self.intensityLabel.setNum)
        self.colorPickerButton.clicked.connect(self.openColorDialog)
        self.solidColorButton.clicked.connect(self.sendSolidColor)
        self.loopFromBackButton.clicked.connect(self.loopFromBack)
        self.fromScreenStaticButton.clicked.connect(self.solidFromScreen)
        self.rainbowColorsButton.clicked.connect(self.rainbowColors)
        self.rainbowCycleButton.clicked.connect(self.rainbowCycle)
        self.rainbowSequenceButton.clicked.connect(self.rainbowSequence)
        self.intensityButton.clicked.connect(self.setIntesity)
        self.animateIntensityButton.clicked.connect(self.animateIntesnity)
        self.ipLine.returnPressed.connect(self.setIP)
        self.waitLine.returnPressed.connect(self.setWait)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        self.COLOR = color

    def setIP(self):
        self.IP = self.ipLine.text()
        self.CONNECTION = http.client.HTTPConnection(self.IP, 8080)

    def setWait(self):
        self.WAIT = float(self.waitLine.text())

    def buildGenericJSON(self):
        data = {'wait': self.WAIT, 'target': self.intensitySlider.value(), 'color': [self.COLOR.red(), self.COLOR.green(), self.COLOR.blue()]}
        return data

    def sendSolidColor(self):
        self.CONNECTION.request('POST', '/solid', '{"wait": 0.0, "red": 40, "green": 0, "blue": 0}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def loopFromBack(self):
        self.CONNECTION.request('POST', '/appearfromback', '{"color": [4, 0, 255]}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def setIntesity(self):
        self.CONNECTION.request('POST', '/intensity', '{"target": 20, "force": "True"}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def animateIntesnity(self):
        self.CONNECTION.request('POST', '/intensity', '{"target": 20, "force": "False"}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def rainbowSequence(self):
        self.CONNECTION.request('POST', '/rainbowS', '{"wait": 0.01}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def rainbowCycle(self):
        self.CONNECTION.request('POST', '/rainbowC', '{"wait": 0.01}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def rainbowColors(self):
        self.CONNECTION.request('POST', '/rainbowColors', '{"wait": 0.01}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def solidFromScreen(self):
        self.CONNECTION.request('POST', '/solidArr', '{"wait": 0.0}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def animateFromScreen(self):
        self.CONNECTION.request('POST', '/solidArr', '{"wait": 0.0}')
        doc = self.CONNECTION.getresponse().read()
        print(doc)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PiLights"))
        self.solidGroup.setTitle(_translate("MainWindow", "Solid Colors"))
        self.colorPickerButton.setText(_translate("MainWindow", "Color Picker"))
        self.solidColorButton.setText(_translate("MainWindow", "Solid Color"))
        self.fromScreenStaticButton.setText(_translate("MainWindow", "Static From Screen"))
        self.loopFromBackButton.setText(_translate("MainWindow", "Loop From Back"))
        self.rainbowGroup.setTitle(_translate("MainWindow", "Rainbow"))
        self.rainbowSequenceButton.setText(_translate("MainWindow", "Rainbow Sequence"))
        self.rainbowCycleButton.setText(_translate("MainWindow", "Rainbow Cycle"))
        self.rainbowColorsButton.setText(_translate("MainWindow", "RainbowColors"))
        self.intensityGroup.setTitle(_translate("MainWindow", "Intensity"))
        self.intensityLabel.setText(_translate("MainWindow", "255"))
        self.intensityButton.setText(_translate("MainWindow", "Set Intensity"))
        self.animateIntensityButton.setText(_translate("MainWindow", "Animate Intensity"))
        self.miscGroup.setTitle(_translate("MainWindow", "Miscellaneous"))
        self.fromScreenAnimate.setText(_translate("MainWindow", "Animate From Screen"))
        self.waitLabel.setText(_translate("MainWindow", "Wait Time"))
        self.waitLine.setText(_translate("MainWindow", "0.01"))
        self.ipLabel.setText(_translate("MainWindow", "IP Address"))
        self.ipLine.setText(_translate("MainWindow", "192.168.1.223"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
