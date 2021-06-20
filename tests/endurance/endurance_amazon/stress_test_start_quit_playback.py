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

def step1():
    """
    steps: 1-go to home
           2-open library menu
           3-open movies menu
           4-searching a free video
           5-open the detail page of the free content
    :return:
    """
    sc_stbt.back_to_home()
    sc_stbt.open_library()
    sc_stbt.goto_movies_menu()
    sc_stbt.select_free_video()
    sc_stbt.open_movie_detail_page()

def step2():
        """
        start a movie and calculate time from clicking ok to the first UI of the playback
        then back to the detail page of the content
        :return:
        """

        sc_stbt.start_movie()
        sc_stbt.detect_movie()
        sc_stbt.open_movie_detail_page(press="KEY_BACK")

def main_test():
        """
        1-do step1
        2-do step2
        3-quit the application and reopen it
        4-repeat step 1
        5-repeat step2 9 times (9 calcule of the specifique perf)

        :return:
        """
        sc_stbt.repeat(lambda :step1(),occurence=1)
        sc_stbt.repeat(lambda :step2(),occurence=200)
sc_stbt.repeat(lambda :main_test(),occurence=1)

