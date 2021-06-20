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
import stbts
import time
import android

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

amazon_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/templates_amazon/"
amazon_path_template_is_menu = "/../../../trunk/tests/templates/templates_amazon/"

polling_secs = stbt.get_config("amazon", "polling_secs", type_=int)
test_secs = stbt.get_config("amazon", "test_secs", type_=int)
interval_secs = stbt.get_config("amazon", "interval_secs", type_=int)

path_mask_motion = amazon_path_template + "/masck_amazon_video/masck_amazon_video.png"
path_mask_buffer= amazon_path_template + "/masck_buffer/masck_amazon_video.png"


region_end_carousel = stbt.Region(x=31, y=209, width=933, height=113)
region_end_list = stbt.Region(x=200, y=114, width=704, height=172)
region_end_bottom = stbt.Region(x=27, y=315, width=908, height=156)

guide = sc_stbt.guide()
menu = sc_stbt.menu()
amazon = sc_stbt.video_tests(path_mask_motion)
prime = sc_stbt.video()

# ------------------ Menu Amazon --------------------------

def is_amazon(press=None, perf=False, perf_name=None):
    """
    is_amazon: check if amazon menu is displayed
                when press is (KEY_OK) it open and check the Prime video
                perf is true : calculate the time it takes to open the APP
    :return: True or False
    """
    if press is None:
        try :
            menu.is_menu(perf=perf,
                     perf_name=perf_name,
                     text="Home",
                     path=amazon_path_template_is_menu + "home/",
                     region_frame=stbt.Region(x=103, y=25, width=98, height=45),
                     timeout=5,
                     timeout_is_menu=15)
            sc_stbt.debug("AMAZON APP IS DISPLAYED")
            return True
        except:
            sc_stbt.debug("AMAZON APP IS NOT DISPLAYED")
            return False
    else:
        try :
            menu.is_menu(perf=perf,
                     perf_name=perf_name,
                     press=[press],
                     text="Home",
                     path=amazon_path_template_is_menu + "home/",
                     region_frame=stbt.Region(x=103, y=25, width=98, height=45),
                     timeout=5,
                     timeout_is_menu=5)
            sc_stbt.debug("AMAZON APP IS DISPLAYED")
            return True
        except:
            sc_stbt.debug("AMAZON APP IS NOT DISPLAYED")
            return False

def select_carousel(press):
    """
	select_carousel:press == "KEY_DOWN" go to carousel from home bar
	            press== "KEY_BACK" from movie detail page in carousel to carousel again

	:return:
	"""
    menu.is_menu(press=[press],
                 text="Home",
                 region_text=stbt.Region(x=41, y=31, width=52, height=27),
                 timeout=5,
                 timeout_is_menu=20)
    sc_stbt.debug("Carousel is selected")


def back_to_home():
    """
    Back_to_home : retourner vers le Home du Prime video
    :return:
    """

    if is_amazon():
        sc_stbt.debug("You ARE ALLREADY IN AMAZON HOME")
    else:
        try:
            menu.is_menu(text="Search",
                         region_text=stbt.Region(x=21, y=31, width=66, height=27),
                         path=amazon_path_template_is_menu + "/back_to_home/",
                         region_frame=stbt.Region(x=192, y=26, width=101, height=38),
                         timeout=2,
                         timeout_is_menu=2)
        except:
            menu.is_menu(press=["KEY_BACK"],
                         text="Search",
                         region_text=stbt.Region(x=21, y=31, width=66, height=27),
                         path=amazon_path_template_is_menu + "/back_to_home/",
                         region_frame=stbt.Region(x=192, y=26, width=101, height=38),
                         timeout=5,
                         timeout_is_menu=30)
        sc_stbt.combo_press(combo=["KEY_DOWN"], number_press=2)
        menu.is_menu(press=["KEY_BACK"],
                     text="Amazon Menu",
                     path=amazon_path_template_is_menu + "/home/",
                     region_frame=stbt.Region(x=107, y=21, width=96, height=54),
                     timeout=5,
                     timeout_is_menu=10)


# ----------------- Navigate carousl --------------------

def is_end_list_navigation(region):
    """
    is_end_carousel:  check if the carousel has finish
    :return:
    """
    if menu.is_menu_template(perf=False,
                             path=amazon_path_template + "/carousel/EndCarousel/",
                             region_frame=region,
                             timeout=3):
        sc_stbt.debug("list is over")
        return True
    else:
        sc_stbt.debug("list is not over")
        return False


