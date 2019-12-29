import http.client
import json
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog
import queue
import pyautogui


def get_max(arr):
    max_c = (0, (0, 0, 0))
    for pix in arr:
        if pix[0] > max_c[0]:
            max_c = pix
    return max_c


class Ui_MainWindow(object):

    def worker(self):
        animate = False
        while True:
            item = self.QUEUE.get()
            if item is None:
                print("EXITING WORKER")
                break
            elif item.get('screen') is not None:
                image = pyautogui.screenshot()
                colors = self.generate_from_image(image)
                data = self.buildGenericJSON(False)
                data['colors'] = colors
                self.CONNECTION.request('POST', '/solidArr', json.dumps(data))
                doc = self.CONNECTION.getresponse().read()
                print(doc)
                if item.get('screen') == 'animate':
                    animate = True
                else:
                    animate = False
            else:
                animate = False
            self.QUEUE.task_done()
            time.sleep(0.35)
            if animate and self.QUEUE.empty():
                self.QUEUE.put({'screen': 'animate'})

    def generate_from_image(self, image):
        x_start = 0
        # Calculates column width for the given picture to fill an LED
        x_inc = self.RESOLUTION[0]//self.PIXEL_COUNT
        colors = []
        for i in range(self.PIXEL_COUNT):
            # Generates a box with the given column width
            crop = image.crop((x_start, 0, x_start + x_inc, self.RESOLUTION[1]))
            # get_max returns (x, (x, x, x)) where the second tuple is the RGB value, we need to transform into a list for JSON
            colors.append(list(get_max(crop.getcolors(x_inc * self.RESOLUTION[1]))[1]))
            # Moves the box over to the next column/LED
            x_start += x_inc
        return colors

    def start_worker(self):
        thread = threading.Thread(target=self.worker)
        thread.start()
        return thread

    def stop_worker(self):
        self.QUEUE.put(None)
        self.WORKER.join()

    def populate_from_config(self):
        with open('config', 'r') as config:
            content = config.read()
        content = json.loads(content)
        if content.get('IP'):
            self.IP = content.get('IP')
        if content.get('PIXEL_COUNT'):
            self.PIXEL_COUNT = content.get('PIXEL_COUNT')
        if content.get('RESOLUTION'):
            self.RESOLUTION = content.get('RESOLUTION')
        if content.get('DEFAULT_WAIT'):
            self.WAIT = content.get('DEFAULT_WAIT')

    def setupUi(self, MainWindow):
        self.COLOR = QColor(255, 0, 4)
        self.INTENSITY = 0
        self.IP = ""
        self.WAIT = 0
        self.PIXEL_COUNT = 1
        self.RESOLUTION = []

        self.populate_from_config()

        self.CONNECTION = http.client.HTTPConnection(self.IP, 8080)
        self.QUEUE = queue.Queue()
        self.WORKER = self.start_worker()


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
        self.fromScreenAnimate.clicked.connect(self.animateFromScreen)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        self.COLOR = color

    def setIP(self):
        self.IP = self.ipLine.text()
        self.CONNECTION = http.client.HTTPConnection(self.IP, 8080)

    def setWait(self):
        self.WAIT = float(self.waitLine.text())

    def buildGenericJSON(self, wait=True):
        data = {'wait': self.WAIT if wait else 0, 'target': self.intensitySlider.value(), 'color': [self.COLOR.red(), self.COLOR.green(), self.COLOR.blue()]}
        return data

    def sendSolidColor(self):
        try:
            self.QUEUE.put({'clear': True})
            self.CONNECTION.request('POST', '/solid', json.dumps(self.buildGenericJSON()))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def loopFromBack(self):
        try:
            self.QUEUE.put({'clear': True})
            self.CONNECTION.request('POST', '/appearfromback', json.dumps(self.buildGenericJSON()))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def setIntesity(self):
        try:
            data = self.buildGenericJSON()
            data['force'] = "True"
            self.CONNECTION.request('POST', '/intensity', json.dumps(data))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def animateIntesnity(self):
        try:
            self.QUEUE.put({'clear': True})
            data = self.buildGenericJSON()
            data['force'] = "False"
            self.CONNECTION.request('POST', '/intensity', json.dumps(data))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def rainbowSequence(self):
        try:
            self.QUEUE.put({'clear': True})
            self.CONNECTION.request('POST', '/rainbowS', json.dumps(self.buildGenericJSON()))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def rainbowCycle(self):
        try:
            self.QUEUE.put({'clear': True})
            self.CONNECTION.request('POST', '/rainbowC', json.dumps(self.buildGenericJSON()))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def rainbowColors(self):
        try:
            self.QUEUE.put({'clear': True})
            self.CONNECTION.request('POST', '/rainbowColors', json.dumps(self.buildGenericJSON()))
            print(self.CONNECTION.getresponse().read())
        except Exception as e:
            print(e)

    def solidFromScreen(self):
        self.QUEUE.put({'screen': 'static'})

    def animateFromScreen(self):
        self.QUEUE.put({'screen': 'animate'})

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
        self.rainbowColorsButton.setText(_translate("MainWindow", "Rainbow Colors"))
        self.intensityGroup.setTitle(_translate("MainWindow", "Intensity"))
        self.intensityLabel.setText(_translate("MainWindow", "255"))
        self.intensityButton.setText(_translate("MainWindow", "Set Intensity"))
        self.animateIntensityButton.setText(_translate("MainWindow", "Animate Intensity"))
        self.miscGroup.setTitle(_translate("MainWindow", "Miscellaneous"))
        self.fromScreenAnimate.setText(_translate("MainWindow", "Animate From Screen"))
        self.waitLabel.setText(_translate("MainWindow", "Wait Time"))
        self.waitLine.setText(_translate("MainWindow", str(self.WAIT)))
        self.ipLabel.setText(_translate("MainWindow", "IP Address"))
        self.ipLine.setText(_translate("MainWindow", self.IP))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ret = app.exec_()
    ui.stop_worker()
    sys.exit(ret)
