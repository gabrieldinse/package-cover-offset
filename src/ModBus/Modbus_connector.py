
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class ModbusConnector(QSerialPort):
    
    def __init__(self, debug=False, vendor_id=10755, product_id=67):
        super().__init__()
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.available_to_use = False
        self.sendmessage = ""
        self.receivemessage = ""
        self.online = False
        self.debug = debug

        if self.debug:
            print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print('Numero de portas seriais conectadas ao PC: {}'.format(
                len(QSerialPortInfo().availablePorts())))

        for port_info in QSerialPortInfo().availablePorts():
            if (port_info.hasVendorIdentifier() and
                    port_info.hasProductIdentifier()):
                if (port_info.vendorIdentifier() == vendor_id and
                        port_info.productIdentifier() == product_id):
                    self.port_name = port_info.portName()
                    self.available_to_use = True

        if self.available_to_use:
            if self.debug:
                print('Dispositivo Modbus encontrado com sucesso!')
            self.setPortName(self.port_name)
            self.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            self.setDataBits(QSerialPort.Data8)
            self.setParity(QSerialPort.NoParity)
            self.setStopBits(QSerialPort.OneStop)
            self.setFlowControl(QSerialPort.NoFlowControl)

            # Apos todas as configuracoes tenta conectar com a porta serial
            if self.open(QSerialPort.ReadWrite):
                if self.debug:
                    print('Comunicacao estabelecida com sucesso!')
                self.online = True
            else:
                if self.debug:
                    print('Erro: nao foi possivel estabelecer a comunicacao com o Modbus')
        else:
            if self.debug:
                print('Aviso: dispositivo Modbus nao encontrado.')
                print('- - - - - - - - - - - - - - - - - - - - - - - - - - -\n')

    def send(self, send_offset):
        self.sendmessage = send_offset
        """ Envia o Offset. """
        if self.isWritable():
            if self.debug:
                print('Enviando Offset: ')
                print(self.sendmessage)
                self.write(self.sendmessage)
                print('Enviado com sucesso')

    def receive(self): 
        """ Não funciona """
        """ Recebe o Offset. """
        if self.isReadable():
            if self.debug:
                print('Recebendo Offset: ')
                print (self.read(5))
                # self.receivemessage = self.read(5)
                # print (self.receivemessage)
                # while self.isOpen():
                #     if self.waitForBytesWritten():
                #         print(self.waitForBytesWritten())
                #         print(self.readLine())
                #         break
                print('Recebido com sucesso')
                # self.close()


