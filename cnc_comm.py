# This file implements a command line script to communicate with the CNC machine
#
# Copyright (C) 2016 Ionut Gorgos (ionutgorgos@gmail.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import serial
import serial.tools.list_ports
import time
import argparse

class CncComm:

    def __init__(self):
        self.ser = None
      #  self.xvalue = 0


    def read_ports(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.ser = serial.Serial(p.device, 115200)   # Open the grbl port

    def stream_code_from_file(self, file):
        f = open(file,'r')
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()

        # Stream g-code to grbl
        for line in f:
            l = line.strip()
            print 'Sending: ' + l
            self.ser.write(l + '\n')
            grbl_out = self.ser.readline()
            print ' : ' + grbl_out.strip()

        raw_input("	Press <Enter> to exit and disable grbl.")

        f.close()
        self.ser.close()

    def stream_code_x_axis(self, xvalue):
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()

        self.ser.write("$X\nG21\nG90" + '\n')
        move = "G00 X" + xvalue
        self.ser.write(move + '\n')
        grbl_out = self.ser.readline()
        print ' : ' + grbl_out.strip()

        raw_input("	Press <Enter> to exit and disable grbl.")

        self.ser.close()

def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'grbl_file',
        help='the file containing the gcode')

    parser.add_argument(
        'xvalue',
        help='the distance on x axis in mm')

    args = parser.parse_args()

    filename = args.grbl_file
    xvalue = args.xvalue

    cnc = CncComm()
    cnc.read_ports()
    #cnc.stream_code_from_file(filename)
   # cnc.stream_code_x_axis(xvalue)


if __name__ == '__main__':
    main()
