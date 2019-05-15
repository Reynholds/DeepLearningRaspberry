import serial
import time

ser=serial.Serial('/dev/ttyUSB2', 9600)
ser.write("AT+CSQ\r\n".encode())

while True:
	ser.write("AT+CSQ\r\n".encode())
	response = ser.readline()
	if "CSQ" in response.decode("utf-8") :
		print(response, end="\r", flush=True)
