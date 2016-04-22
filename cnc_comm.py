import serial
import serial.tools.list_ports
import time

class CncComm:

	def __init__(self):
		self.port = None
		self.f = None


	def read_ports(self):
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			self.port = serial.Serial(p.device, 115200)
			# Open grbl serial port


	def stream_code(self, file):
		self.f = open(file,'r')
		self.port.write("\r\n\r\n")
		time.sleep(2)
		self.port.flushInput()

		# Stream g-code to grbl
		for line in self.f:
			l = line.strip()
			print 'Sending: ' + l,
			self.port.write(l + '\n')
			grbl_out = self.port.readline()
			print ' : ' + grbl_out.strip()

		raw_input("	Press <Enter> to exit and disable grbl.")
		
		self.f.close()
		self.port.close()
