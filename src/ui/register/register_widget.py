from PyQt5 import QtWidgets, uic
from ui.register import register_rc
from navigator import PageName
from PyQt5.QtCore import QTimer
from process import credentials as cd
class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.programRef = programInstance
        super(RegisterWindow, self).__init__()
        uic.loadUi('ui/register/register.ui', self)
        self.singleTimer = QTimer(self)
        self.singleTimer.setSingleShot(True)
        # BINDING
        self.btn_register.clicked.connect(self.register_handler)
        self.lbl_backtologin_txt.mousePressEvent = self.back_to_login
        self.lbl_backtologin_logo.mousePressEvent = self.back_to_login
        self.cbox_showpwd.stateChanged.connect(self.show_pwd)

    def back_to_login(self, event=None):
        self.programRef.showPage(PageName.LOGIN);

    def show_pwd(self, state):
        if self.cbox_showpwd.isChecked():
            self.inp_pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.inp_pwd.setEchoMode(QtWidgets.QLineEdit.Password)

    def disableregisterbutton(self):
        self.btn_register.setEnabled(False)
        self.btn_register.setProperty('text', 'Please Wait...')
        QTimer.singleShot(2000, self.enableregisterbutton)

    def enableregisterbutton(self):
        self.btn_register.setEnabled(True)
        self.btn_register.setProperty('text', 'Register')
    
    def sanitizeemail(self, email):
        if email is None:
            return False
        if email.find('@') == -1:
            return False
        if email.find('.') == -1:
            return False
        return True

    def sanitizeusername(self, username):
        if username is None:
            return False
        if len(username) < 6:
            return False
        if len(username) > 20:
            return False
        return True

    def sanitizepassword(self, password):
        if password is None:
            return False
        if len(password) < 6:
            return False
        if len(password) > 20:
            return False
        return True
    def register_handler(self, event):
        email = self.inp_email.text()
        pwd = self.inp_pwd.text()
        uname = self.inp_uname.text()
        if not self.sanitizeemail(email):
            self.lbl_register_feedback.setProperty('text', 'Invalid Email')
            self.lbl_register_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizepassword(pwd):
            self.lbl_register_feedback.setProperty('text', 'Invalid Password, Must be 6-20 Characters')
            self.lbl_register_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizeusername(uname):
            self.lbl_register_feedback.setProperty('text', 'Invalid Username, Must be 6-20 Characters')
            self.lbl_register_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        else:
            if cd.register_account(uname, email, pwd) == 0:
                self.lbl_register_feedback.setProperty('text', 'Register Success! Redirecting, Please Wait...')
                self.lbl_register_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(27, 209, 76); font-weight: bold;')
                self.singleTimer.timeout.connect(self.back_to_login)
                self.disableregisterbutton()
                self.singleTimer.start(2000)
            else:
                self.lbl_register_feedback.setProperty('text', 'Register Failed! Check your credentials!')
                self.lbl_register_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')