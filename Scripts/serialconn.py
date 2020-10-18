import serial
import struct
from datetime import datetime


def connect(username, password, time):
    ser = serial.Serial(
                    port='/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )

    ser.isOpen()

    now  =  datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H:%M:%S")
    if time < 24:
        connection_time_string = "Time: " + str(time) +" Hours"
    elif time == 24:
        connection_time_string = "Time: 1 Day"
    else:
        connection_time_string = "Time: " + str(int(time/24)) +" Days"

    L0 = [ 0x1b, 0x40, 0x1b, 0x61, 0x01 ]
    L1 = "Thank you for choosing AIR FIBRE".encode()
    L2 = [ 0x0d, 0x0a, 0x0a ]
    L3 = "Username & Password:".encode()
    L4 = [ 0x0d, 0x0a, 0x0a ]
    L5 = [ 0x1b, 0x40, 0x1b, 0x61, 0x01, 0x1d, 0x21, 0x11 ]
    L6 = username.encode()
    L7 = " / ".encode()
    L8 = password.encode()
    L9 = [ 0x0d, 0x0a ]

    # return to small font
    L10 = [ 0x1d, 0x21, 0x10, 0x0a ]
    L11 = [ 0x1b, 0x40, 0x1b, 0x61, 0x01 ]

    L12 = connection_time_string.encode()
    L13 = [ 0x0d, 0x0a ]
    L14 = dt_string.encode()
    L15 = [ 0x0d, 0x0a ]
    L16 = [ 0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x0a ]

    # cut paper
    L17 = [ 0x1b, 0x69 ]

    ser.write(serial.to_bytes(L1))
    ser.write(serial.to_bytes(L2))
    ser.write(serial.to_bytes(L3))
    ser.write(serial.to_bytes(L4))
    ser.write(serial.to_bytes(L5))
    ser.write(serial.to_bytes(L6))
    ser.write(serial.to_bytes(L7))
    ser.write(serial.to_bytes(L8))
    ser.write(serial.to_bytes(L9))
    ser.write(serial.to_bytes(L10))
    ser.write(serial.to_bytes(L11))
    ser.write(serial.to_bytes(L12))
    ser.write(serial.to_bytes(L13))
    ser.write(serial.to_bytes(L14))
    ser.write(serial.to_bytes(L15))
    ser.write(serial.to_bytes(L16))
    ser.write(serial.to_bytes(L17))
    ser.close()

