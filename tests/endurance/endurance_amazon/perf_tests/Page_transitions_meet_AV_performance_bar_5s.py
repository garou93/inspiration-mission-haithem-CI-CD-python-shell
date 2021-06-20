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


def main():
	sc_stbt.open_gerbil()
	sc_stbt.goto_basic_bandwidth()
	if not sc_stbt.check_state_basic_bandwidth():
		sc_stbt.enable_disable_basic_bandwidth()
	sc_stbt.set_basic_bandwidth()
	sc_stbt.close_interface()

def perfs():
	"""
	 time to navigate to watchlist
	 time to navigate to movie detail page
	 time to navigate to tv show detail page
	:return:
	"""
	sc_stbt.back_to_home()
	sc_stbt.goto_watchlist(perf=True, name="navigate_to_watchlist")
	sc_stbt.open_movie_detail_page(perf=True, name="navigate_to_tv_show_detail_page")
	sc_stbt.back_to_list()
	sc_stbt.goto_movies_menu()
	sc_stbt.open_movie_detail_page(perf=True, name="navigate_to_movie_detail_page")


sc_stbt.repeat(lambda: main(), occurence=1)
sc_stbt.repeat(lambda: perfs(), occurence=11)