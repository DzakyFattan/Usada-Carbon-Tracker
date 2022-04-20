from enum import Enum

class PageName(Enum):
    LOGIN = 0
    REGISTER = 1
    ACTIVITY = 2
    SUMMARY = 3
    TIPSANDTRICK = 4
    MEMBERSHIP = 5
    LOGOUTFEEDBACK = 6

class AccStatus():
    ADMIN = "ADMIN"
    CUST = "CUSTOMER"
    MEMBER = "MEMBER"
    PENDING = "PENDING"