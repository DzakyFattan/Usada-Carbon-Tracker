from PyQt5 import QtWidgets, uic, QtCore, QtGui
from ui.membership import membership_rc
from navigator import PageName, AccStatus
from PyQt5.QtCore import QTimer
from process import membership_module as mbmh
from datetime import datetime as dt

class MembershipMainWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.startvindex = 0
        self.inonepage = 10
        self.programRef = programInstance
        super(MembershipMainWindow, self).__init__()
        self.singleTimer = QTimer(self)
        self.singleTimer.setSingleShot(True)
        # BINDING


    def firstbind(self, accountstatus):
        if self.programRef.accstatus == AccStatus.CUST:
            uic.loadUi("ui/membership/membership_nonadm.ui", self)
            self.btn_send.clicked.connect(self.btn_send_clicked)
        else:
            uic.loadUi("ui/membership/membership_adm.ui", self)
            self.entry_next.mousePressEvent = self.entry_next_clicked
            self.entry_prev.mousePressEvent = self.entry_prev_clicked

        self.btn_activity.clicked.connect(self.btn_activity_clicked)
        self.btn_summary.clicked.connect(self.btn_summary_clicked)
        self.btn_tnt.clicked.connect(self.btn_tnt_clicked)
        self.btn_membership.clicked.connect(self.btn_membership_clicked)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
    def initpage(self, accountstatus):
        if accountstatus == AccStatus.ADMIN:
            self.clearLayout()
            self.entry_prev.setHidden(False)
            self.entry_next.setHidden(False)
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        elif accountstatus == AccStatus.CUST:
            detail = mbmh.get_acc_by_uname(self.programRef.username)
            self.lbl_telp_entry.setText(detail[4])
            self.lbl_cc_entry.setText(detail[3])
        elif accountstatus == AccStatus.PENDING:
            self.entry_prev.setHidden(True)
            self.entry_next.setHidden(True)
            self.clearLayout()
            label = QtWidgets.QLabel("Permintaan sedang diproses")
            label.setObjectName("label_pending")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent").addWidget(label)
        else:
            self.entry_prev.setHidden(True)
            self.entry_next.setHidden(True)
            self.clearLayout()
            label = QtWidgets.QLabel("Anda sudah menjadi member")
            label.setObjectName("label_already_member")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent").addWidget(label)
    # BUTTON HANDLER
    def btn_activity_clicked(self):
        self.programRef.showPage(PageName.ACTIVITY)
        return

    def btn_summary_clicked(self):
        self.programRef.showPage(PageName.SUMMARY)
    def btn_tnt_clicked(self):
        self.programRef.showPage(PageName.TIPSANDTRICK)
    def btn_membership_clicked(self):
        self.programRef.showPage(PageName.MEMBERSHIP)
        return
    def btn_logout_clicked(self):
        self.programRef.logout()
        return
    def sanitizetelpnumber(self, notelp):
        return notelp.isnumeric() and len(notelp) > 0
    
    def sanitizecc(self, cc):
        return len(cc) > 0
    def btn_send_clicked(self):
        uname = self.programRef.username
        telp = self.lbl_telp_entry.text()
        cc = self.lbl_cc_entry.text()
        if not self.sanitizetelpnumber(telp):
            self.lbl_feedback.setText("Telepon tidak valid.")
            self.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizecc(cc):
            self.lbl_feedback.setText("Kartu kredit tidak valid.")
            self.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        else:
            self.programRef.accstatus = AccStatus.PENDING
            mbmh.request_membership(uname, telp, cc)
            uic.loadUi("ui/membership/membership_adm.ui", self)
            self.entry_prev.setHidden(True)
            self.entry_next.setHidden(True)
            self.btn_activity.clicked.connect(self.btn_activity_clicked)
            self.btn_summary.clicked.connect(self.btn_summary_clicked)
            self.btn_tnt.clicked.connect(self.btn_tnt_clicked)
            self.btn_membership.clicked.connect(self.btn_membership_clicked)
            self.btn_logout.clicked.connect(self.btn_logout_clicked)
            self.clearLayout()
            label = QtWidgets.QLabel("Permintaan sedang diproses")
            label.setObjectName("label_pending")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent").addWidget(label)

    def entry_next_clicked(self, event=None):
        self.clearLayout()
        self.startvindex = self.startvindex + self.inonepage if self.startvindex + self.inonepage < self.getMBMlength() else self.startvindex
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        return
    def entry_prev_clicked(self, event=None):
        self.clearLayout()
        self.startvindex = self.startvindex - self.inonepage if self.startvindex - self.inonepage >= 0 else 0
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        return

    def reject_clicked(self, event=None, dialog=None):
        self.btn_reject_action(self.sender().objectName()[11:], dialog)
        return

    def accept_clicked(self, event=None, dialog=None): # btn_accept_
        self.btn_accept_action(self.sender().objectName()[11:], dialog)
        return
    def view_detail(self, event=None):
        req_id = int(self.sender().objectName()[10:])
        self.openDetail(req_id)
        return

    # HELPER
    def getMBMlength(self):
        return len(mbmh.get_all_pending_membership())

    def clearLayout(self, layout=None):
        if layout is None:
            layout = self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent")
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def btn_reject_action(self, username, dialog):
        mbmh.reject_membership(username)
        self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        dialog.close()

    def btn_accept_action(self, username, dialog):
        mbmh.accept_membership(username)
        self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
        if self.startvindex >= self.getMBMlength():
            self.startvindex = self.startvindex - self.inonepage if self.startvindex - self.inonepage >= 0 else 0
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        dialog.close()

    
    def openDetail(self, req_id):
        dat = mbmh.get_pending_membership_by_id(req_id)
        detail = mbmh.get_acc_by_uname(dat[1])
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/membership/membership_detail.ui', newDialog)
        newDialog.setWindowTitle(dat[1])
        newDialog.btn_reject.clicked.connect(lambda: self.reject_clicked(dialog=newDialog))
        newDialog.btn_reject.setObjectName(f"btn_reject_{detail[0]}")
        newDialog.btn_accept.clicked.connect(lambda: self.accept_clicked(dialog=newDialog))
        newDialog.btn_accept.setObjectName(f"btn_accept_{detail[0]}")
        newDialog.lbl_uname_entry.setText(detail[0])
        newDialog.lbl_telp_entry.setText(detail[4])
        newDialog.lbl_cc_entry.setText(detail[3])
        newDialog.show()
            

    def buildEntry(self, req_id, username, timestamp):
        framestyle = QtWidgets.QWidget()
        framestyle.setObjectName(f"act_entry_{req_id}")
        framestyle.setProperty("styleSheet",
            f"""
            QWidget#act_entry_{req_id} {{
            border-width: 2px; 
            border-style: solid; 
            padding: 3px;
            border-color: rgb(179, 191, 232) rgb(179, 191, 232)  rgb(179, 191, 232) rgb(179, 191, 232);
            }}
            """
        )

        horibox = QtWidgets.QHBoxLayout()
        keterangan = QtWidgets.QLabel()
        keterangan.setObjectName(f"keterangan_{req_id}")
        keterangan.setText(f"{username}\n{timestamp}")
        keterangan.setProperty("styleSheet", "border: none; font-size: 12pt; color: rgb(179, 191, 232); font-weight: Bold;")
        keterangan.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        detailBtn = QtWidgets.QPushButton()
        detailBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        detailBtn.clicked.connect(self.view_detail)
        detailBtn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        detailBtn.setText("Detail")
        detailBtn.setObjectName(f"detailBtn_{req_id}")
        detailBtn.setProperty("styleSheet",
            """
            font-size: 15pt; background-color: rgb(179, 191, 232); font-weight: Bold;
            color: rgb(54, 54, 54);
            padding: 5px 20px 5px 20px;
            """
        )

        if self.programRef.accstatus == AccStatus.ADMIN:
            horibox.addWidget(keterangan)
            horibox.addWidget(detailBtn)
            framestyle.setLayout(horibox)
        return framestyle
    
    def fillScroll(self, startid, endid):
        vcontent = self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent")
        if self.getMBMlength() > 0:
            startid = startid if startid > 0 else 0
            endid = endid if endid < self.getMBMlength() else self.getMBMlength()
            dat = mbmh.get_all_pending_membership()
            for i in range(startid, endid):
                vcontent.addWidget(self.buildEntry(dat[i][0], dat[i][1], dat[i][2]))
            vcontent.addStretch()
        else:
            label = QtWidgets.QLabel("Empty Data")
            label.setObjectName("label_empty")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            vcontent.addWidget(label)
        