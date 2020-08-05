import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

client=ModbusClient('192.168.4.29')
client.connect()


#read inputs:
data = client.read_input_registers(6,4)
ch0 = (data.registers[0]/20000.0)*10
ch1 = (data.registers[1]/20000.0)*10
ch2 = (data.registers[2]/20000.0)*10
ch3 = (data.registers[3]/20000.0)*10

print("Channel 0 Input Voltage",ch0)
print("Channel 1 Input Voltage",ch1)
print("Channel 2 Input Voltage",ch2)
print("Channel 3 Input Voltage",ch3)
