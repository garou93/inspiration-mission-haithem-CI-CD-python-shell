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


def main_test():
    """
    go to watchlist
    open moviemenu in watchlist
    navigate and count
    if posters is under 50
    go to home and add contents to watchlis
    else test is done
    :return:
    """

    sc_stbt.back_to_home()
    sc_stbt.goto_watchlist()
    sc_stbt.goto_movies_menu()

    count = sc_stbt.count_navigation(menu="list", press="KEY_RIGHT")
    nb = 50 - count
    if nb > 0:
        sc_stbt.back_to_home()
        sc_stbt.repeat(lambda: sc_stbt.select_carousel(press="KEY_DOWN") ,occurence=2)
    else:
        stbt.debug("Test is done OK")

    while nb > 0:
        if not sc_stbt.is_add_to_watchlist():
            sc_stbt.navigation_list(menu="carousel", press="KEY_DOWN")
        else:
            sc_stbt.add_to_watchlist()
            nb -= 1
            stbt.debug("Test is done OK", str(nb))

sc_stbt.repeat(lambda: main_test(),occurence=3)