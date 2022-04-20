from PyQt5 import QtWidgets, uic, QtCore, QtGui
from ui.activity_main import activity_main_rc
from navigator import PageName
from PyQt5.QtCore import QTimer
from datetime import datetime
from process import activity_history_module as ach
from process.activity_history_module import Category

class ActivityMainWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.programRef = programInstance
        self.startvindex = 0
        self.inonepage = 10
        super(ActivityMainWindow, self).__init__()
        uic.loadUi('ui/activity_main/activity_main.ui', self)
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
        self.startvindex = self.startvindex + self.inonepage if self.startvindex + self.inonepage < self.getACTlength() else self.startvindex
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

    # HELPER
    def getACTlength(self):
        return len(ach.get_all_tips_and_tricks(self.programRef.username))

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
    def btn_delete_action(self, tnt_id):
        ach.delete_activity(tnt_id)
        self.clearLayout(self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent"))
        if self.startvindex >= self.getACTlength():
            self.startvindex = self.startvindex - self.inonepage if self.startvindex - self.inonepage >= 0 else 0
        self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
    def btn_edit_action(self, dialog, activityid):
        dat = [i for i in ach.get_data_from_id(activityid)]
        nama = dialog.inp_name.text()
        jenis = dialog.dropdown_jenis.currentText()
        if self.sanitizejumlah(dialog.inp_amount.text()) and self.sanitizenama(nama):
            jumlah = int(dialog.inp_amount.text())
            waktu = dialog.inp_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            dat[2] = nama
            dat[3] = jenis
            if jenis == Category.Kendaraan:
                dat[4] = jumlah
                dat[5] = 0
            else:
                dat[4] = 0
                dat[5] = jumlah
            dat[6] = waktu
            ach.edit_activity(dat)
            self.clearLayout()
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
            dialog.close()
        else:
            dialog.lbl_feedback.setText("Nama tidak valid atau jumlah tidak valid.\nNama harus antara 6-20 karakter dan\njumlah harus angka di atas 0")
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        return

    def sanitizenama(self, nama):
        return 6 <= len(nama) and len(nama) <= 20
    def sanitizejumlah(self, jumlah):
        if jumlah.isnumeric():
            return int(jumlah) > 0
        else:
            return False
    def btn_add_action(self, dialog):
        username = self.programRef.username
        nama = dialog.inp_name.text()
        jenis = dialog.dropdown_jenis.currentText()
        jml_bensin = 0
        tot_watt = 0
        if self.sanitizejumlah(dialog.inp_amount.text()) and self.sanitizenama(nama):
            if jenis == Category.Kendaraan:
                jml_bensin = int(dialog.inp_amount.text())
            else :
                tot_watt = int(dialog.inp_amount.text())
            waktu = dialog.inp_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            tuple = (username, nama, jenis, jml_bensin, tot_watt, waktu)
            ach.add_activity(tuple)
            self.clearLayout()
            self.fillScroll(self.startvindex, self.startvindex + self.inonepage)
            dialog.close()
        else:
            dialog.lbl_feedback.setText("Nama tidak valid atau jumlah tidak valid.\nNama harus antara 6-20 karakter dan\njumlah harus angka di atas 0")
            dialog.lbl_feedback.setProperty('styleSheet', 'font-size: 9pt; color: rgb(255, 33, 33); font-weight: bold;')
        return
    def openEditWindow(self, activityid):
        dat = ach.get_data_from_id(activityid)
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/activity_main/activity_update.ui', newDialog)
        newDialog.dropdown_jenis.addItem(Category.Kendaraan)
        newDialog.dropdown_jenis.addItem(Category.Elektronik)
        newDialog.setWindowTitle("Edit Activity")
        newDialog.btn_update.clicked.connect(lambda: self.btn_edit_action(newDialog, activityid))
        newDialog.btn_cancel.clicked.connect(newDialog.close)
        newDialog.dropdown_jenis.setCurrentText(dat[3])
        newDialog.inp_name.setText(dat[2])
        if dat[3] == Category.Kendaraan:
            newDialog.inp_amount.setText(f"{dat[4]}")
        else:
            newDialog.inp_amount.setText(f"{dat[5]}")
        newDialog.inp_datetime.setDateTime(QtCore.QDateTime.fromString(dat[6], "yyyy-MM-dd HH:mm:ss"))
        newDialog.show()

    def openAddWindow(self):
        newDialog = QtWidgets.QDialog(self)
        newDialog.setMinimumSize(800, 500)
        uic.loadUi('ui/activity_main/activity_add.ui', newDialog)
        newDialog.dropdown_jenis.addItem(Category.Kendaraan)
        newDialog.dropdown_jenis.addItem(Category.Elektronik)
        newDialog.setWindowTitle("Add Activity")
        newDialog.btn_add.clicked.connect(lambda: self.btn_add_action(newDialog))
        newDialog.btn_cancel.clicked.connect(newDialog.close)
        datenow = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        newDialog.inp_datetime.setDateTime(QtCore.QDateTime.fromString(datenow, "yyyy/MM/dd HH:mm:ss"))
        newDialog.show()

    def buildEntry(self, id_act, name, category, amount, datetimestr):
        framestyle = QtWidgets.QWidget()
        framestyle.setObjectName(f"act_entry_{id_act}")
        framestyle.setProperty("styleSheet",
            f"""
            QWidget#act_entry_{id_act} {{
            border-width: 2px; 
            border-style: solid; 
            padding: 3px;
            border-color: rgb(179, 191, 232) rgb(179, 191, 232)  rgb(179, 191, 232) rgb(179, 191, 232);
            }}
            """
        )

        horibox = QtWidgets.QHBoxLayout()
        keterangan = QtWidgets.QLabel()
        if category == Category.Elektronik:
            keterangan.setText(f"{name}\n{category} | {amount}W\n{datetimestr}")
        else:
            keterangan.setText(f"{name}\n{category} | {amount}L\n{datetimestr}")
        keterangan.setProperty("styleSheet", "border: none; font-size: 12pt; color: rgb(179, 191, 232); font-weight: Bold;")
        keterangan.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        editBtn = QtWidgets.QPushButton()
        editBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        editBtn.clicked.connect(self.edit_clicked)
        editBtn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        editBtn.setText("EDIT")
        editBtn.setObjectName(f"editBtn_{id_act}")
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
        delBtn.setObjectName(f"delBtn_{id_act}")
        delBtn.setProperty("styleSheet",
            """
            font-size: 15pt; background-color: rgb(179, 191, 232); font-weight: Bold;
            color: rgb(54, 54, 54);
            background-color: rgb(244, 113, 116);
            padding: 5px 20px 5px 20px;
            """
        )
        horibox.addWidget(keterangan)
        horibox.addWidget(editBtn)
        horibox.addWidget(delBtn)
        framestyle.setLayout(horibox)
        return framestyle
    
    def fillScroll(self, startid, endid):
        vcontent = self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent")
        if self.getACTlength() > 0:
            startid = startid if startid > 0 else 0
            endid = endid if endid < self.getACTlength() else self.getACTlength()
            dat = ach.get_all_tips_and_tricks(self.programRef.username)
            for i in range(startid, endid):
                if dat[i][3] == Category.Elektronik:
                    vcontent.addWidget(self.buildEntry(dat[i][0], dat[i][2], dat[i][3], dat[i][5], dat[i][6]))
                else:
                    vcontent.addWidget(self.buildEntry(dat[i][0], dat[i][2], dat[i][3], dat[i][4], dat[i][6]))
            vcontent.addStretch()
        else:
            label = QtWidgets.QLabel("Empty Data")
            label.setObjectName("label_empty")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setProperty("styleSheet", "border: none; font-size: 20pt; color: rgb(179, 191, 232); font-weight: Bold;")
            vcontent.addWidget(label)
        