def navigation_list(menu="carousel", press="KEY_RIGHT"):
    """
    navigation_list : navigation in list of movies
    :return: True,True : navigation done + end list or carousel
             True, False: navigation done + not end list or carousel
             False, False, problem navigation
             menu == carousel : navigation in carousel list
             menu == list : navigation in library or watchlist
             menu == bottom : navigation to the bottom of home PRIME VIDEO
             press == key_Right : navigation from left to right
             press == key_left : navigation from left to right
             press == down : navigation from up to down
    """
    guide.crop_press(press=press,
                     region_found=stbt.Region(x=42, y=64, width=845, height=455))
    sc_stbt.wait(5)
    if stbt.wait_until(lambda: stbt.match("frame.png",
                                          region=stbt.Region(x=37, y=58, width=850, height=460),
                                          match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                confirm_method='none',
                                                                                match_threshold=0.85,
                                                                                confirm_threshold=0.3)),
                       timeout_secs=3):
        if menu == "carousel":
            if is_end_list_navigation(region_end_carousel):
                sc_stbt.debug("RUN OUT OF CAROUSEL")
                return [True, True]
            else:
                sc_stbt.debug("PROBLEM IN NAVIGATION CAROUSEL")
                return [False, False]
        elif menu == "list":
            if is_end_list_navigation(region_end_list):
                sc_stbt.debug("RUN OUT OF LIST")
                return [True, True]
            else:
                sc_stbt.debug("PROBLEM IN NAVIGATION LIST")
                return [False, False]
        elif menu == "bottom":
            if is_end_list_navigation(region_end_bottom):
                sc_stbt.debug("we have reach the bottom of home menu")
                return [True, True]
            else:
                sc_stbt.debug("PROBLEM IN NAVIGATION TO BOTTOM")
                return [False, False]
        else:
            assert False, "MENU NOT EXIST"
    else:
        sc_stbt.debug("Navigation is Done")
        return [True, False]


# ---------------- Navigation Movies -----------------------------

def open_movie_detail_page(press="KEY_OK", perf=True, name=None):
    """
    open_movie_detail_page: cette api a le but d aller vers la page de detail d un film
    press KEY_BACK ---> from movie to movie detail page
    press KEY_OK -----> from poster of the movie selected to his detail page
    :return:
    """
    menu.is_menu(perf=perf,
                 perf_name=name,
                 press=[press],
                 path=amazon_path_template_is_menu + "/detail_page/",
                 text="Audio Languages",
                 region_frame=stbt.Region(x=234, y=64, width=574, height=43),
                 timeout=10,
                 timeout_is_menu=10)
    sc_stbt.debug("Detail page is displayed")


def search_movie_amazon(movie_name=None):
    """
    search_movie_amazon: API that search for movie by writing his name
    :return:
    """
    sc_stbt.search_video_amazon(movie_name)


def open_library(callable = None):
    """
    open_library: open library menu
    :return:
    """

    if callable is not None :

        generic_dict = callable()
        menu.is_menu(press = ["KEY_RIGHT"],
             text_color = generic_dict['text_color'],
             text = "Video Library",
             region_text = stbt.Region(x=492, y=33, width=120, height=27),
             timeout = 2,
             timeout_is_menu = 14)
    else:
        menu.is_menu(press=["KEY_RIGHT"],
                 text="Open Library",
                 path=amazon_path_template_is_menu + "/Library/",
                 #region_frame=stbt.Region(x=446, y=28, width=217, height=40),
                 region_frame=stbt.Region(x=482, y=26, width=189, height=44),
                 match_parameters = stbt.MatchParameters(match_method='sqdiff-normed',
                                                                   confirm_method="absdiff", match_threshold=0.85,
                                                                   confirm_threshold=0.85),
                 timeout=2,
                 timeout_is_menu=20)

    menu.is_menu(press = ["KEY_OK"],
                 text = "Library",
                 region_text = stbt.Region(x=20, y=28, width=118, height=49),
                 timeout = 3,
                 wait_after_press = 2,
                 timeout_is_menu = 5)
    sc_stbt.debug("Video Library IS OPEND")




def back_to_list(perf=True, name=None):
    """
    back_to_library: back to list movies from watchlist or library
    :return:
    """
    try:
        menu.is_menu(text="Movies",
                     region_text=stbt.Region(x=128, y=61, width=90, height=39),
                     timeout=0,
                     timeout_is_menu=2)
    except:
        menu.is_menu(perf=perf,
                     press=["KEY_BACK"],
                     text="Movies",
                     region_text=stbt.Region(x=128, y=61, width=90, height=39),
                     timeout=10,
                     timeout_is_menu=10,
                     perf_name=name)
    sc_stbt.debug("We Are In Movies Interface")


def goto_movies_menu():
    """
    goto_movies_menu :From tv shows menu, goto movies interface in wathclist or video library
    :return:
    """
    try :
        menu.is_menu(press=["KEY_UP"],
                     text="MOVIES SELECTED",
                     path=amazon_path_template_is_menu + "/Movies/movie_menu/",
                     region_frame=stbt.Region(x=128, y=69, width=107, height=37),
                     timeout=3,
                     timeout_is_menu=3)
        sc_stbt.debug("movie menu is selected")
    except :
        menu.is_menu(press=["KEY_RIGHT"],
                     text="MOVIES SELECTED",
                     path=amazon_path_template_is_menu + "/Movies/movie_menu/",
                     region_frame=stbt.Region(x=128, y=69, width=107, height=37),
                     timeout=3,
                     timeout_is_menu=10)
        sc_stbt.debug("movie menu is selected")
    menu.is_menu(press=["KEY_OK"],
                 text="Movies",
                 region_text=stbt.Region(x=128, y=61, width=90, height=39),
                 timeout=2,
                 wait_after_press=5,
                 timeout_is_menu=20)


