"""
test power switch
"""
import sc_stbt

ON = 'N'
OFF = 'F'

#ser_power = sc_stbt.USBserial(mount='/dev/powerswitch')
#sc_stbt.wait(2)
#ser_power.send("F1F2N3F4")
#sc_stbt.wait(5)
#ser_power.send("F1F2F3N4")
#sc_stbt.wait(20)
#ser_power.close()
#sc_stbt.set_power(ON, ON, ON, ON)
sc_stbt.set_power_on(port=1)
#sc_stbt.set_power_on(port=2)
sc_stbt.set_power_on(port=3)
#sc_stbt.set_power_on(port=4)
sc_stbt.set_power(OFF, OFF, OFF, OFF)
