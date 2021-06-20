import time
import serial
import subprocess
from os import path as os_path
import stbt

#
# we need to create  a fifo file ir_commands in this foder  ../trunk/_sc_stbt before runing this filet
# commande : mkfifo ir_commands 
# now run this file : python irserver_quad.py
#


previous_stb = 0
# port of quadview connection to pc /dev/ttyUSB*
usb_num = stbt.get_config("quad","usb_num")
ser = serial.Serial("/dev/ttyUSB"+str(usb_num), 115200)
print ('Opened serial: ' + ser.name)
PATH = os_path.abspath(os_path.split(__file__)[0])
while True:
    with open(PATH + '/ir_commands') as fifo:
        for line in fifo:
            # parse line
            stb = line.split()[0] # recuperation id STB
            #if stb != previous_stb:
            print ("Selecting serial {}".format(stb))
            time.sleep(0.05)
            ser.write(b'IN{}.'.format(stb))
            time.sleep(0.05)
                #previous_stb = stb
            key = line.split()[1] # recuperation cle IR
            print ("Calling irsend " + key)
            # send IR command with redrat: remote = name of remote /lirc/product.conf name of remote
            # subprocess.call(["irsend", "SEND_ONCE", "remote", key])
            # send IR command with irtrans
            subprocess.call(["stbtv2", "control", key], shell=True)