def select_free_video():
    """
    select_free_video : sert a chercher et lancer des Free videos
    :return:
    """
    if menu.is_menu_template(perf=False,
                             path=amazon_path_template + "/Movies/play_mov/",
                             region_frame=stbt.Region(x=11, y=296, width=475, height=59),
                             match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                   confirm_method="absdiff", match_threshold=0.8,
                                                                   confirm_threshold=0.3)):
        sc_stbt.debug("WE FOUND A FREE MOVIE")

    else:
        menu.is_menu(press=["KEY_RIGHT"],
                     path=amazon_path_template_is_menu + "/Movies/play_mov/",
                     region_frame=stbt.Region(x=11, y=296, width=475, height=59),
                     timeout=2,
                     wait_after_press=1,
                     timeout_is_menu=120)

        sc_stbt.debug("WE FOUND A FREE MOVIE")


def start_movie(perf=False):
    """
    start_movie: start movie: watch now or play from beginning
    :return:
    """
    try:
        menu.is_menu(path=amazon_path_template_is_menu + "/Movies/start_mov/",
                     region_frame=stbt.Region(x=19, y=279, width=543, height=111),
                     timeout=2, timeout_is_menu=2)
    except:
        menu.is_menu(press=["KEY_DOWN"],
                     path=amazon_path_template_is_menu + "/Movies/trailer/",
                     region_frame=stbt.Region(x=19, y=279, width=543, height=111),
                     timeout=5, timeout_is_menu=20)

        menu.is_menu(press=["KEY_RIGHT"],
                     path=amazon_path_template_is_menu + "/Movies/start_mov/",
                     region_frame=stbt.Region(x=19, y=279, width=543, height=111),
                     timeout=5, timeout_is_menu=20)

    if perf == False:
        amazon.open()
    else:
        match = True
        press = "KEY_OK"
        sc_stbt.press(press)
        start_time = time.time()
        while match and (time.time() - start_time) < 300:
            if menu.is_menu_template(perf=False,
                                     path=amazon_path_template + "/spinner",
                                     region_frame=stbt.Region(x=462, y=252, width=40, height=39),
                                     timeout=0.6,
                                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method="normed-absdiff",
                                                                           match_threshold=0.1,
                                                                           confirm_threshold=0.3)):
                sc_stbt.debug("Loading")
                match = True
            else:
                sc_stbt.debug("Loading is over")
                match = False
                if perf and not match:
                    endtime_perf1 = (time.time() - start_time)
                    endtime_perf = endtime_perf1 - 1.42
                    sc_stbt.write_csv_file("TTFF_meets_AV_performance_Bar_12s.csv", [["a", endtime_perf]])
        if time.time() - start_time > 300:
            assert False, "Spinner doesn't despear"
    sc_stbt.wait(3)

def detect_movie(test_secs_audio=20,test_secs=20):
    """
    detect_movie: detection motion and audio
    :return:
    """

    amazon.test_motion_audio(test_secs)
    # aud = sc_stbt.audio_tests()
    #
    # sc_stbt.multi_threading(lambda: amazon.test_motion(polling_secs=5,test_secs=test_secs),
    #                         lambda: aud.test_audio(polling_secs_audio=2 ,test_secs_audio=test_secs_audio))


def goto_watchlist(perf=False, name=None):
    """
    goto_watchlist :: Api de navigation de Home primevideo vers watchlist
    :return:
    """

    menu.is_menu(press=["KEY_RIGHT"],
                 path=amazon_path_template_is_menu + "/watchlist/open_watchlist",
                 region_frame=stbt.Region(x=636, y=28, width=169, height=40),
                 timeout=2,
                 timeout_is_menu=20)

    menu.is_menu(perf=perf,
                 perf_name=name,
                 press=["KEY_OK"],
                 text="Watchlist",
                 region_text=stbt.Region(x=30, y=32, width=121, height=44),
                 timeout=3,
                 timeout_is_menu=20)
    sc_stbt.debug("Watchlist IS OPEND")


def count_navigation(menu="list", press="KEY_RIGHT"):
    """
    count_navigation: navigate in list or carousel and count number of posters
    :return:
    """
    count = 1
    start_time = time.time()
    exit_ = True
    while exit_ and start_time - time.time() < 6000:
        end = navigation_list(menu=menu, press=press)
        if end[0] and not end[1]:
            count += 1
            sc_stbt.debug("counter", str(count))
        elif not end[0] and not end[1]:
            assert False, "PROBLEME NAVIGATION"
            # stbt.debug ("PROBLEME NAVIGATION")
        elif end[0] and end[1]:
            exit_ = False
    return count


# --------------------------------- trick mode amazon ----------------------------------

def test_amazon_motion(polling_secs=polling_secs):
    """
    test_amazon_motion: detect motion from amazon video
    :return: true where motion is detected , False is not
    """

    sc_stbt.get_statut_test("amazon MENU NOT FOUND")
    amazon.test_motion(polling_secs=polling_secs,
                       test_secs=test_secs,
                       interval_secs=interval_secs)

