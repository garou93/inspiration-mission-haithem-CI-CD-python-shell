# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""
import stbts
import sc_stbt

sc_stbt.back_to_home()
sc_stbt.search_movie_amazon(movie_name="live die repeat")
sc_stbt.open_gerbil()
sc_stbt.goto_gerbil_scripts()

if not sc_stbt.state_script_check(gerbil_script_name="QA_v2-sawtooth-up-slow-loop"):
    sc_stbt.run_script(gerbil_script_name="QA_v2-sawtooth-up-slow-loop")
else :
    pass

sc_stbt.stop_script(gerbil_script_name="QA_v2-sawtooth-up-slow-loop")
sc_stbt.close_interface()
sc_stbt.start_movie()
sc_stbt.detect_movie(test_secs=600)



