#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

STANDBY_PATH_TEMPLATES = sc_stbt.get_generic_template_path() + \
                         "/../../../trunk/tests/templates/standby"
path_mask_blackscreen = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/blackscreen_standby_wakeup/mask_black.png"


#----------------- API Standby ------------------

def __set_standby():
    """
    __set_standby: press key power to standby stb and return time
    :return:
    """
    sc_stbt.press("KEY_POWER")
    sc_stbt.wait(2)
    return time.time()



def is_standby(time_out_standby=None):
    """
    Function: Check if the current power state is standby
    :return: True if the current power state is standby
             False if the current power state is wake up

    """
    if time_out_standby is None:
        time_out_standby = stbt.get_config("standby", "time_out_standby", type_=int)

    # if we use quadview
    device_quad = eval(stbt.get_config("standby", "device_quad"))
    # waiting to match blackscreen for quad device
    if device_quad:
        sc_stbt.wait(2)
        if check_blackscreen():
            sc_stbt.debug("STB IN standby MODE")
            return True
        else:
            sc_stbt.debug("STB IS NOT IN standby MODE")
            return False

    # waiting to match blue screen for Teradek
    # waiting to match "no signal" for Magewell
    else:
        sc_stbt.debug(str(time_out_standby))
        if stbt.wait_until(lambda: sc_stbt.wait_for_many_match(image=sc_stbt.get_all_templates_in_directory(STANDBY_PATH_TEMPLATES),
                                                    timeout_secs=0),
                            timeout_secs=time_out_standby):
            sc_stbt.debug("STB IS IN STANDBY MODE")
            return True
        else:
            sc_stbt.debug("STB IS NOT IN STANDBY MODE")
            return False


def _set_standby(callable=is_standby,time_out_standby=None,standby_wait=None):
    """
    _set_standby: press  key_power then check if stb is in standby
    :param time_out_standby:
    :return: True if stb in standby
            else False
    """
    if standby_wait is None:
        standby_wait = stbt.get_config("standby", "standby_wait", type_=int)
    start_standby = __set_standby()
    if callable(time_out_standby):
        standby_secs = time.time() - start_standby - 2
        sc_stbt.write_csv_file("perf_standby.csv", [["a", standby_secs]])
        #  Extra time for test for users
        # sc_stbt.wait(10)
        sc_stbt.debug("TIME NEEDED TO POWER OFF THE STB ", str(standby_secs))
        sc_stbt.debug("wait for ",str(standby_wait))
        sc_stbt.wait(standby_wait)
        return True
    else:
        assert False, ("STANDBY ACTION NOT DONE")


def set_standby(callable=None, time_out_standby=None, standby_wait=None):
    """
    Function: Set the power state standby
    :return: True if set to standby succeed
             False if stb is already in standby
    """
    sc_stbt.wait(1)
    if callable is None:
        callable = is_standby
    if is_standby(time_out_standby):
        assert False, ("STB ALREADY IN STANDBY")

    else:
        return _set_standby(callable, time_out_standby, standby_wait)


#----------------- API Wakeup ------------------

def __set_wakeup(wait = 2):
    """
    __set_wakeup: press key power to wakeup stb and return time
    :return:
    """
    sc_stbt.press("KEY_POWER")
    sc_stbt.wait(wait)
    return time.time()


def is_wakeup(time_out_wakeup=None):
    """
    Function: Check if the current power state is wake up
    :return: True if the current power state is wake up
             False if the current power state is standby
    """
    if time_out_wakeup is None:
        time_out_wakeup = stbt.get_config("standby", "time_out_wakeup", type_=int)

    # if we use quadview
    device_quad = eval(stbt.get_config("standby", "device_quad"))

    # waiting to match blackscreen for quad device
    if device_quad:
        if check_blackscreen(wakeup=True):
            sc_stbt.debug("STB IS NOT IN WAKEUP MODE")
            return False
        else:
            sc_stbt.debug("STB IN WAKEUP MODE")
            return True


    # waiting to match blue screen for Teradek
    # waiting to match "no signal" for Magewell
    else:
        sc_stbt.debug("CHECK WAKEUP MODE IN ",str(time_out_wakeup)+" SECS")
        if stbt.wait_until(lambda: sc_stbt.wait_for_many_match(image=sc_stbt.get_all_templates_in_directory(STANDBY_PATH_TEMPLATES),
                                                    timeout_secs=0),
                            timeout_secs=time_out_wakeup):
            sc_stbt.debug("STB IS NOT IN WAKEUP MODE")
            return False
        else:
            sc_stbt.debug("STB IS IN WAKEUP MODE")
            return True


def _set_wakeup(callable = is_wakeup, time_out_wakeup = None, wakeup_wait = None, wait = 2):
    """
    _set_wakeup:press  key_power then check if stb is in wakeup
    :param callable:
    :param time_out_wakeup:
    :return:
    """
    if wakeup_wait is None:
        wakeup_wait = stbt.get_config("standby", "wakeup_wait", type_=int)

    start_wakeup = __set_wakeup(wait)
    if callable(time_out_wakeup):
        wakeup_secs = time.time() - start_wakeup - wait
        sc_stbt.write_csv_file("perf_wakeup.csv", [["time", wakeup_secs]])
        if callable == is_wakeup:
            pass
        else:
            sc_stbt.debug("TIME NEEDED TO POWER ON THE STB ", str(wakeup_secs))
        #  Extra time for test for users
        sc_stbt.wait(wakeup_wait)
        return True
    else:
        sc_stbt.debug("WAKEUP ACTION NOT DONE")
        return False


def set_wakeup(callable=None, time_out_wakeup=None, wakeup_wait=None):
    """
    Set the power state wake up
    :return:
    True: wakeup is done
    False : wakeup is already the state
          : wakeup not detected (lost key or timeout expired)
    """
    if callable is None:
        callable = is_wakeup
    if is_wakeup(time_out_wakeup):
        assert False, ("STB ALREADY IN WAKEUP")
    else:
        return _set_wakeup(callable, time_out_wakeup, wakeup_wait)


def test_wakeup(callable=None, timeout=None):
    if callable is None:
        set_wakeup(sc_stbt.is_wakeup, timeout)
    else:
        return set_wakeup(callable, timeout)


def check_blackscreen(wakeup=False):
    """
    check_blackscreen: check blackscreen for a 15 second
    :return:
    """
    is_blackscreen = False
    i = 0
    start_time = time.time()
    sc_stbt.wait(3)
    while time.time() - start_time < 15:
        if wakeup:
            if stbt.is_screen_black(mask=path_mask_blackscreen):
                is_blackscreen = True
            else:
                return False
        else:
            if stbt.is_screen_black(mask=path_mask_blackscreen):
                is_blackscreen = True
                i = i + 1
            else:
                return False
            if i == 15:
                return is_blackscreen
        sc_stbt.wait(0.2)

    return is_blackscreen