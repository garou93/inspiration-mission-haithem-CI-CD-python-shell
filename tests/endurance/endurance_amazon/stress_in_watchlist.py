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


region_end_list = stbt.Region(x=200, y=114, width=704, height=172)

# sc_stbt.back_to_home()
# sc_stbt.goto_watchlist()
# sc_stbt.goto_movies_menu()
# sc_stbt.open_movie_detail_page()

while not sc_stbt.is_end_list_navigation(region=region_end_list):
        sc_stbt.open_movie_detail_page(press="KEY_OK")
        sc_stbt.back_to_list()
        sc_stbt.navigation_list(menu="list", press="KEY_RIGHT")


while sc_stbt.is_end_list_navigation(region=region_end_list):
    sc_stbt.back_to_home()

