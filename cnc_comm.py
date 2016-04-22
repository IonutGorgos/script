import serial
import serial.tools.list_ports
import time


class CncComm:

    def __init__(self):
        self.ser = None
        self.f = None


    def read_ports(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.ser = serial.Serial(p.device, 115200)   # Open the grbl port

    def stream_code(self, file):
        self.f = open(file,'r')
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()

        # Stream g-code to grbl
        for line in self.f:
            l = line.strip()
            print 'Sending: ' + l,
            self.ser.write(l + '\n')
            grbl_out = self.ser.readline()
            print ' : ' + grbl_out.strip()

        raw_input("	Press <Enter> to exit and disable grbl.")

        self.f.close()
        self.ser.close()

