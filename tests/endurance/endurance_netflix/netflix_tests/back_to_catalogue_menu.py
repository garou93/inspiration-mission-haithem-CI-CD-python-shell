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


if sc_stbt.back_to_netflix_movie_menu():
    sc_stbt.debug("MENU CATALOGUE IS FOUND")
else:
    assert False, "MENU CATALOGUE IS NOT FOUND"


