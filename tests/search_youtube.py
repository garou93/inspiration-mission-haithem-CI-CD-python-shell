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
import time
import stbts
import os

project = os.environ.get('STBT_PROJECT')
navigation=sc_stbt.navigation()
match_parameters = stbt.MatchParameters(match_threshold=0.96, confirm_threshold=0.2)
menu = sc_stbt.menu()
youtube_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/youtube/"
any_frame = youtube_path_template + "/search/any_frame/any_frame.png"
is_keyboard=youtube_path_template+"/search/any_frame/"
is_video_selected="/../../../trunk/tests/templates/youtube/search/is_video_selected/"
any_frame_list = youtube_path_template + "/search/keyboard/list_cursor.png"
path_selected_search = "/../../../trunk/tests/templates/youtube/search/"
keyboard =  "/../../../trunk/tests/templates/youtube/search/keyboard/"
alphabetic =  youtube_path_template+"/search/alphabetic/"
numeric =  youtube_path_template+"/search/numeric/"
youtube = sc_stbt.video_tests()
path_mask_blackscreen = youtube_path_template + "/black/mask_black.png"

android = eval(stbt.get_config ("adb","adb_press"))
keyboard_language = stbt.get_config("youtube", "keyboard_language")


def search_video(original_video_name=None,callable=None):
    """
    search video in youtube
    :return:
    """
    if original_video_name is None:
        original_video_name = stbt.get_config("youtube", "video_name")

    #open keyboard search youtube, and if android is True,
    #so this API write do a search with adb command and open a video
    open_search_youtube(original_video_name)

    # if product is not android
    if not android:
        youtube_keyboard = sc_stbt.youtube_keyboard(keyboard_language)
        youtube_keyboard.enter_text(original_video_name)
        youtube.open(path_mask_blackscreen=path_mask_blackscreen)
        sc_stbt.wait(5)

    if android :
        from android import write_text
        write_text(text=original_video_name)
        sc_stbt.combo_press(combo=["KEY_DOWN"], number_press=3, delay_sec=0.5)
        sc_stbt.combo_press(combo=["KEY_RIGHT"], number_press=3, delay_sec=0.5)

        if goto_cord('*',callable):
            try :
                menu.is_menu(press=["KEY_DOWN"],
                            text ="Result found",
                            path=is_video_selected,
                            region_frame=stbt.Region(x=268,y=406,width=133,height=124),
                            timeout=2,
                            timeout_is_menu=6,
                            match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                  confirm_method='none',
                                                                  match_threshold=0.9,
                                                                  confirm_threshold=0.3))
            except:
                sc_stbt.combo_press(["KEY_DOWN"],number_press = 3)

            youtube.open(path_mask_blackscreen=path_mask_blackscreen)
            sc_stbt.wait(10)
        else:
            assert False, "PROBLEM TO SELECT KEY SEARCH"




#-------------- API TO NAVIGUATE IN MENU SHEARCH YOUTUBE ----------------

def open_search_youtube(original_video_name):
    """
    open_search_youtube: go to menu search youtube
    :return:
    """
    sc_stbt.combo_press(combo=["KEY_LEFT"], number_press= 3,delay_sec = 0.3)
    menu.is_menu(press=["KEY_UP"],
                 path=path_selected_search,
                 region_frame=stbt.Region(x=207,y=91,width=11,height=11),
                 timeout=2,
                 timeout_is_menu=4)
    goto_keyboard()


def goto_keyboard():
    """
    goto_keayboard: goto keyboard (select first button A)
    :return:
    """
    if not android :
        menu.is_menu(press=["KEY_RIGHT"],
                 text="Keyboard",
                 path="/../../../trunk/tests/templates/youtube/search/keyboard/",
                 region_frame=stbt.Region(x=365,y=23,width=574,height=235),
                 timeout=2,
                 timeout_is_menu=6,
                 match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                       confirm_method='none',
                                                       match_threshold=0.97,
                                                       confirm_threshold=0.3))

        if keyboard_language == "spa":
            update_matrix_android(soft="mdw-spa")
    else :
        sc_stbt.combo_press(["KEY_RIGHT"],number_press =2 ,delay_sec = 0.5)
        sc_stbt.press("KEY_1")
        sc_stbt.wait(2)
        sc_stbt.combo_press(combo=["KEY_DEL"], number_press=3)
        sc_stbt.wait(2)

    sc_stbt.debug("KEYBOARD IS FOUND AND SELECTED")


