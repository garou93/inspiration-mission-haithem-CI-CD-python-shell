"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import sc_stbt
import stbt
import serial
import time

# sc_stbt.set_hdmi_input(port=1)
# sc_stbt.set_hdmi_input(port=2)
# sc_stbt.set_hdmi_input(port=3)
# sc_stbt.set_hdmi_input(port=4)


def set_hdmi_input(hdmi_port=None, callable=None):
    """
    set_hdmi_input: switch hdmi port
    :return:
    """
    # if hdmi_port not passed as parameter it will be get from config file
    if hdmi_port is None:
        hdmi_port = stbt.get_config("hdmi_switcher", "port", type_=int)
    device = stbt.get_config("hdmi_switcher", "device")

    rcu_switch = eval(stbt.get_config("hdmi_switcher", "rcu_switch"))
    if not rcu_switch:
        # if device is hdmi switch
        if device != "quad":
            try:
                sc_stbt.set_hdmi_input(port=hdmi_port)
            except serial.SerialException:
                assert False, ("THE HDMI SWITCH IS NOT CONNECTED")
        # if device is quadview
        elif device == "quad":
            #execution with serial port
            try:
                usb_num = stbt.get_config("quad","usb_num")
                ser = serial.Serial("/dev/ttyUSB"+str(usb_num), 115200)
                print ('Opened serial: ' + ser.name)
                time.sleep(0.05)
                print ("Selecting serial {}".format(hdmi_port))
                ser.write(b'IN{}.'.format(hdmi_port))
                time.sleep(0.05)
                ser.write(b'IN{}.'.format(hdmi_port))
                time.sleep(0.05)
                ser.close()
            except serial.SerialException:
                assert False, ("THE QUAD SWITCH IS NOT CONNECTED")
    elif rcu_switch:
        sc_stbt.combo_press(combo=["HDMI_"+str(hdmi_port)], number_press=3)

    if callable is None:
        sc_stbt.debug(str(hdmi_port)+" is ON")
    else:
        callable()
        sc_stbt.debug(str(hdmi_port)+" is ON")
    time.sleep(5)

if __name__ == "__main__":
    set_hdmi_input(hdmi_port=None, callable=None)