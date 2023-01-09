import validators
from PyQt5 import QtCore, QtGui, QtWidgets

import linkedinScraper

class scraper(object):
    def setup(self, mainWindow):

        mainWindow.setObjectName("LinkedinScraper")
        mainWindow.resize(840, 600)

        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        mainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 240, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.gatherData)

        self.scraperLabel = QtWidgets.QLabel(self.centralwidget)
        self.scraperLabel.setGeometry(QtCore.QRect(340, 80, 151, 16))
        self.scraperLabel.setObjectName("scraperLabel")

        self.profileLabel = QtWidgets.QLabel(self.centralwidget)
        self.profileLabel.setGeometry(QtCore.QRect(250, 130, 71, 16))
        self.profileLabel.setObjectName("profileLabel")

        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setGeometry(QtCore.QRect(230, 160, 91, 20))
        self.emailLabel.setObjectName("emailLabel")

        self.passLabel = QtWidgets.QLabel(self.centralwidget)
        self.passLabel.setGeometry(QtCore.QRect(260, 190, 71, 16))
        self.passLabel.setObjectName("passLabel")

        self.profileLink = QtWidgets.QLineEdit(self.centralwidget)
        self.profileLink.setGeometry(QtCore.QRect(330, 130, 281, 21))
        self.profileLink.setText("")
        self.profileLink.setObjectName("profileLink")

        self.email = QtWidgets.QLineEdit(self.centralwidget)
        self.email.setGeometry(QtCore.QRect(330, 160, 281, 21))
        self.email.setText("")
        self.email.setObjectName("email")

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(330, 190, 281, 21))
        self.password.setText("")
        self.password.setObjectName("password")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(210, 290, 411, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.setInitialText(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def setInitialText(self, LinkedinScraper):
        _translate = QtCore.QCoreApplication.translate
        LinkedinScraper.setWindowTitle("Linkedin Scraper")
        self.pushButton.setText(_translate("LinkedinScraper", "Gather Data"))
        self.scraperLabel.setText(_translate("LinkedinScraper", "Niya\'s Linkedin Scraper"))
        self.profileLabel.setText(_translate("LinkedinScraper", "Profile Link:"))
        self.emailLabel.setText(_translate("LinkedinScraper", "Email Address:"))
        self.passLabel.setText(_translate("LinkedinScraper", "Password:"))

    def gatherData(self, mainWindow):
        userEmail = self.email.text()
        userPass = self.password.text()
        link = self.profileLink.text()
        validURL = validators.url(link)
        if not validURL:
            print("The link you have provided is not valid, please try again")
            self.profileLink.setText("")
        else:
            data = linkedinScraper.scraper(userEmail, userPass, link)
            self.textBrowser.setText(data)
            self.textBrowser.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = scraper()
    ui.setup(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
