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
import time


def test_power_on(callable=None, power_port=None):
    """
    test_power_on:power port passed on parameter
    :param callable: The function that verif if STB finish the boot
    :param power_port: the port of power switch we need to enable
    :return: fail if set_power_on() fail
    """
    # if power_port not passed as parameter it will be get from config file
    if power_port is None:
        power_port = stbt.get_config("power", "port", type_=int)

    if callable is None:
        callable = lambda: check_stb_boot()

    # disable all ports of power switch
    sc_stbt.set_power_off(port=power_port)
    sc_stbt.wait(5)

    # enable the power port passed on parameter
    sc_stbt.set_power_on(port=power_port)

    # get the time after detect the STB boot
    end_time = callable()

    # write the time of STB boot into file stb_boot.txt
    output_file = open('stb_boot.txt', 'a')
    output_file.close()


def check_stb_boot():
    """
    Function : check STB boot
    :return: True : if no signal not yet detected
            assert if not
    """

    if stbt.wait_until(lambda: sc_stbt.is_wakeup(),
                       timeout_secs=60):
        return time.time()
    
    assert False, "The STB boot does not start"

if __name__ == "__main__":
    test_power_on(lambda: check_stb_boot())
