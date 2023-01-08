from PyQt5 import QtCore, QtWidgets
import linkedinScraper
import sys


class Ui_MainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("Linkedin Scraper")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 190, 113, 32))
        self.pushButton.setObjectName("gatherDataButton")
        self.pushButton.clicked.connect(self.gatherData)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 80, 151, 16))
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(270, 130, 281, 21))
        self.lineEdit.setObjectName("input")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(210, 260, 411, 192))
        self.textBrowser.setObjectName("textBrowser")

        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.gatherData()
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("Linkedin Scraper", "Linkedin Scraper"))
        self.pushButton.setText(_translate("Linkedin Scraper", "Gather Data"))
        self.label.setText(_translate("Linkedin Scraper", "Niya\'s Linkedin Scraper"))
        self.lineEdit.setText(_translate("Linkedin Scraper", ""))

    def gatherData(self):
        link = self.lineEdit.text()
        if link != "":
            data = linkedinScraper.scraper(link)
            self.textBrowser.setText(data)

if __name__ == "__main__":
    scraper = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(scraper.exec_())