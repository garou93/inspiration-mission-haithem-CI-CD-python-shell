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

region_end_carousel = stbt.Region(x=31, y=209, width=933, height=113)

region_end_list = stbt.Region(x=200, y=114, width=704, height=172)
region_end_bottom=stbt.Region(x=27, y=315, width=908, height=156)

def navigation_():
	"""
	navigate in carousel and open the movie detail page after navigation
	:return:
	"""
	sc_stbt.navigation_list(menu = "carousel", press="KEY_RIGHT")
	sc_stbt.open_movie_detail_page(),
	sc_stbt.select_carousel(press="KEY_BACK")

def main_test1():
	"""
	main_test:: search for a movie
	back to home
	go to a carousel and scroll to the end of list
	go to the bottom of the home menu
	do navigation_()
	paly a movie for 5 mins
	:return:
	"""

	i=0
	while i < 4 :
		sc_stbt.back_to_home()
		sc_stbt.search_movie_amazon(movie_name= "hacksaw ridge")
		sc_stbt.back_to_home()
		sc_stbt.select_carousel(press="KEY_DOWN")
		while not sc_stbt.is_end_list_navigation(region_end_bottom):
			sc_stbt.navigation_list(menu="bottom",press="KEY_DOWN")
		sc_stbt.back_to_home()
		sc_stbt.select_carousel(press="KEY_DOWN")
		while not sc_stbt.is_end_list_navigation(region=region_end_carousel):
			sc_stbt.navigation_list(menu="carousel",press = "KEY_RIGHT")
		sc_stbt.select_carousel(press="KEY_DOWN")
		sc_stbt.repeat(lambda: navigation_(), occurence=20)
		sc_stbt.back_to_home()
		sc_stbt.open_library()
		sc_stbt.goto_movies_menu()
		sc_stbt.select_free_video()
		sc_stbt.start_movie()
		sc_stbt.detect_movie(test_secs=300)
		i+=1
		sc_stbt.debug("iteration number : " + str(i))


sc_stbt.repeat( lambda: main_test1(), occurence=1)
