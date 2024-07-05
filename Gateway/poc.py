#!/usr/bin/python3
import re
import serial
import binascii,time


lines = []
lines.append('f4 6c 21 55\n')
# 6c overwrite rx_callback[1] to trigger the crash 

f_out = open("out.log","w",encoding='utf-8')


ser = serial.Serial("/dev/ttyACM0", 9600)  
if ser.isOpen():                       
    print("Success open serial port")
    print(ser.name)   
else:
    print("Fail to open serial port")

total_line = len(lines)
prev = 0
count = 0
for (idx,line) in enumerate(lines):
    last_ = (total_line - idx)
    print(f"last {last_} In: {line}")
    f_out.write("In: " + line)
    d=bytes.fromhex(line)
    print(d)
    ser.write(d)

    time.sleep(0.5)
    prev = 0
    while True:
        prev = count 
        count = ser.inWaiting()
        if count > 0 and prev == count:
            break
        time.sleep(1)

    if count>0:
        data=ser.read(count)
        data = data.decode('unicode_escape')
        data = data.replace('\n', "\\n")
        data = data.replace('\r', '')
        datalist = data.split('\\n')
        for i in datalist:
            print(i)
            f_out.write(i+"\n")
    
# log the error 
print("sleep::::")
time.sleep(10)
count = ser.inWaiting()
if count > 0:
    data=ser.read(count)
    data = data.decode('unicode_escape')
    data = data.replace('\n', "\\n")
    data = data.replace('\r', '')
    datalist = data.split('\\n')
    for i in datalist:
        print(i)
        f_out.write(i+"\n")
f_out.close()
