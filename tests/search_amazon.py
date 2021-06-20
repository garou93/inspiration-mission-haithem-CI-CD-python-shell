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
import stbts
import stbt
import time
import networkx as nx



amazon_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/templates_amazon/"
amazon_path_template_is_menu = "/../../../trunk/tests/templates/templates_amazon/"
any_frame = amazon_path_template + "/search/any_frame/any_frame.png"

polling_secs = stbt.get_config("amazon", "polling_secs", type_=int)
test_secs = stbt.get_config("amazon", "test_secs", type_=int)
interval_secs = stbt.get_config("amazon", "interval_secs", type_=int)

path_mask_motion = amazon_path_template + "/masck_amazon_video/masck_amazon_video.png"

menu = sc_stbt.menu()
amazon = sc_stbt.video_tests(path_mask_motion)

def search_video_amazon(original_video_name):
    """
    search video in youtube
    :return:
    """
    open_search_amazon()

    if original_video_name is None:
        original_video_name = stbt.get_config("amazon", "movie_name")

    vide_name = original_video_name.replace(' ','#')

    list_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':']

    for i in range(len(vide_name)):

        if vide_name[i] in list_number:
            if check_keyboard_type() == "alphabetic keyboard":
                goto_cord('-')
            goto_cord(vide_name[i])

        else:
            if check_keyboard_type() == "numeric keyboard":
                goto_cord('-')
            goto_cord(vide_name[i])

    goto_list_select()
    if select_video_name(original_video_name) :
        sc_stbt.debug("Movie is Found")
        return True
    else:
        assert False, "Movie name does'nt exsist"


#-------------------------------Navigation Search------------------------------------


def open_search_amazon():
    """
    goto_search :: Api de navigation de Home primevideo vers search menu...
                   keyboard is automaticly selected ...
    :return:
    """
    menu.is_menu(press=["KEY_LEFT"],
                 path= amazon_path_template_is_menu + "/search/go_to_search/",
                 region_frame=stbt.Region (x=30,y=30 ,width=81 ,height=37 ),
                 timeout=2,
                 timeout_is_menu=20)

    menu.is_menu(press=["KEY_OK"],
                 text="Search",
                 region_text=stbt.Region (x=31, y=38, width=87, height=33),
                 timeout=3,
                 timeout_is_menu=20)
    is_keyboard()

    sc_stbt.debug("SEARCH MENU IS OPEND")


def is_keyboard():
    """
    is_keyboard :: check that the cursor is on the lettre q of the keyboard (first lettre)
    :return:
    """
    menu.is_menu(path= amazon_path_template_is_menu + "/search/keyboard_check/",
                 region_frame=stbt.Region (x=242 ,y=363 ,width=39 ,height=41),
                 timeout=2,
                 timeout_is_menu=20)

def check_keyboard_type():
    """
    check_keyboard_type: check type of keyboard alphabetic or numeric
    :return:
    """
    if menu.is_menu_template(perf=False,
                             path= amazon_path_template +"search/alphabetic/" ,
                             region_frame=stbt.Region(x=571,y=407,width=30,height=28),
                             timeout=3):

        return "alphabetic keyboard"
    elif menu.is_menu_template(perf=False,
                             path=amazon_path_template +"/search/numeric/",
                             region_frame=stbt.Region(x=572,y=407,width=30,height=28),
                             timeout=3):

        return "numeric keyboard"

# #------------ API to check in list suggestion -----------------------

def video_name_found(original_video_name):
    """
    video_name_found: check if video name is found in the suggestion list
    :return: True or False
    """
    if stbts.match_text(text=original_video_name,
                        region=stbt.Region(x=26, y=66, width=954, height=41),
                        timeout_secs=5, threshold=1).match :
        sc_stbt.debug("VIDEO NAME FOUND IN LIST SUGGESTION")
        return True
    else:
        sc_stbt.debug("VIDEO NAME NOT FOUND IN LIST SUGGESTION")
        return False


def goto_list_select():
    """
    goto_list_select; goto suggested list
    :return:
    """
    menu.is_menu(press=["KEY_UP"],
                 path=amazon_path_template_is_menu +"search/goto_list_select/",
                 region_frame=stbt.Region(x=27, y=98, width=266, height=10),
                 timeout=2,
                 timeout_is_menu=20)


