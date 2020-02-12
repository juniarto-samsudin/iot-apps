import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
while(1):
    print(ser.name)
    ser.write(b'hello')
ser.close
