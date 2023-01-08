from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LinkedinScraper(object):
    def setupUi(self, LinkedinScraper):
        LinkedinScraper.setObjectName("LinkedinScraper")
        LinkedinScraper.resize(840, 600)
        self.centralwidget = QtWidgets.QWidget(LinkedinScraper)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 240, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 80, 151, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(330, 130, 281, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(210, 290, 411, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 130, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 160, 91, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(330, 160, 281, 21))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 190, 71, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(330, 190, 281, 21))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        LinkedinScraper.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LinkedinScraper)
        self.statusbar.setObjectName("statusbar")
        LinkedinScraper.setStatusBar(self.statusbar)

        self.retranslateUi(LinkedinScraper)
        QtCore.QMetaObject.connectSlotsByName(LinkedinScraper)

    def retranslateUi(self, LinkedinScraper):
        _translate = QtCore.QCoreApplication.translate
        LinkedinScraper.setWindowTitle(_translate("LinkedinScraper", "MainWindow"))
        self.pushButton.setText(_translate("LinkedinScraper", "Gather Data"))
        self.label.setText(_translate("LinkedinScraper", "Niya\'s Linkedin Scraper"))
        self.textBrowser.setHtml(_translate("LinkedinScraper", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_2.setText(_translate("LinkedinScraper", "Profile Link:"))
        self.label_3.setText(_translate("LinkedinScraper", "Email Address:"))
        self.label_4.setText(_translate("LinkedinScraper", "Password:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LinkedinScraper = QtWidgets.QMainWindow()
    ui = Ui_LinkedinScraper()
    ui.setupUi(LinkedinScraper)
    LinkedinScraper.show()
    sys.exit(app.exec_())
