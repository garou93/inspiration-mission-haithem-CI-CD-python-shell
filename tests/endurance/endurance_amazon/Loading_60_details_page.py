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

region_end_carousel = stbt.Region(x=31, y=209, width=933, height=113)

def navigation_stress():
    """
    navigation_stress :  navigate to a carousel then navigate in this carousel and after Key_Right navigate the movie detail page
    :return:
    """
    sc_stbt.navigation_list(menu="carousel" , press="KEY_RIGHT")
    sc_stbt.open_movie_detail_page()
    sc_stbt.select_carousel(press= "KEY_BACK")

def chek_and_navigate():
    """
    check if the carousel is over or not
    if the carousel is not over continue navigation
    else select another carousel and continue the navigation_stress()
    :return:
    """
    if sc_stbt.is_end_list_navigation(region=region_end_carousel):
        sc_stbt.select_carousel(press="KEY_DOWN")
        navigation_stress()
    else:
        navigation_stress()


sc_stbt.back_to_home()
sc_stbt.select_carousel(press= "KEY_DOWN")
sc_stbt.repeat(lambda: chek_and_navigate(),occurence=60)
