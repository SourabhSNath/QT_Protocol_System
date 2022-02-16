import csv
import os

from PyQt6 import QtWidgets, QtCore

from ui import saved_data_window


class SavedDataViewer(QtWidgets.QMainWindow, saved_data_window.Ui_MainWindow):
    def __init__(self):
        # https://stackoverflow.com/questions/22744102/pyqt4-why-do-we-need-to-pass-class-name-in-call-to-super
        # Not required to add the class name here. Keeping it for now.
        super(SavedDataViewer, self).__init__()
        self.setupUi(self)

        self.date_input.setDate(QtCore.QDate.currentDate())
        self.search_button.clicked.connect(self.search_data)

    def search_data(self):
        data_type = self.type_combobox.currentText()

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            if data_type == "Transmit Terminal":
                database_location = root_dir + "/data/storage/data.csv"
                self.load_data(database_location)
            else:
                database_location = root_dir + "/data/storage/ethernet_data.csv"
                self.load_data(database_location)
        except FileNotFoundError as e:
            print(e)

    def load_data(self, database_location):
        input_date = self.date_input.date()

        rows = []
        with open(database_location, "r") as file:
            reader = csv.reader(file)
            # Extracting field names through first row.
            fields = next(reader)
            # Extract data in each row
            for row in reader:
                rows.append(row)

            print(f"Total rows: {reader.line_num}")

        print(f"Field Names: {fields}")
        print(rows)

        num_cols = len(fields)
        num_rows = len(rows)
        print(f"Number of rows {num_rows}, Cols {num_cols}")

        self.data_table.setColumnCount(num_cols)
        self.data_table.setHorizontalHeaderLabels(fields)
        self.data_table.setRowCount(num_rows)

        for row in range(num_rows):
            print(f"Row {row}")
            for col in range(num_cols):
                print(f"Col {col}")
                self.data_table.setItem(row, col, QtWidgets.QTableWidgetItem(rows[row][col]))
                # self.data_table.setItem(row, col, QtWidgets.QTableWidgetItem("Wololo"))

                print(rows[row][col], type(rows[row][col]), end=",")