def test_amazon_pause(test_secs=18,
                      polling_secs=8,
                      interval_secs=8):
    """
    test_amazon_pause: check video is paused
    :return:    *if moition is not detected (video paused )==> play() (make video play ==> pause (make video
                pause)
                * elif motion is detected (video pause) ==> pause (make video pause)

                return false when:
                1) if video paused ==> when play() not done (motion not detected)
                2) if video paused ==>  play() done ==> when pause() not done (motion detected)
                3) if video played ==> when pause() not done (motion detected)
    """

    sc_stbt.get_statut_test("amazon MENU NOT FOUND")

    amazon.unit_pause(test_secs=test_secs,
                         polling_secs=polling_secs,
                         interval_secs=interval_secs,
                         key_pause="key_pause")
    sc_stbt.wait(2)

def test_amazon_play(test_secs=24,
                      polling_secs=12,
                      interval_secs=12):
    """
    test_amazon_play: check video is played
    :return: *if moition is detected (video played ) ==> pause() (make video pause)==> play (make video play)
                * elif motion is not detected (video paused) ==> play (make video play)

                return false when:
                1) if video played: when pause() not done (motion detected)
                2) if video played ==>  pause() done ==> when play() not done (motion not detected)
                3) if video paused ==> when play() not done (motion not detected)
    """

    sc_stbt.get_statut_test("amazon MENU NOT FOUND")
    amazon.unit_play(test_secs=test_secs,
                     polling_secs=polling_secs,
                     interval_secs=interval_secs)
    sc_stbt.wait(2)

def test_amazon_fastforward(occurence_forward=3,
                            key_forward="KEY_FASTFORWARD",
                            wait_pause_secs=2):
    """
    test_amazon_fastforward: check motion is forwarded
    :return:
            * Make video play with test_youtube_play()
            * use trick_mode with press= forward of video class (see how to use video)
    """
    sc_stbt.get_statut_test("amazon MENU NOT FOUND")

    amazon.unit_fastforward(occurence_forward=occurence_forward,
                       key_forward=key_forward,
                       key_pause="KEY_PAUSE",
                       wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY'])
    sc_stbt.wait(2)

def test_amazon_rewind(occurence_rewind=2,
                       wait_pause_secs=2):
    """
    test_amazon_fastforward: check motion is rewinded
    :return: * Make video play with test_youtube_play()
             * use trick_mode with press= rewind of video class (see how to use video)
    """
    sc_stbt.get_statut_test("amazon MENU NOT FOUND")
    amazon.unit_rewind(occurence_rewind=occurence_rewind,
                       wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY'])
    sc_stbt.wait(2)
# -------------------------------------------------------------------------

def quit_amazon(press="KEY_EXIT"):
    """
    exit_amazon:: Exit application to apps menu
    :return:
    """
    guide.crop_press(press=press,
                     region_found=stbt.Region(x=42, y=64, width=845, height=455))
    sc_stbt.wait(2)
    if stbt.wait_until(lambda: stbt.match("frame.png",
                                          region=stbt.Region(x=40, y=60, width=850, height=460),
                                          match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                confirm_method='none',
                                                                                match_threshold=0.85,
                                                                                confirm_threshold=0.3)),
                       timeout_secs=5):
        assert False, "user still in Prime Video APP"
        # stbt.debug ("user still in Prime Video APP")
    else:
        stbt.debug("Prime Video is closed")


def exit_amazon():
    """
    exit_amazon: exit from amazon live or menu
    :return:
    """
    back_to_home()
    menu.is_menu(press = ["KEY_BACK", "KEY_UP"],
                 text = "Exit the app",
                 region_text = stbt.Region(x=395, y=193, width=166, height=44),
                 timeout = 2,
                 timeout_is_menu = 10)

    guide.crop_press(press="KEY_OK",
                     region_found=stbt.Region(x=42, y=64, width=845, height=455))
    sc_stbt.wait(1)
    if stbt.wait_until(lambda: stbt.match("frame.png",
                                          region=stbt.Region(x=40, y=60, width=850, height=460),
                                          match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                confirm_method='none',
                                                                                match_threshold=0.85,
                                                                                confirm_threshold=0.3)),
                       timeout_secs=3):
        assert False, "user still in Prime Video APP"
    else:
        stbt.debug("Prime Video is closed")


def is_add_to_watchlist():
    """
    is_add_to_watchlist:: check if the selected movie exsist in watchlist or not
    :return:
    """
    try:
        menu.is_menu(path=amazon_path_template_is_menu + "/watchlist/add_towatchlist/",
                     region_frame=stbt.Region(x=775, y=474, width=185, height=40),
                     timeout=2,
                     timeout_is_menu=8)
        return True
    except:
        return False


def add_to_watchlist():
    """
    add_to_watchlist:: add the selected movie to watchlist if he's not allready added
    :return:
    """
    menu.is_menu(press=["KEY_GREEN"],
                 path=amazon_path_template_is_menu + "/watchlist/check_add/",
                 region_frame=stbt.Region(x=714, y=469, width=260, height=46),
                 timeout=4,
                 wait_after_press=1,
                 timeout_is_menu=14)

