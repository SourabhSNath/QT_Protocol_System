from PyQt6 import QtWidgets

from ui import saved_data_window
import csv


class SavedDataViewer(QtWidgets.QDialog, saved_data_window.Ui_Dialog):
    def __init__(self):
        # https://stackoverflow.com/questions/22744102/pyqt4-why-do-we-need-to-pass-class-name-in-call-to-super
        # Not required to add the class name here. Keeping it for now.
        super(SavedDataViewer, self).__init__()
        self.setupUi(self)
