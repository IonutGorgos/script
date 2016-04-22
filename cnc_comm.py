import serial
import serial.tools.list_ports
import time
import argparse

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

def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'grbl_file',
        help='the file containing the gcode')

    args = parser.parse_args()

    filename = args.grbl_file

    cnc = CncComm()
    cnc.read_ports()
    cnc.stream_code(filename)


if __name__ == '__main__':
    main()
