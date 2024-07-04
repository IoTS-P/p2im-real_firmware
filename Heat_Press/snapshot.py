#!/usr/bin/python3
import re
import sys
import serial
import binascii,time

if len(sys.argv) > 2:
    port = sys.argv[1]
else:
    port = '/dev/ttyACM0'

f_out = open("out.log","w",encoding='utf-8')

ser = serial.Serial(port, 9600) 
if ser.isOpen():                       
    print("Successful open serial port。")
    print(ser.name)  
else:
    print("Open Serial port fail")

# send signal
command = bytes("snapshot", "ascii")
ser.write(command)
prev = 0
count = 0

# recv snapshot
while True:
    prev = count 
    count = ser.inWaiting()
    if count > 0 and prev == count:
        break
    time.sleep(1)

if count > 0:
    data=ser.read(count)
    data = data.decode('unicode_escape')
    data = data.replace('\n', "\\n")
    data = data.replace('\r', '')
    # datalist = data.split('\\n')
    f_out.write(data)
   
f_out.close()