def check_keyboard_type():
    """
    check_keyboard_type: check type of keyboard alphabetic or numeric
    :return:
    """
    if menu.is_menu_template(perf=False,
                             path=alphabetic,
                             region_frame=stbt.Region(x=640,y=58,width=142,height=131),
                             timeout=3):
        return "alphabetic"
    elif menu.is_menu_template(perf=False,
                             path=numeric,
                             region_frame=stbt.Region(x=640,y=58,width=142,height=131),
                             timeout=3):
        return "numeric"




# #------------ API to check in list suggestion -----------------------

def video_name_found(original_video_name):
    """
    video_name_found: check if video name is found in the suggestion list
    :return: True or False
    """
    region_video_name = None
    if stbts.match_text(text=original_video_name,
                        region=stbt.Region(x=130, y=69, width=261, height=351),
                        timeout_secs=3, threshold=1).match :
        region_video_name = stbts.match_text(text=original_video_name,
                                        region=stbt.Region(x=130, y=69, width=261, height=351),
                                        timeout_secs=3).region
        sc_stbt.debug("VIDEO NAME FOUND IN LIST SUGGESTION")
        return [True, region_video_name.y]
    else:
        sc_stbt.debug("VIDEO NAME NOT FOUND IN LIST SUGGESTION")
        return [False, region_video_name]



def goto_list_select():
    """
    goto_list_select; goto suggested list
    :return:
    """
    menu.is_menu(press=["KEY_LEFT"],
                 path=keyboard,
                 region_frame=stbt.Region(x=123,y=67,width=71,height=47),
                 timeout=3,
                 timeout_is_menu=30)



def select_video_name(list_value_video_name_found):
    """
    select_video_name: select a video name from suggestion list
    :return:
    """
    tolerance = 6
    try:
        target_y = list_value_video_name_found
    except:
        assert False, "VIDEO NAME NOT FOUND IN LIST SUGGESTION"
    target_y -= 10

    source = stbt.match(any_frame_list).position
    source_y = source.y

    start_time = time.time()
    while time.time() - start_time < 100:
        if source_y in range ((target_y-tolerance),(target_y+tolerance)):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(4)
            return True
        else:
            sc_stbt.press(_next_key_list(source_y, target_y, tolerance))
            sc_stbt.wait(4)
            source = stbt.match(any_frame_list).position
            source_y = source.y
    return False


#------------- API to write video name -----------------

def goto_cord(char='*', callable=None , timeout = 100):
    """

    :param char:
    :return:
    """
    tolerance = 18
    target = matrix_youtube[char]
    if callable is not None :
        generic_dict = callable()
        tolerance_sur_x = int (generic_dict['tol_search_x'])
        tolerance_sur_y = int (generic_dict['tol_search_y'])
        target[0] +=  tolerance_sur_x
        target[1] +=  tolerance_sur_y
    target_x = target[0]
    target_y = target[1]


    source = stbt.match(any_frame,
                        match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method='none', match_threshold=0.99, confirm_threshold=0.3),
                        region=stbt.Region(x=340,y=80,width=300,height=200)).position
    source_x = source.x
    source_y = source.y

    start_time = time.time()
    while time.time() - start_time < timeout:
        if source_x in range ((target_x-tolerance),(target_x+tolerance)) and source_y in range ((target_y-tolerance),(target_y+tolerance)):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(1)
            if callable is not None :
                target[0] -=  tolerance_sur_x
                target[1] -=  tolerance_sur_y
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x, target_y, tolerance))
            sc_stbt.wait(1)
            source = stbt.match(any_frame,
                                match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                      confirm_method='none',
                                                                      match_threshold=0.99, confirm_threshold=0.3),
                                region=stbt.Region(x=340,y=80,width=300,height=200)).position
            source_x = source.x
            source_y = source.y
    if callable is not None :
        target[0] -=  tolerance_sur_x
        target[1] -=  tolerance_sur_y
    return False