def open_catflap(catflap = "movie details"):
    """
    open_catflap : Api that dispaly catflap in playback or in home (build infos and streaming details
    :param catflap:
    :return:
    """
    sc_stbt.wait(1)
    android1 = (stbt.get_config("android", "android"))
    if android1 :
        android.adb_cmd(cmd="shell input keyevent KEYCODE_PROG_RED KEYCODE_PROG_GREEN KEYCODE_PROG_BLUE KEYCODE_PROG_YELLOW")
    else :
        press = sc_stbt.combo_press(combo=["KEY_RED","KEY_GREEN","KEY_BLUE","KEY_YELLOW" ], delay_sec=0.3)
        if catflap == "build information":
            try:
                menu.is_menu(press=press,
                    text="build information",
                    region_text= stbt.Region(x=381, y=42, width=203, height=38),
                    timeout=2,
                    timeout_is_menu=2)
                sc_stbt.debug("Build informations are displayed")
                return True
            except:
                sc_stbt.debug("Catflap is not displayed")
                return False
        if catflap == "streaming session details":
            try:
                sc_stbt.wait(1)
                press = sc_stbt.combo_press(combo=["KEY_RED","KEY_GREEN","KEY_BLUE","KEY_YELLOW" ], delay_sec=0.3)
                menu.is_menu(press=press,
                    text="streaming session details",
                    region_text= stbt.Region(x=343, y=77, width=272, height=42),
                    timeout=1,
                    timeout_is_menu=3)
                sc_stbt.debug("streaming session details are displayed")
                return True
            except:
                sc_stbt.debug("Catflap is not displayed")
                return False
        if catflap == "movie details":
            try :
                menu.is_menu(press=press,
                    text="Streaming method",
                    region_text= stbt.Region(x=58, y=31, width=136, height=20),
                    timeout=1,
                    timeout_is_menu=2)
                sc_stbt.debug("Movie Details are displayed")
                return True
            except :
                sc_stbt.debug("Catflap is not displayed")
                return False
        else:
            assert False, "MENU NOT EXIST"

def get_error_info(text="error count"):
    """
    get_info : API that gets information from catflap and note it in a Txt file
    :param text:
    :return:
    """
    if text == "error count":
        region_text= stbts.match_text(text= text,
                                          region=stbt.Region(x=487, y=55, width=315, height=202),
                                          threshold=0.9).region


        info = sc_stbt.is_text(threshold=0.8,
                       region=stbt.Region (x= region_text.x + region_text.width, y=region_text.y,width = 15,height= region_text.height),
                       mode=stbt.OcrMode.SINGLE_LINE,
                       timeout=10)
        sc_stbt.write_csv_file(text+".txt", [[info]])

    elif text == "buffer count":

         region_text= stbts.match_text(text= text,
                                          region=stbt.Region(x=487, y=55, width=315, height=202),
                                          threshold=0.9).region



         info = sc_stbt.is_text(threshold=0.8,
                       region=stbt.Region (x= region_text.x + region_text.width, y=region_text.y,width = 15,height= region_text.height),
                       mode=stbt.OcrMode.SINGLE_LINE,
                       timeout=10)
         sc_stbt.write_csv_file(text+".txt", [[info]])
         return info
    else :
        assert False, "catflap info is not found"
    # return info

def open_settings():
    """
    open_settings : open settings menu
    :param text:
    :return:
    """

    menu.is_menu(press=["KEY_RIGHT"],
                 path=amazon_path_template_is_menu + "/Settings/set",
                 region_frame=stbt.Region(x=693, y=24, width=225, height=42),
                 timeout=2,
                 timeout_is_menu=30)

    menu.is_menu(press=["KEY_OK"],
             text="Settings",
             region_text=stbt.Region(x=26, y=37, width=94, height=36),
             timeout=3,
             timeout_is_menu=6)
    sc_stbt.debug("PRIME VIDEO SETTINGS MENU IS DISPLAYED")

def deregister_your_device():
    """
    deregister_your_device : api that select the option deregister your device in settings menu
    than sign out from amazon account
    :param text:
    :return:
    """

    menu.is_menu(press=["KEY_RIGHT"],
             path=amazon_path_template_is_menu + "/Settings/deregister/",
             region_frame=stbt.Region(x=18, y=83, width=930, height=213),
             timeout=4,
             timeout_is_menu=24)

    menu.is_menu(press=["KEY_OK"],
                 path=amazon_path_template_is_menu + "/Settings/confirm_deregister/",
                 region_frame=stbt.Region(x=480, y=156, width=185, height=48),
                 timeout=4,
                 timeout_is_menu=8)
    sc_stbt.wait(2)
    menu.is_menu(press=["KEY_OK"],
                 text="Deregister your device",
                 region_text=stbt.Region(x=366, y=186, width=225, height=31),
                 timeout=4,
                 timeout_is_menu=8)
    sc_stbt.debug("PLEASE NOTE : YOUR DEVICE WILL BE SIGNED OUT...")

    menu.is_menu(press=["KEY_OK"],
                 text="Success",
                 region_text=stbt.Region(x=432, y=211, width=102, height=22),
                 timeout=15,
                 timeout_is_menu=30)
    if stbts.match_text("Success",
                        region=stbt.Region(x=432, y=211, width=102, height=22),
                        timeout_secs=10).match:
        sc_stbt.press("KEY_OK")
        sc_stbt.debug("DEREGESTRATION IS DONE")
        sc_stbt.wait(4)
        return True
    else :
        sc_stbt.debug("YOUR ARE STILL LOGED IN THE PRIME ACCOUNT")
        return False

