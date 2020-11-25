
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# vendor_id=6790, product_id=29987
# vendor_id=10755, product_id=67
# vendor_id=9025, product_id=67

class ModbusConnector(QSerialPort):
    
    def __init__(self, debug=False, vendor_id=9025, product_id=67):
        super().__init__()
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.available_to_use = False
        self.online = False
        self.debug = debug
        self.current_message = None

        if self.debug:
            print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print('Numero de portas seriais conectadas ao PC: {}'.format(
                len(QSerialPortInfo().availablePorts())))

        for port_info in QSerialPortInfo().availablePorts():
            if (port_info.hasVendorIdentifier() and
                    port_info.hasProductIdentifier()):
                if self.debug:
                    print(f"\nPorta:")
                    print(f"Vendor id: {port_info.vendorIdentifier()}")
                    print(f"Product id: {port_info.productIdentifier()}")
                if (port_info.vendorIdentifier() == vendor_id and
                        port_info.productIdentifier() == product_id):
                    self.port_name = port_info.portName()
                    self.available_to_use = True

        if self.available_to_use:
            if self.debug:
                print('\nDispositivo Modbus encontrado com sucesso!')
            self.setPortName(self.port_name)
            self.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            self.setDataBits(QSerialPort.Data8)
            self.setParity(QSerialPort.NoParity)
            self.setStopBits(QSerialPort.OneStop)
            self.setFlowControl(QSerialPort.NoFlowControl)

            # Apos todas as configuracoes tenta conectar com a porta serial
            if self.open(QSerialPort.ReadWrite):
                if self.debug:
                    print('\nComunicacao estabelecida com sucesso!')
            else:
                if self.debug:
                    print('\nErro: nao foi possivel estabelecer a comunicacao com o Modbus')
        else:
            if self.debug:
                print('\nAviso: dispositivo Modbus nao encontrado.')
                print('- - - - - - - - - - - - - - - - - - - - - - - - - - -\n')

        self.readyRead.connect(self.on_ready_read)

    def send_offset(self, offset):
        """ Envia o Offset. """
        if self.isOpen():
            if self.isWritable():
                if self.debug:
                    print('Enviando Offset: ')
                    print(offset)
                    self.write(offset)
                    print('Enviado com sucesso')

    # Slots
    def on_ready_read(self):
        while self.bytesAvailable():
            byte = self.read(1)