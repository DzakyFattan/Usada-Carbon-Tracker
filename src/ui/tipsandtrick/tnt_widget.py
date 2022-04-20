from PyQt5 import QtWidgets, uic, QtCore, QtGui
from ui.tipsandtrick import tnt_rc
from navigator import PageName, AccStatus
from PyQt5.QtCore import QTimer
from process import tips_and_tricks_module as tnth
from datetime import datetime as dt

class TNTMainWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.startvindex = 0
        self.inonepage = 10
        self.programRef = programInstance
        super(TNTMainWindow, self).__init__()
        uic.loadUi('ui/tipsandtrick/tnt_main.ui', self)
        self.singleTimer = QTimer(self)
        self.singleTimer.setSingleShot(True)
        # BINDING

        self.btn_activity.clicked.connect(self.btn_activity_clicked)
        self.btn_summary.clicked.connect(self.btn_summary_clicked)
        self.btn_tnt.clicked.connect(self.btn_tnt_clicked)
        self.btn_membership.clicked.connect(self.btn_membership_clicked)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
        self.btn_tambah.clicked.connect(self.btn_tambah_clicked)
        self.entry_next.mousePressEvent = self.entry_next_clicked
        self.entry_prev.mousePressEvent = self.entry_prev_clicked


    def initpage(self, accountstatus):
        self.clearLayout()
        if accountstatus == AccStatus.ADMIN:
            self.btn_tambah.show()
            self.entry_prev.setHidden(False)
            self.entry_next.setHidden(False)
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        elif accountstatus == AccStatus.MEMBER:
            self.btn_tambah.hide()
            self.entry_prev.setHidden(False)
            self.entry_next.setHidden(False)
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        else:
            self.btn_tambah.hide()
            self.entry_prev.setHidden(True)
            self.entry_next.setHidden(True)
            label = QtWidgets.QLabel("Anda tidak memiliki akses\nuntuk halaman ini")
            label.setObjectName("label_noaccess")
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

    def btn_tambah_clicked(self):
        self.openAddWindow()

    def entry_next_clicked(self, event=None):
        self.clearLayout()
        self.startvindex = self.startvindex + self.inonepage if self.startvindex + self.inonepage < self.getTNTlength() else self.startvindex
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        return
    def entry_prev_clicked(self, event=None):
        self.clearLayout()
        self.startvindex = self.startvindex - self.inonepage if self.startvindex - self.inonepage >= 0 else 0
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
        return

    def edit_clicked(self, event=None):
        self.openEditWindow(int(self.sender().objectName()[8:]))
        return

    def delete_clicked(self, event=None):
        tnt_id = int(self.sender().objectName()[7:])
        self.btn_delete_action(tnt_id)
        return
    def view_clicked(self, event=None):
        # self.openDetail(int(self.sender().objectName()[11:])) # BUAT PLACEHOLDER EVENT LISTENER
        return

    # HELPER
    def sanitizejudul(self, judul):
        return 10 <= len(judul) and len(judul) <= 30
    def sanitizesubtitle(self, judul):
        return 10 <= len(judul) and len(judul) <= 30
    def sanitizecontent(self, content):
        return len(content) >= 10
    def getTNTlength(self):
        return len(tnth.get_all_tips_and_tricks())

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

    def btn_update_action(self, dialog, tnt_id, tstmp):
        title = dialog.inp_title.text()
        subtitle = dialog.inp_subtitle.text()
        content = dialog.inp_content.toPlainText()
        if not self.sanitizejudul(title):
            dialog.lbl_feedback.setProperty('text', 'Judul tidak valid\n(min. 10, max. 30 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizesubtitle(subtitle):
            dialog.lbl_feedback.setProperty('text', 'Subjudul tidak valid\n(min. 10, max. 30 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizecontent(content):
            dialog.lbl_feedback.setProperty('text', 'Konten tidak valid\n(min. 10 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        else:
            tuple = [tnt_id, title, subtitle, content, tstmp]
            tnth.edit_tips_tricks_data(tuple)
            self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
            dialog.close()

    def btn_delete_action(self, tnt_id):
        tnth.del_tips_tricks_by_id(tnt_id)
        self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
        if self.startvindex >= self.getTNTlength():
            self.startvindex = self.startvindex - self.inonepage if self.startvindex - self.inonepage >= 0 else 0
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)

    def btn_add_action(self, dialog, tstmp):
        title = dialog.inp_title.text()
        subtitle = dialog.inp_subtitle.text()
        content = dialog.inp_content.toPlainText()
        if not self.sanitizejudul(title):
            dialog.lbl_feedback.setProperty('text', 'Judul tidak valid\n(min. 10, max. 30 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizesubtitle(subtitle):
            dialog.lbl_feedback.setProperty('text', 'Subjudul tidak valid\n(min. 10, max. 30 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        elif not self.sanitizecontent(content):
            dialog.lbl_feedback.setProperty('text', 'Konten tidak valid\n(min. 10 karakter)')
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        else:
            tuple = [title, subtitle, content, tstmp]
            tnth.add_tips_tricks_data(tuple)
            self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
            dialog.close()
            

    def openEditWindow(self, tnt_id):
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/tipsandtrick/tnt_edit.ui', newDialog)
        newDialog.setWindowTitle("Edit Tips and Trick")
        newDialog.btn_cancel.clicked.connect(newDialog.close)
        dat = tnth.get_tips_tricks_by_id(tnt_id)

        newDialog.inp_title.setText(dat[1])
        newDialog.inp_subtitle.setText(dat[2])
        newDialog.inp_content.setPlainText(dat[3])
        newDialog.btn_edit.clicked.connect(lambda: self.btn_update_action(newDialog, tnt_id, dat[4]))
        newDialog.show()

    def openAddWindow(self):
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/tipsandtrick/tnt_add.ui', newDialog)
        newDialog.setWindowTitle("Add Tips and Trick")
        newDialog.btn_cancel.clicked.connect(newDialog.close)
        newDialog.btn_add.clicked.connect(lambda: self.btn_add_action(newDialog, dt.now().strftime("%Y-%m-%d %H:%M:%S")))
        newDialog.show()
    
    def openDetail(self, tnt_id):
        dat = tnth.get_tips_tricks_by_id(tnt_id)
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/tipsandtrick/tnt_view.ui', newDialog)
        newDialog.setWindowTitle(dat[1])
        newDialog.btn_cancel.clicked.connect(newDialog.close)
        newDialog.lbl_title.setText(dat[1])
        newDialog.lbl_subtitle.setText(dat[2])
        newDialog.text_content.setPlainText(dat[3])
        newDialog.lbl_date.setText(dat[4])
        newDialog.show()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source.objectName()[:11] == "keterangan_":
            self.openDetail(int(source.objectName()[11:]))
            
        return super(TNTMainWindow, self).eventFilter(source, event)

    def buildEntry(self, id_tnt, title, subtitle, timestamp):
        framestyle = QtWidgets.QWidget()
        framestyle.setObjectName(f"act_entry_{id_tnt}")
        framestyle.setProperty("styleSheet",
            f"""
            QWidget#act_entry_{id_tnt} {{
            border-width: 2px; 
            border-style: solid; 
            padding: 3px;
            border-color: rgb(179, 191, 232) rgb(179, 191, 232)  rgb(179, 191, 232) rgb(179, 191, 232);
            }}
            """
        )

        horibox = QtWidgets.QHBoxLayout()
        keterangan = QtWidgets.QLabel()
        keterangan.setObjectName(f"keterangan_{id_tnt}")
        keterangan.mousePressEvent = self.view_clicked
        keterangan.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        keterangan.setText(f"{title}\n{subtitle}\n{timestamp}")
        keterangan.installEventFilter(self)
        keterangan.setProperty("styleSheet", "border: none; font-size: 12pt; color: rgb(179, 191, 232); font-weight: Bold;")
        keterangan.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        editBtn = QtWidgets.QPushButton()
        editBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        editBtn.clicked.connect(self.edit_clicked)
        editBtn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        editBtn.setText("EDIT")
        editBtn.setObjectName(f"editBtn_{id_tnt}")
        editBtn.setProperty("styleSheet",
            """
            font-size: 15pt; background-color: rgb(179, 191, 232); font-weight: Bold;
            color: rgb(54, 54, 54);
            padding: 5px 20px 5px 20px;
            """
        )

        delBtn = QtWidgets.QPushButton()
        delBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        delBtn.clicked.connect(self.delete_clicked)
        delBtn.setText("DELETE")
        delBtn.setObjectName(f"delBtn_{id_tnt}")
        delBtn.setProperty("styleSheet",
            """
            font-size: 15pt; background-color: rgb(179, 191, 232); font-weight: Bold;
            color: rgb(54, 54, 54);
            background-color: rgb(244, 113, 116);
            padding: 5px 20px 5px 20px;
            """
        )

        horibox.addWidget(keterangan)
        if self.programRef.accstatus == AccStatus.ADMIN:
            horibox.addWidget(editBtn)
            horibox.addWidget(delBtn)
        framestyle.setLayout(horibox)
        return framestyle
    
    def fillScroll(self, startid, endid):
        vcontent = self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent")
        if self.getTNTlength() > 0:
            startid = startid if startid > 0 else 0
            endid = endid if endid < self.getTNTlength() else self.getTNTlength()
            dat = tnth.get_all_tips_and_tricks()
            for i in range(startid, endid):
                vcontent.addWidget(self.buildEntry(dat[i][0], dat[i][1], dat[i][2], dat[i][4]))
            vcontent.addStretch()
        else:
            label = QtWidgets.QLabel("Empty Data")
            label.setObjectName("label_empty")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            vcontent.addWidget(label)
        