def get_signin_code():

    code = sc_stbt.get_text(region=stbt.Region(x=149,y=247,width=226,height=53),mode=stbt.OcrMode.SINGLE_WORD)
    code_1= str(code)
    return code_1

def get_new_signin_code():

    guide.crop_press(press="KEY_OK",
                     region_found=stbt.Region(x=149,y=247,width=226,height=53))
    sc_stbt.wait(2)
    if stbt.wait_until(lambda: stbt.match("frame.png",
                                          region=stbt.Region(x=40, y=60, width=850, height=460),
                                          match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                confirm_method='none',
                                                                                match_threshold=0.85,
                                                                                confirm_threshold=0.3)),
                       timeout_secs=3):
        sc_stbt.debug("NEW CODE IS NOT GENERATED")
        return False
    else:
        stbt.debug("NEW CODE IS GENERETED")
        return True

# def get_catflap(menu_catflap="build information",timeout=None):
#
#     if timeout is None :
#         timeout = eval(stbt.get_config("Amazon", "timeout"))
#
#     name_list = []

#     if menu_catflap== "build information" :
#             name_list= ["oslocale","manufacturer","client bucket","model name","chipset","DTID","middleware version","Firmware","AVPK","ruby","oauthurl","blast url","init.js","atv endpoint"]
#     elif menu_catflap == "streaming session details":
#             name_list = ['Error Count','Buffer Count',"Asin s Streamed","Total Errors","Total Buffers","Recent Errors"]
#     else:
#             assert False, "menu_catflap is not found"
#     for item in name_list:
#         if menu_catflap== "build information" :
#             target = build_info_name[item]
#         elif menu_catflap == "streaming session details":
#             target = streaming_details[item]
#
#         element = stbt.get_config("Amazon", item)
#         region_x = target[0]
#         region_y = target[1]
#         val_item = sc_stbt.is_text(threshold=0.8,
#                                  region=stbt.Region(x=region_x,y=region_y,width=711,height=16),
#                                  mode=stbt.OcrMode.SINGLE_LINE,
#                                  timeout=timeout)
#         sc_stbt.write_csv_file("build_info.txt", [[val_item]])
        # if menu.is_menu(text=element,
        #              region_text=stbt.Region(x=region_x,y=region_y,width=711,height=16),
        #              timeout_is_menu=14,
        #              timeout=1).match:
        #     sc_stbt.debug("OKKKKKKKKKKKKKKKKKKKKKK")
        # else :
        #     assert False, "NOT OKKKKKKKKKKKKKKK"

# ------------- API of Gerbil Tests -----------


def open_gerbil():
    """
    open_gerbil: open_gerbil interface
    :return:
    """
    fp = webdriver.FirefoxProfile()
    fp.set_preference('network.proxy.type', 2)
    fp.set_preference("network.proxy.autoconfig_url", "http://pac.comon/scomproxy.pac")

    global browser
    browser = webdriver.Firefox(firefox_profile=fp,
                                executable_path=sc_stbt.get_generic_template_path() + "/../../../trunk/scripts/geckodriver")

    # maximize window
    browser.maximize_window()
    # open web page with a url
    browser.get("http://192.168.2.1/")
    browser.save_screenshot('screenshot_web.png')

    try:
        ui.WebDriverWait(browser, 20).until(EC.title_is("Gerbil v3.1"))
        browser.save_screenshot('screenshot_web.png')
        sc_stbt.debug("GERBIL IS FOUND")
    except:
        browser.save_screenshot('screenshot_web.png')
        browser.quit()
        assert False, "GERBIL IS NOT FOUND"


def check_state_basic_bandwidth():
    """
    check_state_basic_bandwidth: check if basic bandwidh is enable or disable
    :return:
    """
    inputElement = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/button')
    inputElement.click()
    browser.save_screenshot('screenshot_web.png')

    try:
        state = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[2]/a").text
        browser.save_screenshot('screenshot_web.png')

        if state == "Enable":
            sc_stbt.debug("Basic Bandwidth IS DISABLE")
            inputElement = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/button')
            inputElement.click()
            browser.save_screenshot('screenshot_web.png')
            return False

    except:
        state = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/ul/li[1]/a").text
        browser.save_screenshot('screenshot_web.png')

        if state == "Disable":
            sc_stbt.debug("Basic Bandwidth IS ENABLE")
            inputElement = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/button')
            inputElement.click()
            browser.save_screenshot('screenshot_web.png')
            return True


