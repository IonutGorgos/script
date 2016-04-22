import cnc_comm

cnc = cnc_comm.CncComm()
cnc.read_ports()
cnc.stream_code('grbl.gcode')