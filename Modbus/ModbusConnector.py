# Standard Library
import time

# Third party modules
import minimalmodbus

# Local application imports


class ModbusConnector(minimalmodbus.Instrument):
    def __init__(self, port: str='COM3', slaveaddress: int=1,
                 close_port_after_each_call: bool=False, debug: bool=False):
        minimalmodbus.Instrument.__init__(self, port, slaveaddress)
        self.serial.baudrate = 19200
        self.serial.bytesize = 8
        self.serial.stopbits = 1
        self.serial.timeout = 1  # segundos

        self.mode = 'rtu'
        self.close_port_after_each_call = close_port_after_each_call
        self.debug = debug
        self.usb_on = True
        self.register = 0

        if self.debug:
            print(self)

        time.sleep(2)

    def send_offset(self, offset: float) -> None:
        if self.usb_on:
            self.write_register(0, offset if offset >= 0 else offset + 65535)
            if self.debug:
                print(f'Offset {offset}mm enviado com sucesso')

    def read_offset(self) -> None:
        if self.usb_on:
            test_reg = self.read_registers(0, 1, 4)
            if self.debug:
                print(f'Recebido offset {test_reg}')
