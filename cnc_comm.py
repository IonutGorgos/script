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
import sys

class CncComm:

    def __init__(self):
        self.ser = None
        self.speed = 2 # mm / s


    def open_port(self, port):
        self.ser = serial.Serial(port, 115200)   # Open the grbl port

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

        #raw_input("	Press <Enter> to exit and disable grbl.")

        f.close()
        self.ser.close()

    def stream_code_x_axis(self, xvalue):
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write("$X\nG21\nG90" + '\n')
        move = "G00 X" + str(xvalue)
        a = time.time()  # to measure time elapsed
        self.ser.write(move + '\n')
        i = 0.0
        while i < abs(xvalue):
            print "X : " + str(i)
            #print (str(i))
            if (abs(xvalue) - i) < 0.005:
                break
            time.sleep(0.0525)
            i = i + 0.105

        elapsed = time.time() - a  # to measure time elapsed
        print elapsed  # to measure time elapsed
        grbl_out = self.ser.readline()
        print 'X : ' + str(xvalue) + " = " + grbl_out.strip()
        #raw_input("	Press <Enter> to exit and disable grbl."
        self.ser.close()


    def go_home(self):
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write("$X\nG21\nG90" + '\n')
        self.ser.write("G00 X0 Y0 Z0")
        #raw_input("Your position is (0, 0, 0), press <Enter> to exit.")
        self.ser.close()

def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'port',
        help = 'the name of the serial port to communicate to the Arduino, '
               'e.g. COM10'
    )
    parser.add_argument(
        '--f',
        nargs=1,
        type=argparse.FileType('r'),
        default=False, metavar='filename',
        help='the file containing the gcode')

    parser.add_argument(
        '--x',
        nargs = 1,
        type = float,
        default= 0.0,
        metavar = 'value',
        #action = 'store_true',
        help='the distance on x axis in mm')
    parser.add_argument(
        '--home',
        action = 'store_true',
        help='go to home (0, 0, 0)')

    args = parser.parse_args()
    port = args.port

    cnc = CncComm()
    cnc.open_port(port)


    #filename = args.grbl_file

    #cnc.stream_code_from_file(filename)
    cnc.stream_code_x_axis(args.x[0])
    #cnc.go_home()


if __name__ == '__main__':
    main()