def _next_key(source_x, source_y, target_x, target_y, tolerance):
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
        return "KEY_DOWN"
    if (source_y-tolerance > target_y):
        return "KEY_UP"

def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)+1):
            yield chr(c)

def update_matrix_android(soft):
    """
    update_matrix_android: update keyboard for a new region
    :return:
    """
    global matrix_youtube
    if soft == "android":
        for i in matrix_youtube.keys():
            region_x = matrix_youtube[i]
            region_x[0] -= 26
            region_x[1] += 2
            matrix_youtube[i] = region_x
    elif soft == "mdw":
        for i in matrix_youtube.keys():
            region_x = matrix_youtube[i]
            region_x[0] += 26
            region_x[1] -= 2
            matrix_youtube[i] = region_x
    elif soft == "mdw-spa":
        for c in char_range('o', 't'):
            region_x = matrix_youtube.get(c)[0]
            region_x += 33
            matrix_youtube.get(c)[0] = region_x
        for c in char_range('v', 'z'):
            region_x = matrix_youtube.get(c)[0]
            region_x += 33
            matrix_youtube.get(c)[0] = region_x
        region_x = matrix_youtube.get('u')[0]
        region_y = matrix_youtube.get('u')[1]
        region_x -= 198
        region_y += 33
        matrix_youtube.get('u')[0] = region_x
        matrix_youtube.get('u')[1] = region_y



#######################
# keyboard youtube search
matrix_youtube = {}

# Debut de ligne abcdefg
matrix_youtube["a"] = [343, 83]
matrix_youtube["b"] = [376, 83]
matrix_youtube["c"] = [409, 83]
matrix_youtube["d"] = [442, 83]
matrix_youtube["e"] = [475, 83]
matrix_youtube["f"] = [508, 83]
matrix_youtube["g"] = [541, 83]

# Debut de ligne hijklmn
matrix_youtube["h"] = [343, 116]
matrix_youtube["i"] = [376, 116]
matrix_youtube["j"] = [409, 116]
matrix_youtube["k"] = [442, 116]
matrix_youtube["l"] = [475, 116]
matrix_youtube["m"] = [508, 116]
matrix_youtube["n"] = [541, 116]

##debut de ligne opqrstu
matrix_youtube["o"] = [343, 149]
matrix_youtube["p"] = [376, 149]
matrix_youtube["q"] = [409, 149]
matrix_youtube["r"] = [442, 149]
matrix_youtube["s"] = [475, 149]
matrix_youtube["t"] = [508, 149]
matrix_youtube["u"] = [541, 149]

##debut de ligne vwxyz-'
matrix_youtube["v"] = [343, 182]
matrix_youtube["w"] = [376, 182]
matrix_youtube["x"] = [409, 182]
matrix_youtube["y"] = [442, 182]
matrix_youtube["z"] = [475, 182]
matrix_youtube["-"] = [508, 182]
matrix_youtube["\'"] = [541, 182]

##debut de ligne 123
matrix_youtube["1"] = [343, 83]
matrix_youtube["2"] = [376, 83]
matrix_youtube["3"] = [409, 83]

##debut de ligne 456
matrix_youtube["4"] = [343, 116]
matrix_youtube["5"] = [376, 116]
matrix_youtube["6"] = [409, 116]

##debut de ligne 7890
matrix_youtube["7"] = [343, 149]
matrix_youtube["8"] = [376, 149]
matrix_youtube["9"] = [409, 149]
matrix_youtube["0"] = [442, 149]

##bouton &123/ABC
matrix_youtube["-"] = [583,116]

# bouton space
matrix_youtube["#"] = [347, 223]

# bouton clear
matrix_youtube["+"] = [451, 223]

# bouton search
matrix_youtube["*"] = [542, 223]
