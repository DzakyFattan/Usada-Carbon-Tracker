from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from ui.login import login_rc
from navigator import PageName, AccStatus
from process import credentials as cd

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.programRef = programInstance
        super(LoginWindow, self).__init__()
        uic.loadUi('ui/login/login.ui', self)
        self.singleTimer = QTimer(self)
        self.singleTimer.setSingleShot(True)
        # for delay purpose

        # BINDING
        self.btn_login.clicked.connect(self.login_handler)
        self.lbl_signup.mousePressEvent = self.btn_register_handler

        # Modification
        signupfont = self.lbl_signup.font()
        signupfont.setUnderline(True)
        self.lbl_signup.setFont(signupfont)

    def initpage(self):
        self.lbl_login_feedback.setProperty('text', '')

    def btn_register_handler(self, event=None):
        self.programRef.showPage(PageName.REGISTER);

    def redir_to_act(self, event=None):
        self.programRef.showPage(PageName.ACTIVITY);
    def disableloginbutton(self):
        self.btn_login.setEnabled(False)
        self.btn_login.setProperty('text', 'Please Wait...')
        QTimer.singleShot(2000, self.enableloginbutton)
    
    def enableloginbutton(self):
        self.btn_login.setEnabled(True)
        self.btn_login.setProperty('text', 'Login')

    def login_handler(self):
        uname = self.inp_uname.text()
        pwd = self.inp_pwd.text()
        if cd.login_account(uname, pwd) == 0:
            self.lbl_login_feedback.setProperty('text', 'Login Success! Redirecting, Please Wait...')
            self.lbl_login_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(27, 209, 76); font-weight: bold;')
            self.programRef.username = uname
            self.programRef.accstatus = cd.get_account_status(uname)
            self.programRef.widgets.widget(5).firstbind(self.programRef.accstatus)
            self.singleTimer.timeout.connect(self.redir_to_act)
            self.disableloginbutton()
            self.singleTimer.start(2000)

        else:
            self.lbl_login_feedback.setProperty('text', 'Login Failed! Check your credentials!')
            self.lbl_login_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')

