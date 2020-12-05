from ModbusConnector import ModbusConnector
import time

Modbus = ModbusConnector()
send_command=20
Modbus.send_offset(send_command)
Modbus.read_offset()
