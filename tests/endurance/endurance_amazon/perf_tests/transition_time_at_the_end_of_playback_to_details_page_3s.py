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

sc_stbt.back_to_home()
sc_stbt.open_library()
sc_stbt.goto_movies_menu()
sc_stbt.select_free_video()


def main():
	"""
	main : set the bandwidth to 5 mbit with selenium
	:return:
	"""
	sc_stbt.open_gerbil()
	sc_stbt.goto_basic_bandwidth()
	if not sc_stbt.check_state_basic_bandwidth():
		sc_stbt.enable_disable_basic_bandwidth()
	sc_stbt.set_basic_bandwidth()
	sc_stbt.close_interface()

def perf_time():
	"""
	perf_time : play movie for 30s then calculate the time from clicking exit playback to the playback detail page
	:return:
	"""
	sc_stbt.start_movie()
	sc_stbt.detect_movie(test_secs=30)
	sc_stbt.back_to_list(perf=True, name="from_the_end_of_playback_to_details_page_bar_3s")


sc_stbt.repeat(lambda: main(), occurence=1)
sc_stbt.back_to_home()
sc_stbt.open_library()
sc_stbt.goto_movies_menu()
sc_stbt.select_free_video()
sc_stbt.repeat(lambda: perf_time(), occurence=11)
