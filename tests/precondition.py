"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""


import sc_stbt
import sys
from serial import SerialException

DURATION_WAIT = 120

port = int(sys.argv[1])

sc_stbt.set_power_off(port=port)
sc_stbt.set_power_on(port=port)

try:
	sc_stbt.set_hdmi_input(port=port)
except SerialException:
	sc_stbt.debug("THE HDMI SWITCH IS NOT CONNECTED")
	pass
