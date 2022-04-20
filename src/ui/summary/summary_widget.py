from PyQt5 import QtWidgets, uic, QtCore, QtGui
from ui.summary import sum_rc
from navigator import PageName, AccStatus
from PyQt5.QtCore import QTimer
from process import activity_history_module as acth
from datetime import datetime as dt

class SummaryMainWindow(QtWidgets.QMainWindow):
    def __init__(self, programInstance):
        self.programRef = programInstance
        super(SummaryMainWindow, self).__init__()
        uic.loadUi('ui/summary/summary.ui', self)
        self.singleTimer = QTimer(self)
        self.singleTimer.setSingleShot(True)
        # BINDING
        self.detailLayout = self.mainScroll.findChild(QtWidgets.QGridLayout, "details")
        self.pieChartLayout = self.mainScroll.findChild(QtWidgets.QVBoxLayout, "vcontent").findChild(QtWidgets.QHBoxLayout, "HBoxPieChart")
        self.interval_entry.currentTextChanged.connect(self.fillDat)
        self.interval_entry.addItem("Today")
        self.interval_entry.addItem("This Week")
        self.interval_entry.addItem("This Month")
        self.interval_entry.addItem("This Year")
        self.interval_entry.addItem("All Time")

        self.btn_activity.clicked.connect(self.btn_activity_clicked)
        self.btn_summary.clicked.connect(self.btn_summary_clicked)
        self.btn_tnt.clicked.connect(self.btn_tnt_clicked)
        self.btn_membership.clicked.connect(self.btn_membership_clicked)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)


    def initpage(self):
        self.interval_entry.setCurrentText("Today")
        self.fillDat()
        return
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

    # HELPER
    def getACTlength(self):
        return len(acth.get_all_tips_and_tricks(self.programRef.username))

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
    
    def fillDat(self, interval=None):
        if interval is None:
            interval = self.interval_entry.currentText()
        # self.clearLayout(self.pieChartLayout)
        intervaln = 1
        if interval == "Today":
            intervaln = 1
        elif interval == "This Week":
            intervaln = 7
        elif interval == "This Month":
            intervaln = 30
        elif interval == "This Year":
            intervaln = 365
        elif interval == "All Time":
            intervaln = -1
        if self.getACTlength() > 0:
            totalEmi = acth.get_total_emission(self.programRef.username, intervaln)
            totalSum = acth.get_total_sum(self.programRef.username, intervaln)
            totalCount = acth.get_total_count(self.programRef.username, intervaln)

            self.total_entry.setText(f"{totalEmi[0] + totalEmi[1]:.2f} KgCO2 ({totalCount[0] + totalCount[1]} Activities)")
            self.electronic_entry.setText(f"{totalEmi[1]:.2f} KgCO2 ({totalCount[1]} Activities)")
            self.fuel_entry.setText(f"{totalEmi[0]:.2f} KgCO2 ({totalCount[0]} Activities)")
            self.grade_entry.setText(f"{acth.get_grades(self.programRef.username, intervaln)}")
        else:
            self.total_entry.setText("Data Empty")
            self.electronic_entry.setText("Data Empty")
            self.fuel_entry.setText("Data Empty")
            self.grade_entry.setText("Data Empty")