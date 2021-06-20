# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""
#
import sc_stbt
import time
import stbt

menu = sc_stbt.menu()
amazon_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/templates_amazon/"
amazon_path_template_is_menu = "/../../../trunk/tests/templates/templates_amazon/"
match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',confirm_method="normed-absdiff",match_threshold=0.2,confirm_threshold=0.3)



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

def step2 (perf=False):
    """
    start a movie and calculate time from clicking ok to the first UI of the playback
    then back to the detail page of the content
    :return:
    """
    sc_stbt.start_movie(perf=perf)
    sc_stbt.detect_movie(test_secs=50)
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
    sc_stbt.open_gerbil()
    sc_stbt.goto_basic_bandwidth()
    if not sc_stbt.check_state_basic_bandwidth():
        sc_stbt.enable_disable_basic_bandwidth()
    sc_stbt.set_basic_bandwidth()
    sc_stbt.close_interface()

    sc_stbt.repeat(lambda: step1(), occurence=1)
    sc_stbt.repeat(lambda: step2(), occurence=1)
    sc_stbt.quit_amazon()
    sc_stbt.is_amazon(press="KEY_OK")

    sc_stbt.repeat(lambda: step1(), occurence=1)
    sc_stbt.repeat(lambda: step2(perf=True), occurence=9)

sc_stbt.repeat(lambda: main_test(), occurence=1)
