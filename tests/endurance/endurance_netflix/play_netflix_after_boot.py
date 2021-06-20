
import sc_stbt
import stbt
import time
import subprocess
from android import goto_netflix

menu = sc_stbt.menu()
global_path = sc_stbt.get_generic_template_path()
generic_path = sc_stbt.get_generic_template_path()



def check_stb_boot():
    """

    :return:
    """
    try:
        menu.is_menu(
                     path="/boot",
                     region_frame=stbt.Region(x=277, y=210, width=399, height=126),
                     timeout=3,
                     timeout_is_menu=70)
        sc_stbt.debug("REBOOT IS DONE")
        return time.time()
    except:
        assert False, "MENU NOT DISPLAYED AFTER REBOOT"



def navigation_stress_menu():

    sc_stbt.combo_press(combo=["KEY_RIGHT"],number_press=5)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_DOWN"],number_press=3)

    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_RIGHT"],number_press=3)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_RIGHT"],number_press=5)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_RIGHT"],number_press=5)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_DOWN"],number_press=2)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_UP"],number_press=2)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_RIGHT"],number_press=10)
    sc_stbt.wait(1)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_LEFT"],number_press=5)
    sc_stbt.open_video_netflix()
    sc_stbt.back_to_netflix_movie_menu()


#################################API Call#################################################

sc_stbt.test_power_on(lambda: check_stb_boot())
sc_stbt.wait(20)
sc_stbt.combo_press(combo=["KEY_HOME"],number_press=5)
sc_stbt.wait(5)
sc_stbt.go_to_netflix()
sc_stbt.open_video_netflix()
sc_stbt.back_to_netflix_movie_menu()
sc_stbt.repeat(lambda: navigation_stress_menu(), occurence=30)


