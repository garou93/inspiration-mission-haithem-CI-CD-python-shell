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
import time
import stbt

amazon_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/templates_amazon/"

sc_stbt.back_to_home()
sc_stbt.open_library()
sc_stbt.goto_movies_menu()
sc_stbt.select_free_video()
sc_stbt.start_movie()
sc_stbt.detect_movie(test_secs=5)
sc_stbt.open_catflap(catflap = "movie details")
sc_stbt.wait(10)

sc_stbt.open_gerbil()
sc_stbt.goto_basic_bandwidth()
if not sc_stbt.check_state_basic_bandwidth():
	sc_stbt.enable_disable_basic_bandwidth()
sc_stbt.set_basic_bandwidth(mbit="200kbit")

start_time=time.time()
while time.time()-start_time< 900 :
	if stbt.wait_until(lambda: stbt.match(image= amazon_path_template+"insufficient_bandwidth/insufficient_bandwidth.png",
                                          region=stbt.Region(x=247, y=164, width=468, height=212),
                                          match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                confirm_method='none',
                                                                                match_threshold=0.85,
                                                                                confirm_threshold=0.3)),
                       timeout_secs=3):
		sc_stbt.wait(120)
		sc_stbt.open_gerbil()
		sc_stbt.wait(120)
		sc_stbt.goto_basic_bandwidth()
		sc_stbt.wait(120)
		sc_stbt.set_basic_bandwidth(mbit="1000kbit")
		stbt.wait_until(lambda :sc_stbt.detect_movie(test_secs=10),timeout_secs=20)
		sc_stbt.open_gerbil()
		sc_stbt.wait(120)
		sc_stbt.set_basic_bandwidth(mbit="200kbit")

sc_stbt.get_error_info(text="buffer count")
sc_stbt.enable_disable_basic_bandwidth()
sc_stbt.close_interface()

