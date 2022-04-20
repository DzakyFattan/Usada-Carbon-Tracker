import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from ui.register.register_widget import RegisterWindow
from ui.login.login_widget import LoginWindow
from ui.activity_main.activity_main_widget import ActivityMainWindow
from ui.tipsandtrick.tnt_widget import TNTMainWindow
from ui.membership.membership_widget import MembershipMainWindow
from ui.summary.summary_widget import SummaryMainWindow
from navigator import PageName, AccStatus
from process import credentials as cd


class MainWindow():
    def __init__(self, width, height):
        self.username = None
        self.accstatus = AccStatus.CUST
        self.app = QApplication(sys.argv)
        self.app.aboutToQuit.connect(self.logout_on_exit)
        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.setMinimumSize(width, height)
        self.widgets.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('ui/img/logo.png')))

        # PAGE BUILDING
        
        # 0. LOGIN
        window = LoginWindow(self)
        self.widgets.addWidget(window)
        # 1. REGISTER
        window = RegisterWindow(self)
        self.widgets.addWidget(window)
        # 2. ACTIVITY
        window = ActivityMainWindow(self)
        self.widgets.addWidget(window)

        window = SummaryMainWindow(self)
        self.widgets.addWidget(window)


        window = TNTMainWindow(self)
        self.widgets.addWidget(window)

        window = MembershipMainWindow(self)
        self.widgets.addWidget(window)
        # DEFAULT PAGE
        self.showPage(PageName.LOGIN)
        self.runApp()

    def logout(self):
        cd.logout_account(self.username)
        self.username = None
        self.showPage(PageName.LOGIN)

    def logout_on_exit(self):
        if self.username is not None:
            cd.logout_account(self.username)
        self.username = None

    def showPage(self, pageEnum):
        self.widgets.setCurrentIndex(pageEnum.value)
        # Window Title
        if pageEnum == PageName.LOGIN:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Login')
            # CLEANUP
            self.widgets.currentWidget().initpage()
        elif pageEnum == PageName.REGISTER:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Register')
            # CLEANUP
            self.widgets.currentWidget().lbl_register_feedback.setProperty('text', '')
        elif pageEnum == PageName.ACTIVITY:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Activity')
            self.widgets.currentWidget().clearLayout()
            self.widgets.currentWidget().fillScroll(0,10)
            # CLEANUP
        elif pageEnum == PageName.SUMMARY:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Summary')
            self.widgets.currentWidget().initpage()
        elif pageEnum == PageName.TIPSANDTRICK:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Tips & Trick')
            self.widgets.currentWidget().initpage(self.accstatus)
            # CLEANUP
        elif pageEnum == PageName.MEMBERSHIP:
            self.widgets.setWindowTitle('Usada Carbon Tracker - Membership')
            self.widgets.currentWidget().initpage(self.accstatus)
            # CLEANUP

        self.widgets.show()
    
    def runApp(self):
        self.app.exec()
def main():
    mainprogram = MainWindow(900, 786)
    
if __name__ == '__main__':
    main()