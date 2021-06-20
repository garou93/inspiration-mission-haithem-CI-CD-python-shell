# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import _stbt.core
import stbt
import time
import sc_stbt


audio = eval(stbt.get_config("global", "audio"))
_duration=eval(stbt.get_config("audio", "duration_audio"))
_level=eval(stbt.get_config("audio", "level_audio"))

def is_audio():

    _stbt.core.isaudio_present()

def is_not_audio():

    _stbt.core.isaudio_absent()


def check_vol_up(duration=_duration ,level=_level):
    """

    :param duration: time to get audio chunks
    :param level: number of press v+
    :return:
    """

    sc_stbt.combo_press(combo=["KEY_VOLUMEDOWN"],number_press=level)
    before = moy_vol(duration)
    print "volume before" , before
    time.sleep(2)
    sc_stbt.combo_press(combo=["KEY_VOLUMEUP"],number_press=level)
    after=moy_vol(duration)
    print "volume after" , after
    time.sleep(2)
    if before < after :
          stbt.debug("VOULUME_UP is OK ")
    else:
          assert False, "ERROR NO VOLUME UP "

def check_vol_down(duration=_duration ,level=_level ):

    """

    :param duration: time to get audio chunks
    :param level: number of press v-
    :return:
    """

    sc_stbt.combo_press(combo=["KEY_VOLUMEUP"],number_press=level)
    before = moy_vol(duration)
    print "volume before" , before
    time.sleep(2)
    sc_stbt.combo_press(combo=["KEY_VOLUMEDOWN"],number_press=level)
    after=moy_vol(duration)
    print "volume after" , after
    time.sleep(2)
    if before > after :
           stbt.debug("VOULUME_DOWN is OK ")
    else:
           assert False, "ERROR NO VOLUME DOWN "

def moy_vol(duration=None):
        """

        :param duration: duration: time to get audio chunks
        :return: RMS audio
        """
        if duration is None:
            duration=_duration
        start_time=time.time()
        chunk=0
        iteration=0
        while time.time() - start_time < duration:
              wave1 = stbt._dut._display.pull_wave()
              ch1 = "" + str(wave1)
              chunk = chunk + stbt.get_rms(ch1)
              iteration+=1
        RMS = chunk/iteration
        return RMS