def enable_disable_basic_bandwidth():
    """
    enable_disable_basic_bandwidth:
    :return:
    """
    if not check_state_basic_bandwidth:
        sc_stbt.debug("ENABLE BASIC BANDWIDTH")
        inputElement = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/button')
        inputElement.click()
        browser.save_screenshot('screenshot_web.png')

        ui.WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/ul]'))).click()
        browser.save_screenshot('screenshot_web.png')

        sc_stbt.wait(2)
        if check_state_basic_bandwidth:
            sc_stbt.debug("BASIC BANDWIDTH IS ENABLE")

    else:
        sc_stbt.debug("DISABLE BASIC BANDWIDTH")
        inputElement = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/button')
        inputElement.click()
        browser.save_screenshot('screenshot_web.png')

        ui.WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/ul'))).click()
        browser.save_screenshot('screenshot_web.png')

        sc_stbt.wait(2)
        if not check_state_basic_bandwidth:
            sc_stbt.debug("BASIC BANDWIDTH IS DISABLE")


def goto_basic_bandwidth():
    """
    goto_basic_bandwidth: 1- goto basic bandwidth interface
                          2- enable basic bandwdth
    :return:
    """

    try:
        ui.WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/ul/ul/li[2]/a'))).click()
        browser.save_screenshot('screenshot_web.png')
    except:
        browser.save_screenshot('screenshot_web.png')
        sc_stbt.debug("Popup of browser not detected")

    inputElement = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/ul/li[2]/ul/li/a')
    inputElement.click()
    browser.save_screenshot('screenshot_web.png')

    try:
        ui.WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/h2")))
        browser.save_screenshot('screenshot_web.png')
        sc_stbt.debug("Basic Bandwidth IS FOUND")
    except:
        browser.save_screenshot('screenshot_web.png')
        browser.quit()
        assert False, "Basic Bandwidth IS NOT FOUND"


def set_basic_bandwidth(mbit="5mbit"):
    """
    set_basic_bandwidth:
    :param mbit:
    :return:
    """
    browser.save_screenshot('screenshot_web.png')
    state = ''
    start_time = time.time()
    while state != '100mbit' and time.time() - start_time < 10:
        try:
            state = browser.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/div[1]").text
        except:
            pass

    ui.WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[3]/div/form/div/ng-form/input")))
    inputElement = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[3]/div/form/div/ng-form/input')
    inputElement.send_keys(mbit)
    browser.save_screenshot('screenshot_web.png')

    inputElement = browser.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[3]/div/form/div/div/button')
    inputElement.click()
    browser.save_screenshot('screenshot_web.png')

def goto_gerbil_scripts():
    """
    goto_gerbil_scripts: go to gerbil_scripts interface

    :return:
    """
    try:
        ui.WebDriverWait(browser, 40).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/ul/ul/li[4]/a'))).click()
        browser.save_screenshot('screenshot_web.png')
    except:
        browser.save_screenshot('screenshot_web.png')
        sc_stbt.debug("Popup of browser not detected")

    inputElement = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/ul/li[4]/ul/li[1]/a')
    inputElement.click()
    browser.save_screenshot('screenshot_web.png')

    try:
        ui.WebDriverWait(browser, 40).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/h2")))
        browser.save_screenshot('screenshot_web.png')
        sc_stbt.debug("Gerbil Scripts ARE FOUND")
    except:
        browser.save_screenshot('screenshot_web.png')
        browser.quit()
        assert False, "Gerbil Scripts ARE NOT FOUND"

def run_script(gerbil_script_name="None"):
    """
    run_script: run script by clicking run button of the specified script

    :return:
    """
    script = script_name[gerbil_script_name]
    script_ID= ''.join(str(ID)for ID in script)
    ui.WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tr.ng-scope:nth-child(118) > td:nth-child(5) > button:nth-child(1)")))
    Element= browser.find_element_by_css_selector(
        'tr.ng-scope:nth-child('+ script_ID +') > td:nth-child(4) > button:nth-child(1)')
    Element.click()
    browser.save_screenshot('screenshot_web.png')

def state_script_check(gerbil_script_name="None"):
    """
    state_script_check : check if script is running or not
    :return:
    """
    script = script_name[gerbil_script_name]
    script_ID= ''.join(str(ID)for ID in script)
    ui.WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table[1]/tbody/tr['+ script_ID +']/td[3]/span')))
    state = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table[1]/tbody/tr['+ script_ID +']/td[3]/span').text
    if state == "Running" :
        sc_stbt.debug("Script " + gerbil_script_name + " is Running")
        return True
    else :
        sc_stbt.debug ("Script " + gerbil_script_name + " is NOT Running")
        return False

def stop_script(gerbil_script_name="None"):
    """
    stop_script : stop the script by clicking the stop button of the specified script
    :return:
    """
    script = script_name[gerbil_script_name]
    script_ID= ''.join(str(ID)for ID in script)
    ui.WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tr.ng-scope:nth-child(1) > td:nth-child(5) > button:nth-child(1)")))
    Element=browser.find_element_by_css_selector('tr.ng-scope:nth-child('+ script_ID +') > td:nth-child(4) > button:nth-child(2)')
    Element.click()
    browser.save_screenshot('screenshot_web.png')

def close_interface():
    """
    close_interface :: quit the web interface
    :return:
    """
    browser.quit()

