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
import stbt
import android

def main_test():
   """
   main_test:: stress of the APP play a content for 1 min then rxit then repeat 60 times
   :return:
   """
   android_conf = eval(stbt.get_config("android", "android"))
   if android_conf :
      android.go_to_amazon()
   else:
      sc_stbt.go_to_amazon()
   sc_stbt.back_to_home(),
   sc_stbt.open_library(),
   sc_stbt.goto_movies_menu(),
   sc_stbt.select_free_video(),
   sc_stbt.start_movie(),
   sc_stbt.detect_movie(),
   sc_stbt.quit_amazon(press="KEY_EXIT")

sc_stbt.repeat(lambda: main_test(),occurence=60)



