# -*- coding: utf-8 -*-
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



###########################################
#-------------- Wakeup Tests ------------
###########################################

def test_force_wakeup():
    """
    test_force_standby: precondition test,we use it to ensure
    that stb on wakeup state
    :return: True if stb is already in wakeup
    else Fail with assert if force wakeup is not done

    """
    if sc_stbt.is_wakeup():
        sc_stbt.debug("STB ALREADY IN WAKEUP MODE")
        return True
    assert stbt.wait_until(lambda: sc_stbt._set_wakeup(wait=3),
                           timeout_secs=180,
                           interval_secs=60), \
        ("FORCE WAKEUP ACTION NOT DONE")




def set_wakeup_from_deep_standby(time_out_wakeup=None):
    # SET WAKE UP AFTER  DEEP_STANDBY
    """
    :param time_out_wakeup:  time needed to wake up  the STB
    :return: True : if wake up achieved before timeout ends
             False : if wake up not detected , or timeout ends

    """
    sc_stbt.wait(5)
    if time_out_wakeup is None:
        time_out_wakeup = stbt.get_config("standby",
                                          "time_out_wakeup_fom_deep_standby",
                                          type_=int)
    assert sc_stbt.test_wakeup(sc_stbt.is_wakeup, time_out_wakeup), \
        ("PROBLEM IN WAKE_UP")


def set_wakeup_from_fake_standby():

    # SET WAKE UP AFTER  FAKE_STANDBY
    """
    :param time_out_wakeup:  time needed to wake up  the STB
    :return: True : if wake up achieved before timeout ends
             False : if wake up not detected , or timeout ends

    """
    sc_stbt.wait(5)
    assert sc_stbt.test_wakeup(sc_stbt.is_wakeup), \
        ("PROBLEM IN WAKE_UP")


def test_set_wakeup(time_out_wakeup=None):
    """
    Funtion:set the STB on wakeup status
    :return: Fail if stb is already wakeup
    """
    sc_stbt.wait(1)
    print "iiiiiiiiiiiiiiiiiiiiiiii"
    assert sc_stbt.test_wakeup(timeout=time_out_wakeup),"WAKEUP ACTION NOT DONE"





###########################################
# #Standby
###########################################

def test_set_standby(time_out_standby=None):
    """
    Funtion:set the STB on standby status
            Precondition: STB should be on wake up to launch this test
    :return: Fail if set_standby() fail
    """
    sc_stbt.wait(1)
    if time_out_standby is None:
        time_out_standby = stbt.get_config("standby",
                                           "time_out_standby",
                                           type_=int)
    return sc_stbt.set_standby(time_out_standby=time_out_standby)


def test_force_standby():
    """
    test_force_standby: precondition test,we use it to ensure
    that stb on standby state
    :return: True if stb is already in standby
    else Fail with assert if force standby is not done
    """
    sc_stbt.wait(5)
    if sc_stbt.is_standby():
        sc_stbt.debug("STB ALREADY IN STANDBY MODE")
        return True
    assert stbt.wait_until(lambda: sc_stbt._set_standby(),
                           timeout_secs=180,
                           interval_secs=60), \
        ("FORCE STANDBY ACTION NOT DONE")