def main():

    open_gerbil()
    goto_gerbil_scripts()
    run_script(gerbil_script_name="QA_HDR_3Mbit_to_1Mbit")
    stop_script(gerbil_script_name="QA_HDR_3Mbit_to_1Mbit")
    sc_stbt.wait(2)
    browser.quit()
    # run_script(gerbil_script_name="QA-sawtooth-up-500-kbps-steps-every-60sec")
    # state_script_check(gerbil_script_name="QA_HDR_3Mbit_to_1Mbit")
    # state_script_check(gerbil_script_name="QA-sawtooth-up-500-kbps-steps-every-60sec")
    # sc_stbt.wait(10)
    # stop_script(gerbil_script_name="QA-sawtooth-up-500-kbps-steps-every-60sec")
    # run_script(gerbil_script_name="QA_DASH_CVBR_H265_Bitrate_Floor_Surround_192")
    # state_script_check(gerbil_script_name="QA_DASH_CVBR_H265_Bitrate_Floor_Surround_192")

script_name={}

# list of scripts
script_name["QA-sawtooth-up-500-kbps-steps-every-60sec"] = [1]
script_name["QA_HDR_3Mbit_to_1Mbit"] = [2]
script_name["QA_DASH_CVBR_H265_Bitrate_Floor_Surround_192"] = [3]
script_name["QA_time_series_profile_limited_endurance_v2"] = [4]
script_name["QA_v2-slow-step-up-HD_Moonshot"] = [5]
script_name["QA_FHD_SmoothStreaming_CBR_Step_Up_bitrate_Rapid_Drop_Loop_Script_H264"] = [6]
script_name["QA-sawtooth-up-slow-loop-UHD"] = [7]
script_name["QA-bursts-of-latency"] = [8]
script_name["QA-random-HD-high-variability-1-every-5-seconds"] = [9]
script_name["QA_FHD_DASH_CVBR_15_High_85_low_script_H264"] = [10]
script_name["QA-Unstable-Medium-BW"] = [11]
script_name["QA-slow-step-up-Mobile"] = [12]
script_name["QA_Average_Bandwidth_and_disconnection_script"] = [13]
script_name["QA_Extreme_Low_Bandwidth_script"] = [14]
script_name["QA_Endurance_Step_Up"] = [15]
script_name["QA-step-up-step-down"] = [16]
script_name["QA-random-low-bw-variability-1-every-5-seconds"] = [17]
script_name["QA-sawtooth-up-slow-loop"] = [18]
script_name["QA_v2-sawtooth-down-slow-loop"] = [19]
script_name["QA-random-low-bw-variability-2-every-5-seconds"] = [20]
script_name["QA_time_series_profile_low_endurance_v2"] = [21]
script_name["QA-slow-step-up-HD"] = [22]
script_name["QA_time_series_profile_good_v2"] = [23]
script_name["QA-BigScreen-Surround-stable-low-bw-600kbps"]=[29]
script_name["QA_time_series_profile_step_up_down_endurance_v2"]=[35]
script_name["QA-slow-step-up-UHD-SS"]=[43]
script_name["QA-BigScreen-Stereo-stable-low-bw-400kbps"]=[45]
script_name["QA_time_series_profile_average_endurance_v2"]=[46]
script_name["QA_time_series_profile_average"]=[57]
script_name["QA_v2-slow-step-up-HD"]=[63]
script_name["QA_DASH_CVBR_H265_Step_Up_All_Bitrates"]=[115]
script_name["QA_v2-sawtooth-up-slow-loop"]=[118]
script_name["QA_time_series_profile_good"]=[129]



build_info_name={}
# list of catflap
build_info_name["oslocale"]= [100,87]
build_info_name["manufacturer"]=[100,103]
build_info_name["client bucket"]=[100,119]
build_info_name["model name"]=[100,135]
build_info_name["chipset"]=[100,169]
build_info_name["DTID"]=[100,320]
build_info_name["middleware version"]=[100,338]
build_info_name["Firmware"]=[100,353]
build_info_name["AVPK"]=[100,353]
build_info_name["ruby"]=[100,353]
build_info_name["oauthurl"]=[100,368]
build_info_name["blast url"]=[100,385]
build_info_name["init.js"]=[100,403]
build_info_name["atv endpoint"]=[100,419]


# streaming_details={}
# #List of Catflap
# streaming_details["Error Count"]=[]
# streaming_details["Buffer Count"]=[]
# streaming_details["Pause Count"]=[]
# streaming_details["FF Count"]=[]
# streaming_details["RW Count"]=[]
# streaming_details ["TryConnection Reported"]=[]
# streaming_details["DRMLicense Reported"]=[]
# streaming_details["TimedText Reported"]=[]
# streaming_details["StartStream Reported"]=[]
# streaming_details["StreamingSession Reported"]=[]
# streaming_details["StopStream Reported"]=[]
# streaming_details["AmountStreamed Reported"]=[]
# streaming_details["Asin's Streamed"]=[]
# streaming_details["Total Errors"]=[]
# streaming_details["Total Buffers"]=[]
# streaming_details["Recent Errors"]=[]
