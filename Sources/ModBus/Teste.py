
from ModbusConnector import ModbusConnector
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import sys
import time

app = QApplication(sys.argv)
Window = QMainWindow()
Window.show()

Modbus = ModbusConnector(debug=True)
send_command=b'A'
Modbus.send_offset(send_command)
# time.sleep(2)
# Modbus.receive()
# Modbus.close()
sys.exit(app.exec_())
































