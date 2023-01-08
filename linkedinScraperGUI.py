from PyQt5 import QtCore, QtWidgets
import linkedinScraper
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Linkedin Scraper")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.gatherData(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Linkedin Scraper", "Linkedin Scraper"))
        self.pushButton.setText(_translate("Linkedin Scraper", "Gather Data"))
        self.label.setText(_translate("Linkedin Scraper", "Niya\'s Linkedin Scraper"))
        self.lineEdit.setText(_translate("Linkedin Scraper", ""))

    def gatherData(self, MainWindow):
        link = self.lineEdit.text()
        if link != "":
            data = linkedinScraper.scraper(link)
            self.textBrowser.setText(data)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
