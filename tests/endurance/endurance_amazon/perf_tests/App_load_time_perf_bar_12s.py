# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import sc_stbt
import android
import stbt

def main():
    sc_stbt.open_gerbil()
    sc_stbt.goto_basic_bandwidth()
    if not sc_stbt.check_state_basic_bandwidth():
        sc_stbt.enable_disable_basic_bandwidth()
    sc_stbt.set_basic_bandwidth()
    sc_stbt.close_interface()

def start_app():
    """
    start_app: quit Prime Video
    and the calculate the time of reopening the APP Prime Video
    :return:
    """
    sc_stbt.back_to_home()
    sc_stbt.exit_amazon()
    sc_stbt.wait(3)
    #sc_stbt.press("KEY_MENU")
    android1= eval(stbt.get_config("android", "android"))
    if android1 :
         android.goto_amazon()
    else :
         sc_stbt.is_amazon(press="KEY_OK",perf=True,perf_name= "Start_App_time")

sc_stbt.repeat(lambda: main(), occurence=1)
sc_stbt.repeat(lambda: start_app(), occurence=11)
