import csv  # import json
import os
from datetime import date

from PyQt6 import QtWidgets
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from saved_data_viewer import SavedDataViewer
from ui import main_form


class MainUI(QtWidgets.QMainWindow, main_form.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_baud_rate()
        self.setup_input_validation()
        self.save_button.clicked.connect(self.save_transmit_form_data)
        self.save_ethernet_button.clicked.connect(self.save_ethernet_form_data)
        self.actionOpenFi.triggered.connect(self.open_saved_data_viewer)

    def setup_baud_rate(self):
        baud_rates = [110, 150, 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
        for rate in baud_rates:
            self.baud_rate_combo_box.addItem(str(rate))

    def save_transmit_form_data(self):
        terminal_name = self.terminal_input.text()
        port_name = self.port_name_input.text()
        port_number = self.port_number_input.text()
        baud_rate = self.baud_rate_combo_box.currentText()
        data_bit = self.data_bit_combobox.currentText()
        parity_bit = self.parity_combobox.currentText()
        frame = self.frame_input.text()

        date_today = get_date()

        data = [terminal_name, port_name, port_number, baud_rate, data_bit, parity_bit, frame, date_today]
        data_header = ["Terminal Name", "Port Name", "Port Number", "Baud Rate", "Data Bits", "Parity Bits", "Frame",
                       "Date"]

        error_list = []
        if not terminal_name:
            error_list.append(data_header[0])
        if not port_name:
            error_list.append(data_header[1])
        if not port_number:
            error_list.append(data_header[2])
        if not frame:
            error_list.append(data_header[7])

        print(error_list)

        if error_list:
            msg = QtWidgets.QMessageBox()
            msg_grammar = "these inputs" if len(error_list) > 1 else "this input"
            nl = ',\n'
            msg.setText(f"Please check {msg_grammar}:\n\n{nl.join(error_list)}")
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            database_location = root_dir + "/data/storage/data.csv"
            csv_data = [data]
            with open(database_location, "a+") as file:
                writer = csv.writer(file)

                # Write header only if the file is empty.
                is_empty_file = os.stat(database_location).st_size == 0
                if is_empty_file:
                    writer.writerow(header for header in data_header)
                writer.writerows(csv_data)
                print("Saved data")

        print(terminal_name, port_name, port_number, baud_rate, data_bit, parity_bit, frame)

    def save_ethernet_form_data(self):
        terminal_name = self.ethernet_terminal_input.text()
        ip_address = self.ip_input.text()
        port_name = self.ethernet_port_name_input.text()
        port_number = self.ethernet_port_number_input.text()
        packet_size = self.packet_input.text()
        protocol = self.protocol_combobox.currentText()
        frame = self.ethernet_frame_input.text()

        date_today = get_date()

        data_header = ["Terminal Name", "IP Address", "Port Name", "Port Number", "Packet Size", "Protocol", "Frame",
                       "Date"]
        data = [terminal_name, ip_address, port_name, port_number, packet_size, protocol, frame, date_today]
        error_list = []
        if not terminal_name:
            error_list.append("Terminal Name")
        if not ip_address:
            error_list.append("IP Address")
        if not port_name:
            error_list.append("Port Name")
        if not port_number:
            error_list.append("Port Number")
        if not packet_size:
            error_list.append("Packet Size")
        if not frame:
            error_list.append("Frame")

        if error_list:
            msg = QtWidgets.QMessageBox()
            msg_grammar = "these inputs" if len(error_list) > 1 else "this input"
            nl = ',\n'
            msg.setText(f"Please check {msg_grammar}:\n\n{nl.join(error_list)}")
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            database_location = root_dir + "/data/storage/ethernet_data.csv"
            csv_data = [data]
            with open(database_location, "a+") as file:
                writer = csv.writer(file)
                # Write header only if the file is empty.
                is_empty_file = os.stat(database_location).st_size == 0
                if is_empty_file:
                    writer.writerow(header for header in data_header)
                writer.writerows(csv_data)
                print("Saved data")

    # Opens a different window to view the saved data
    # noinspection PyAttributeOutsideInit
    def open_saved_data_viewer(self):
        self.saved_data_window = SavedDataViewer()
        self.saved_data_window.show()

    def setup_input_validation(self):
        alphanumeric_validator = QRegularExpressionValidator(QRegularExpression(r"^\w+$"))
        self.terminal_input.setValidator(alphanumeric_validator)
        self.ethernet_terminal_input.setValidator(alphanumeric_validator)
        self.port_name_input.setValidator(alphanumeric_validator)
        self.ethernet_port_name_input.setValidator(alphanumeric_validator)

        decimal_validator = QRegularExpressionValidator(QRegularExpression(r"[0-9]+"))
        self.port_number_input.setValidator(decimal_validator)
        self.packet_input.setValidator(decimal_validator)
        self.ethernet_port_number_input.setValidator(decimal_validator)


def get_date():
    return date.today().strftime("%d/%m/%Y")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Avionics Protocol System")

    form = MainUI()
    form.show()
    app.exec()
