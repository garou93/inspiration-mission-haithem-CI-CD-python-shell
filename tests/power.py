"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""
import time
import stbt
import sc_stbt

from serial import SerialException

DURATION_WAIT = 10


def check_stb_boot(timeout=None):
    """
    Function : check STB boot
    :return: True : if no signal not yet detected
            assert if not
    """
    if timeout is None:
        timeout = stbt.get_config("power", "timeout", type_=int)

    if sc_stbt.is_wakeup(time_out_wakeup=timeout):
        return time.time()

    assert False, "The STB boot does not start"


def boot_on(callable=None, port=None):
    """
    Function: enable hdmi and power port passed on parameter
    :param callable: The function that verif if STB finish the boot
    :param power_port: the port of power switch we need to enable
    :param hdmi_port: the port of hdmmi switch we need to enable
    :return: fail if set_power_on() fail
    """
    # if port is not passed it will be get from config file
    if port is None:
        port = stbt.get_config("power", "port", type_=int)

    if callable is None:
        callable = lambda: check_stb_boot()

    # enable the hdmi port passed on parameter
    try:
        sc_stbt.set_hdmi_input(port)
    except SerialException:
        sc_stbt.debug("THE HDMI SWITCH IS NOT CONNECTED")
        pass
    sc_stbt.wait(DURATION_WAIT)

    # disable all ports of power switch
    sc_stbt.set_power_off(port)
    sc_stbt.wait(DURATION_WAIT)

    # enable the power port passed on parameter
    start_time = sc_stbt.set_power_on(port)

    # get the time after detect the STB boot
    end_time = callable()
    sc_stbt.wait(60)

    # write the time of STB boot into file stb_boot.txt
    output_file = open('perf_boot.txt', 'a')
    output_file.write("Boot on time : " + str(end_time - start_time) + '\n')
    output_file.close()


def boot_off(port=None):
    """
    Funtion: disable all ports of power switch
    :return: Fail if set_power_off() fail
    """
    # disable all ports of power switch

    if port is None:
        port = stbt.get_config("power", "port", type_=int)
    sc_stbt.set_power_off(port)
    if sc_stbt.is_standby():
        sc_stbt.debug("POWER PORT IS OFF")
        sc_stbt.wait(DURATION_WAIT)
    else:
        assert False, "POWER PORT IS  NOT  OFF"
