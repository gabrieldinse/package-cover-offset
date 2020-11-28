
import sys
import minimalmodbus

info1 = 100 
info2 = 102
PORT = 'COM4'

# Configurar instrumento
instrument = minimalmodbus.Instrument(PORT, 1, mode = 'rtu')

# Configurações
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout = 1

# Fechar porta a cada chamada
instrument.close_port_after_each_call = True    

# Limpar buffers
instrument.clear_buffers_before_each_transaction = True

informação1 = instrument.read_float(info1)
informação2 = instrument.read_float(info2)

print('A 1ª Informação é: ' + informação1)
print('A 2ª Informação é: ' + informação2)