
from Modbus_connector import ModbusConnector
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import sys
import time

app = QApplication(sys.argv)
Window = QMainWindow()
Window.show()

Modbus = ModbusConnector(debug=True)
send_command=b'Aaa'
Modbus.send(send_command)
# time.sleep(2)
# Modbus.receive()
# Modbus.close()
sys.exit(app.exec_())
































