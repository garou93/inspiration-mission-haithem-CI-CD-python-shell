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


netflix_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/netflix/"

match_parameters_is_menu = eval(stbt.get_config("netflix", "match_parameters_is_menu"))

match_parameters = eval(stbt.get_config("netflix", "match_parameters"))


language_menu = stbt.get_config("netflix", "language_menu")
language_profile = stbt.get_config("netflix", "language_profile")

tab_config = ['Search','Rechercher','Buscar']


menu = sc_stbt.menu()


def goto_keyboard():
    """
    goto_keyboard: goto keyboard menu in netflix
    :return:
    """
    #back to movie netflix menu
    if sc_stbt.back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    #goto config menu in netflix
    sc_stbt.goto_config_menu()
    #select settings menu
    menu.is_menu(press=["KEY_UP"],
                             path="/../../../trunk/tests/templates/netflix/search/",
                             region_frame=stbt.Region(x=151, y=133, width=48, height=63),
                             timeout=3,
                             timeout_is_menu=40)
    menu.is_menu(press=["KEY_OK"],
                     region_frame=stbt.Region(x=79, y=35, width=205, height=131),
                     path="/../../../trunk/tests/templates/netflix/search_netflix/keyboard/")




def search_netflix(original_movie_name):
    """
    search movie in netflix
    :return:
    """
    sc_stbt.get_statut_test("NETFLIX MENU NOT FOUND OR SESSION CONNECTED")


    movie_name = original_movie_name.replace(' ','#')
    movie_name = movie_name.lower()

    goto_keyboard()

    list_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(movie_name)):
        if movie_name[i] in list_number:
            sc_stbt.press("KEY_" + list_number[i])
            sc_stbt.wait(2)
        else:
            goto_cord(movie_name[i])
    goto_cord('5')
    stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[original_movie_name],
                                         region=stbt.Region(x=380, y=25, width=566, height=34),
                                         timeout_secs=3,
                                         timeout=60,
                                         threshold=0.7)
    sc_stbt.combo_press(combo=["KEY_OK"], number_press=2)
    play_mode = stbt.get_config("netflix", "play_mode")
    if play_mode == "resume":
        sc_stbt.press("KEY_OK")
    elif play_mode == "beginning":
        if stbt.wait_until(lambda: stbt.match_text(text="Resume",
                                                    region=stbt.Region(x=63, y=265, width=277, height=102),
                                                    threshold=0.8),
                                                    timeout_secs=1):
                sc_stbt.press("KEY_DOWN")
                sc_stbt.wait(1)
                sc_stbt.press('KEY_OK')
        else:
            sc_stbt.press("KEY_OK")
    sc_stbt.wait(20)



any_frame = netflix_path_template + "/search_netflix/any_frame/any_frame.png"
tolerance = 5

def goto_cord(char):
    """

    :param char:
    :return:
    """
    target = matrix_netflix[char]

    target_x = target[0]
    target_y = target[1]

    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y

    global tolerance
    tolerance = 6

    start_time = time.time()
    while time.time() - start_time < 300:
        if source_x in range ((target_x-tolerance),(target_x+tolerance)) and source_y in range ((target_y-tolerance),(target_y+tolerance)):
            if char == "5":
                return True
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(2)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x, target_y))
            sc_stbt.wait(4)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y
    return False

def _next_key(source_x, source_y, target_x, target_y):
    if (source_y < target_y-tolerance):
        return "KEY_DOWN"
    if (source_y-tolerance > target_y):
        return "KEY_UP"
    if (source_x < target_x-tolerance):
        return "KEY_RIGHT"
    if (source_x-tolerance > target_x):
        return "KEY_LEFT"


#######################
# keyboard netflix search
matrix_netflix = {}

# Debut de ligne abcdef
matrix_netflix["a"] = [62, 77]
matrix_netflix["b"] = [95, 77]
matrix_netflix["c"] = [128, 77]
matrix_netflix["d"] = [161, 77]
matrix_netflix["e"] = [194, 77]
matrix_netflix["f"] = [227, 77]

# Debut de ligne ghijkl
matrix_netflix["g"] = [62, 110]
matrix_netflix["h"] = [95, 110]
matrix_netflix["i"] = [128, 110]
matrix_netflix["j"] = [161, 110]
matrix_netflix["k"] = [194, 110]
matrix_netflix["l"] = [227, 110]

##debut de ligne mnopqr-
matrix_netflix["m"] = [62, 143]
matrix_netflix["n"] = [95, 143]
matrix_netflix["o"] = [128, 143]
matrix_netflix["p"] = [161, 143]
matrix_netflix["q"] = [194, 143]
matrix_netflix["r"] = [227, 143]

##debut de ligne stuvwx-
matrix_netflix["s"] = [62, 176]
matrix_netflix["t"] = [95, 176]
matrix_netflix["u"] = [128, 176]
matrix_netflix["v"] = [161, 176]
matrix_netflix["w"] = [194, 176]
matrix_netflix["x"] = [227, 176]

# debut de ligne  yz
matrix_netflix["y"] = [62, 209]
matrix_netflix["z"] = [95, 209]

# bouton space
matrix_netflix["#"] = [62, 44]

# key 5
matrix_netflix["5"] = [62, 242]