def select_video_name(original_video_name):
    """
    select_video_name: select a video name from suggestion list
    :return:
    """
    try :
        if stbts.match_any_text(text=[original_video_name],
                                     region=stbt.Region(x=32, y=303, width=440, height=30),
                                     timeout_secs=2,
                                     threshold=0.8):
            sc_stbt.open_movie_detail_page()

        else:
            stbts.press_until_match_any_text(press_key="KEY_RIGHT",
                                         text=[original_video_name],
                                         region=stbt.Region(x=32, y=303, width=440, height=30),
                                         timeout_secs=2,
                                         timeout=60,
                                         threshold=0.8)
            sc_stbt.open_movie_detail_page()
        return True
    except:
        return False


def goto_cord(char):
    """
    :param char:
    :return:
    """
    target = matrix_amazon[char]

    target_x = target[0]
    target_y = target[1]

    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y

    global tolerance
    tolerance = 5

    start_time = time.time()
    while time.time() - start_time < 300:
        if source_x in range ((target_x-tolerance),(target_x+tolerance)) and source_y in range ((target_y-tolerance),(target_y+tolerance)):
            if char == "5":
                return True
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(3)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x, target_y, tolerance))
            sc_stbt.wait(3)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y
    return False

def _next_key(source_x, source_y, target_x, target_y,tolerance):
    if (source_y < target_y-tolerance):
        return "KEY_DOWN"
    if (source_y-tolerance > target_y):
        return "KEY_UP"
    if (source_x < target_x-tolerance):
        return "KEY_RIGHT"
    if (source_x-tolerance > target_x):
        return "KEY_LEFT"

def _next_key_list(source_y, target_y, tolerance):
    if (source_y < target_y-tolerance):
        return "KEY_LEFT"
    if (source_y-tolerance > target_y):
        return "KEY_RIGHT"



#######################


# keyboard amazon search
matrix_amazon = {}

# Debut de ligne qwertyuiop
matrix_amazon["q"] = [247, 371]
matrix_amazon["w"] = [283, 371]
matrix_amazon["e"] = [319, 371]
matrix_amazon["r"] = [355, 371]
matrix_amazon["t"] = [391, 371]
matrix_amazon["y"] = [427, 371]
matrix_amazon["u"] = [463, 371]
matrix_amazon["i"] = [499, 371]
matrix_amazon["o"] = [535, 371]
matrix_amazon["p"] = [571, 371]

# Debut de ligne asdfghjkl
matrix_amazon["a"] = [247, 407]
matrix_amazon["s"] = [283, 407]
matrix_amazon["d"] = [319, 407]
matrix_amazon["f"] = [355, 407]
matrix_amazon["g"] = [391, 407]
matrix_amazon["h"] = [427, 407]
matrix_amazon["j"] = [463, 407]
matrix_amazon["k"] = [499, 407]
matrix_amazon["l"] = [535, 407]

##debut de ligne zxcvbnm
matrix_amazon["z"] = [247, 443]
matrix_amazon["x"] = [283, 443]
matrix_amazon["c"] = [319, 443]
matrix_amazon["v"] = [355, 443]
matrix_amazon["b"] = [391, 443]
matrix_amazon["n"] = [427, 443]
matrix_amazon["m"] = [463, 443]

##debut de ligne 123
matrix_amazon["1"] = [247, 371]
matrix_amazon["2"] = [283,371]
matrix_amazon["3"] = [319,371]

##debut de ligne 456
matrix_amazon["4"] = [355,371]
matrix_amazon["5"] = [391,371]
matrix_amazon["6"] = [427,371]

##debut de ligne 7890
matrix_amazon["7"] = [463, 371]
matrix_amazon["8"] = [499, 371]
matrix_amazon["9"] = [535, 371]
matrix_amazon["0"] = [571, 371]

##bouton &123/ABC
matrix_amazon["-"] = [571,407]
matrix_amazon[":"] = [319, 407]

## bouton '
matrix_amazon["\'"] =[463, 443]

# bouton space
matrix_amazon["#"] = [499, 443]

# bouton clear
matrix_amazon["+"] = [607, 407]