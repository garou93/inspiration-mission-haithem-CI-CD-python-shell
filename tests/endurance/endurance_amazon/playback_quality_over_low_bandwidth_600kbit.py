# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""nt:    Socle8,  STBT V2
"""
import stbts
import sc_stbt

sc_stbt.back_to_home()
sc_stbt.search_movie_amazon(movie_name="friends: the complete first season")
sc_stbt.open_gerbil()
sc_stbt.goto_gerbil_scripts()

if not sc_stbt.state_script_check(gerbil_script_name="QA-BigScreen-Surround-stable-low-bw-600kbps"):
    sc_stbt.run_script(gerbil_script_name="QA-BigScreen-Surround-stable-low-bw-600kbps")
else :
    pass

sc_stbt.stop_script(gerbil_script_name="QA-BigScreen-Surround-stable-low-bw-600kbps")
sc_stbt.close_interface()
sc_stbt.select_free_video()
sc_stbt.start_movie()
sc_stbt.detect_movie(test_secs=600)


