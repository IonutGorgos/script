import argparse
import cnc_comm

def main():
    
# Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'grbl_file',
        help='the file containing the gcode')

    args = parser.parse_args()

    filename = args.grbl_file

    cnc = cnc_comm.CncComm()
    cnc.read_ports()
    cnc.stream_code(filename)

if __name__ == '__main__':
    main()