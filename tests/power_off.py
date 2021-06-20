"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import stbt
import sc_stbt
import os

menu = sc_stbt.menu()
path = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/standby"
path_mask_blackscreen = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/blackscreen_standby_wakeup/mask_black.png"


def test_power_all_off():
    """
    Funtion: disable all ports of power switch
    :return: Fail if set_power_off() fail
    """
    # disable all ports of power switch
    quad = eval(stbt.get_config("standby","device_quad"))
    sc_stbt.set_power_off(port='0')
    sc_stbt.wait(2)
    if quad :
        if stbt.is_screen_black(mask=path_mask_blackscreen):
            sc_stbt.debug("ALL POWER PORTS ARE OFF")
        else:
            assert False, "POWER PORTS ARE NOT ALL OFF"

    elif stbt.wait_until(lambda: sc_stbt.wait_for_many_match(image=sc_stbt.get_all_templates_in_directory(path),
                                                    timeout_secs=0),
                            timeout_secs=10):
        sc_stbt.debug("ALL POWER PORTS ARE OFF")
        sc_stbt.wait(3)
    else:
        assert False, "POWER PORTS ARE NOT ALL OFF"
#


def test_power_off(power_port=None):
    """
    Funtion: disable all ports of power switch
    :return: Fail if set_power_off() fail
    """
    # disable all ports of power switch

    if power_port is None:
        power_port = stbt.get_config("power", "port", type_=int)
    sc_stbt.set_power_off(port=power_port)
    if menu.is_menu_template(perf=False,
                             path = path ,
                             region_frame=stbt.Region(x=0, y=0, width=961, height=542),
                             timeout=3):
          sc_stbt.debug(" POWER PORT"+ str(power_port) +" IS OFF")
          sc_stbt.wait(3)
    else:
        assert False, "POWER PORT" +str(power_port) + " IS NOT OFF"

if __name__ == "__main__":
    test_power_off()
