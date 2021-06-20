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
# import sws1
import vodafone

youtube_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/youtube/"
path_mask_motion1 = youtube_path_template + "/motion/mask_motion.png"
youtube = sc_stbt.video_tests(path_mask_motion1)

def x():
    android1= eval(stbt.get_config("android", "android"))
    if android1 :
          android.goto_amazon()
    else:
    ##########ajouter le ligne specifique pour le go to amazon selon le projet linux (projet.go_to_amazon()) ##########
          vodafone.goto_amazon()
          # sws1.go_to_amazon()


def main(switch=None):
    sc_stbt.is_amazon()
    sc_stbt.open_library()
    sc_stbt.goto_movies_menu()
    sc_stbt.select_free_video()
    sc_stbt.start_movie()
    sc_stbt.detect_movie(test_secs=40)
    sc_stbt.press("KEY_BACK")
    sc_stbt.quit_amazon()
    sc_stbt.wait(1)

    if switch == "netflix" :
        press = 7
    elif switch == "youtube" :
        press = 3
    else : assert False, "Please enter a valid App Name"

    sc_stbt.wait(3)
    sc_stbt.combo_press(combo=["KEY_RIGHT"], number_press=press)
    sc_stbt.wait(2)
    sc_stbt.combo_press(combo=["KEY_OK"], number_press=1, delay_sec=0.5)
    sc_stbt.wait(15)

    if switch == "netflix" :
        sc_stbt.open_video_netflix()
    elif switch == "youtube" :
        sc_stbt.test_open_video_youtube()
        sc_stbt.wait(2)
        sc_stbt.test_youtube_motion(test_secs=40)
    else : assert False, "Please enter a valid App Name"
    sc_stbt.combo_press(combo=["KEY_BACK","KEY_BACK","KEY_EXIT" ], delay_sec=1)
    sc_stbt.wait(2)
    sc_stbt.combo_press(combo=["KEY_LEFT"], number_press=10)
    sc_stbt.wait(1)
    sc_stbt.press("KEY_OK")
#
def x1():
    i = 0
    while i<200 :
        main(switch="netflix")
        i= i+1
        sc_stbt.debug("iteration number : " + str(i))

sc_stbt.repeat( lambda: x(), occurence=1)
sc_stbt.repeat( lambda: x1(), occurence=2)