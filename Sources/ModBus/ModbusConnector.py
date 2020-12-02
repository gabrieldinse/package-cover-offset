import time
import minimalmodbus
import time


class ModbusConnector(minimalmodbus.Instrument):

	
	def __init__(self, port='COM3', slaveaddress=1, close_port_after_each_call=False):
		minimalmodbus.Instrument.__init__(self, port, slaveaddress) 
		self.serial.baudrate = 19200
		self.serial.bytesize = 8
		self.serial.stopbits = 1
		self.serial.timeout = 1  # segundos
	
		# self.port = port
		# self.slaveaddress = slaveaddress
		self.mode = 'rtu'
		self.close_port_after_each_call = close_port_after_each_call
		self.debug = False
		self.usb_on = True
		self.register = 0

		if self.debug == True:
		    print(self)

		time.sleep(2)

	def send_offset(self, offset):  # Envia o offset
		if self.usb_on == True:
			try:
				print ("Enviado Offset: " + str(offset))
				self.write_register(0, offset)
				print('Enviado com sucesso')
				time.sleep (2)

			except:
				print ("Erro de Comunicação: Não enviado --------------")
				time.sleep (2)

	def read_offset(self):  # Recebe o offset
		if self.usb_on == True :
			try:
				print ("Recebendo Offset: ")
				test_reg = self.read_registers(0,2,4)
				print('Recebido: ' + str(test_reg))
				time.sleep (2)

			except:
				print ("Erro de Comunicação: Não recebido --------------")
				time.sleep (2)
