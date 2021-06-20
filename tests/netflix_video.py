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

netflix_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/netflix"
netflix_path_template_from_project = "/../../../trunk/tests/templates/netflix/after_signin/"
path_mask_blackscreen = netflix_path_template + "/black/mask_black.png"
path_mask_motion = netflix_path_template + "/motion/mask_motion.png"
path_lateral_menu = netflix_path_template + "/lateral_menu/"
path_profile_ = netflix_path_template + "/profile_/"

threshold = stbt.get_config("netflix", "threshold", type_=float)
consecutive_frames = stbt.get_config("netflix", "consecutive_frames")
noise_threshold = stbt.get_config("netflix", "noise_threshold", type_=float)

key_pause = stbt.get_config("netflix", "key_pause")
key_forward = stbt.get_config("netflix", "key_forward")
key_back = stbt.get_config("netflix", "key_back")

pause_frame = eval(stbt.get_config("netflix", "pause_frame"))

polling_secs = stbt.get_config("netflix", "polling_secs", type_=int)
test_secs = stbt.get_config("netflix", "test_secs", type_=int)
interval_secs = stbt.get_config("netflix", "interval_secs", type_=int)
wait_pause_secs = stbt.get_config("netflix", "wait_pause_secs", type_=int)

occurence_forward = stbt.get_config("netflix", "occurence_forward", type_=int)
occurence_rewind = stbt.get_config("netflix", "occurence_rewind", type_=int)

match_parameters_is_menu = eval(stbt.get_config("netflix", "match_parameters_is_menu"))

match_parameters = eval(stbt.get_config("netflix", "match_parameters"))

region_current_timer = eval(stbt.get_config("netflix", "region_current_timer"))
region_end_timer = eval(stbt.get_config("netflix", "region_end_timer"))

language_menu = stbt.get_config("netflix", "language_menu")
language_profile = stbt.get_config("netflix", "language_profile")

position_main_profil = stbt.get_config("netflix", "position_main_profil", type_=int)
position_change_profil = stbt.get_config("netflix", "position_change_profil", type_=int)
keyboard = ['Enter', 'Entrez', 'Ingresa']
menu_signin = ['Watch', 'Profitez', 'Ve']
menu_profil = ['watching', 'regarde', 'quiere']
# tab_config = ['Search','Rechercher','Buscar']
menu_settings = ['Settings', 'Parametres', 'Configuracion']
tab_signout = ['Sign out', 'deconnecter', 'Cerrar']
tab_exit = ['Exit', 'Quitter', 'Salir']
menu_exit = ['Exiting', 'Sortie', 'Saliendo']

menu = sc_stbt.menu()
netflix = sc_stbt.video_tests(path_mask_motion=path_mask_motion,
                              path_mask_blackscreen=path_mask_blackscreen,
                              threshold=threshold,
                              consecutive_frames=consecutive_frames,
                              noise_threshold=noise_threshold,
                              key_pause=key_pause,
                              key_forward=key_forward,
                              pause_frame=pause_frame,
                              polling_secs=polling_secs,
                              test_secs=test_secs,
                              interval_secs=interval_secs,
                              wait_pause_secs=wait_pause_secs,
                              occurence_forward=occurence_forward,
                              occurence_rewind=occurence_rewind,
                              match_parameters=match_parameters,
                              region_current_timer=region_current_timer,
                              region_end_timer=region_end_timer)


################ unit function netflix#################################################"

def check_timer():
    if stbt.wait_until(lambda: sc_stbt.timer(region_current_timer, region_end_timer),
                       timeout_secs=12):
        sc_stbt.debug("TIMER DETECTED")
        return True
    else:
        sc_stbt.debug("TIMER NOT DETECTED")
        return False


def check_pause_netflix_timer():
    """
    check_pause_youtube_timer:
    :return:
    """
    if check_timer():
        return True
    else:
        assert False, ("PAUSE IS NOT DONE IN NETFLIX")


def check_pause_netflix_icon():
    """
    check_pause_netflix: when pause is done, check if the video is paused in netflix video
    :return:
    """
    try:
        menu.is_menu(press=['KEY_DOWN'],
                     path="/../../../trunk/tests/templates/netflix/icon_audio_subtitles/",
                     region_frame=stbt.Region(x=77, y=470, width=37, height=33),
                     timeout=3,
                     timeout_is_menu=7,
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method='none', match_threshold=0.8, confirm_threshold=0.3))
        sc_stbt.debug('NETFLIX IS PAUSED')
        return True
    except:
        assert False, ("NETFLIX IS NOT PAUSED")


def back_to_netflix_movie_menu():
    """
    back_to_netfli_movie_menu: back to netflix movie menu and check if it is displayed
    :return:
    """
    try:
        try:
            try:
                menu.is_menu(path="/../../../trunk/tests/templates/netflix/movie_menu/",
                     text="Menu netflix",
                     region_frame=stbt.Region(x=800, y=475, width=121, height=38),
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                           match_threshold=0.8, confirm_threshold=0.3),
                     timeout=3,
                     timeout_is_menu=0)
            except:
                menu.is_menu(press=['KEY_BACK'],
                             path="/../../../trunk/tests/templates/netflix/movie_menu/",
                             text="Menu netflix",
                             region_frame=stbt.Region(x=800, y=475, width=121, height=38),
                             match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                                   match_threshold=0.8, confirm_threshold=0.3),
                             timeout=2,
                             timeout_is_menu=6,
                             wait_after_press=3)
            sc_stbt.debug("MENU NETFLIX IS DISPLAYED")
            return True
        except:
            try:
                menu.is_menu(path="/../../../trunk/tests/templates/netflix/search/",
                         region_frame=stbt.Region(x=151, y=133, width=48, height=63),
                         timeout=2,
                         timeout_is_menu=6)
            except:
                menu.is_menu(press=["KEY_BACK"],
                                         path="/../../../trunk/tests/templates/netflix/search/",
                                         region_frame=stbt.Region(x=151, y=133, width=48, height=63),
                                         timeout=2,
                                         timeout_is_menu=6,
                                         wait_after_press=3)
            sc_stbt.press("KEY_DOWN")
            menu.is_menu(press=['KEY_OK'],
                     path="/../../../trunk/tests/templates/netflix/movie_menu/",
                     text="Menu netflix",
                     region_frame=stbt.Region(x=800, y=475, width=121, height=38),
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                           match_threshold=0.8, confirm_threshold=0.3),
                     timeout=2,
                     timeout_is_menu=20,
                     wait_after_press=3)
            return True
    except:
        sc_stbt.debug("MENU NETFLIX IS NOT DISPLAYED")
        return False


def is_netflix_settings():
    """
    press key ok until found menu settings in netflix
    :return: True when menu settings is displayed:  search word settings or get help in english ui
    """
    sc_stbt.wait(2)
    sc_stbt.press("KEY_OK")
    if stbts.match_any_text(text=['Get Help', 'Settings', 'configuracion'],
                            region=stbt.Region(x=46, y=42, width=186, height=64),
                            threshold = 0.8,
                            timeout_secs=10).match:
        return True
    else:
        return False


##################################### trick mode netflix ##################################################

def test_netflix_motion(polling_secs=polling_secs, test_secs=test_secs, interval_secs=interval_secs):
    """
    test_netflix_motion: detect motion from netflix video
    :return: true where motion is detected , False is not
    """
    sc_stbt.wait(10)
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    netflix.test_motion(polling_secs=polling_secs,
                        test_secs=test_secs,
                        interval_secs=interval_secs)


def test_netflix_pause(test_secs=test_secs,
                       polling_secs=polling_secs,
                       interval_secs=interval_secs,
                       wait_pause_secs=wait_pause_secs):
    """
    test_netflix_pause: check video is paused
    :return:    *if moition is not detected (video paused )==> play() (make video play ==> pause (make video
                pause)
                * elif motion is detected (video pause) ==> pause (make video pause)

                return false when:
                1) if video paused: when play() not done (motion not detected)
                2) if video paused ==>  play() done ==> when pause() not done (motion detected)
                3) if video played ==> when pause() not done (motion detected)
    """
    sc_stbt.wait(10)
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    netflix.pause(test_secs=test_secs,
                  polling_secs=polling_secs,
                  interval_secs=interval_secs,
                  key_pause=key_pause,
                  wait_pause_secs=wait_pause_secs)
    sc_stbt.debug("CHECK NETFLIX IS PAUSED")
    try:
        check_pause_netflix_timer()
    except:
        check_pause_netflix_icon()


def test_netflix_play(test_secs=test_secs,
                      polling_secs=polling_secs,
                      interval_secs=interval_secs):
    """
    test_netflix_play: check video is played
    :return: *if moition is detected (video played ) ==> pause() (make video pause)==> play (make video play)
                * elif motion is not detected (video paused) ==> play (make video play)

                return false when:
                1) if video played: when pause() not done (motion detected)
                2) if video played ==>  pause() done ==> when play() not done (motion not detected)
                3) if video paused ==> when play() not done (motion not detected)
    """
    sc_stbt.wait(10)
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    netflix.play(test_secs=test_secs,
                 polling_secs=polling_secs,
                 interval_secs=interval_secs,
                 key_pause=key_pause)
    sc_stbt.wait(10)


def test_netflix_fastforward(occurence_forward=occurence_forward,
                             key_forward=key_forward,
                             wait_pause_secs=wait_pause_secs):
    """
    test_netflix_fastforward: check motion is forwarded
    :return:
            * Make video play with test_youtube_play()
            * use trick_mode with press= forward of video class (see how to use video)
    """
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    netflix.fastforward(occurence_forward=occurence_forward,
                        key_forward=key_forward,
                        key_pause=key_pause,
                        wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY', 'KEY_PLAY'])
    sc_stbt.wait(10)


def test_netflix_rewind(occurence_rewind=occurence_rewind,
                        wait_pause_secs=wait_pause_secs):
    """
    test_netflix_fastforward: check motion is rewinded
    :return: * Make video play with test_youtube_play()
             * use trick_mode with press= rewind of video class (see how to use video)
    """
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    netflix.rewind(occurence_rewind=occurence_rewind,
                   key_pause=key_pause,
                   wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY', 'KEY_PLAY'])
    sc_stbt.wait(10)


def test_netflix_next_video():
    """
    test_netflix_next_video: go to next video and detect blackscreen
    :return:* Make video play with test_netflix_play()
                * use change_video with press = next_video of video class (see how to use video)

                return False when:
                1) blackscreen not detected
    """
    netflix.next_video()
    sc_stbt.wait(10)


def test_netflix_previous_video():
    """
    test_netflix_previous_video: go to previoust video and detect blackscreen
    :return: * Make video play with test_netflix_play()
                * use change_video with press = next_video of video class (see how to use video)

                retunr False when:
                1) blackscreen not detected
    """
    netflix.previous_video()
    sc_stbt.wait(10)


def is_netflix_movie_menu():
    """
    is_netflix_movie_menu: chec kif we are in netflix movie menu
    :return:
    """
    if menu.is_menu_template(perf=False,
                             path=netflix_path_template + "/movie_menu/",
                             region_frame=stbt.Region(x=770, y=460, width=180, height=67),
                             match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                   confirm_method="absdiff", match_threshold=0.8,
                                                                   confirm_threshold=0.3)):
        sc_stbt.debug("MENU NETFLIX IS FOUND")
        return True
    else:
        assert False, "Menu netflix movie is not found"


def forward_play_netflix(speed_trickmode_play=1, polling_secs=20, test_secs=20, forward_time=5):
    """
    forward_play_netflix: forward video and play a video
    :return:
    """
    sc_stbt.wait(1)
    sc_stbt.combo_press(combo=["KEY_FASTFORWARD"], number_press=speed_trickmode_play)
    sc_stbt.wait(forward_time)

    sc_stbt.press("KEY_PLAY")

    sc_stbt.wait(10)

    if check_timer():
        sc_stbt.debug("FORWARD IS DONE CORRECTLY")
    else:
        sc_stbt.debug("FORWARD IS NOT DONE CORRECTLY")


    netflix.test_motion(polling_secs=polling_secs,
                    test_secs=test_secs,
                    interval_secs=interval_secs)


def rewind_play_netflix(speed_trickmode_play=1, polling_secs=20, test_secs=20, rewind_time=5):
    """
    rewind_play_netflix: forward video and play a video
    :return:
    """
    sc_stbt.combo_press(combo=["KEY_REWIND"], number_press=speed_trickmode_play)
    sc_stbt.wait(rewind_time)
    sc_stbt.press("KEY_PLAY")
    sc_stbt.wait(10)
    if check_timer():
        sc_stbt.debug("FORWARD IS DONE CORRECTLY")
    else:
        sc_stbt.debug("FORWARD IS NOT DONE CORRECTLY")



    netflix.test_motion(polling_secs=polling_secs,
                    test_secs=test_secs,
                    interval_secs=interval_secs)


def active_subtitles_netflix():
    """

    :return:
    """
    sc_stbt.wait(5)
    sc_stbt.press("KEY_OK")
    sc_stbt.wait(2)
    sc_stbt.combo_press(combo=["KEY_UP"],number_press=1)
    menu.is_menu(press=['KEY_UP'],
                         path="/../../../trunk/tests/templates/netflix/subtitle/",
                         text="Menu subtitle",
                         region_frame=stbt.Region(x=112, y=46, width=47, height=36),
                         match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                               match_threshold=0.8, confirm_threshold=0.3),
                         timeout=2,
                         timeout_is_menu=15)

    menu.is_menu(press=['KEY_OK'],
                         path="/../../../trunk/tests/templates/netflix/subtitle/",
                         text="Subtitles",
                         region_text=stbt.Region(x=588, y=49, width=168, height=43),
                         match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                               match_threshold=0.8, confirm_threshold=0.3),
                         timeout=2,
                         timeout_is_menu=15,
                         wait_after_press=1)

    region_cursor = stbt.match(netflix_path_template+"/active_subtitle/active_subtitle.png").position

    region_cursor_x = region_cursor.x
    region_cursor_y = region_cursor.y
    sc_stbt.wait(1)

    if menu.is_menu_ocr(perf=False,
                        text="Off",
                        region_text=stbt.Region(x=region_cursor_x+38, y=region_cursor_y+9, width=43, height=19),
                        timeout=3):
        sc_stbt.debug("SUBTITLE NOT ACTIVATED")
        if region_cursor_y in [82,92]:
            sc_stbt.press("KEY_DOWN")
            sc_stbt.wait(1)
            sc_stbt.press("KEY_OK")
        else:
            sc_stbt.press("KEY_UP")
            sc_stbt.wait(1)
            sc_stbt.press("KEY_OK")

    else:
        sc_stbt.debug("SUBTITLE IS ACTIVATED")
    sc_stbt.wait(3)
    sc_stbt.press("KEY_OK")

##########################################API check menu and profile#######################################################


def check_keyboard(text, region_text):
    """
    check_keyboard: check keyboard in menu signin
    :param text:
    :param region_text:
    :return:
    """
    menu.is_menu(text=text,
                 region_text=region_text,
                 path="/../../../trunk/tests/templates/netflix/keyboard/",
                 mode=stbt.OcrMode.SINGLE_WORD,
                 match_parameters=match_parameters_is_menu,
                 timeout=3,
                 timeout_is_menu=0)
    sc_stbt.debug("KEYBOARD DISPLAYED")


def check_menu_signin(text, region_text):
    """
    check_menu_signin: check if we are in menu signin of netflix
    :param text:
    :param region_text:
    :return:
    """
    if stbts.match_text(text=text,
                        region=region_text,
                        timeout_secs=3).match:
        sc_stbt.debug("NETFLIX MENU SINGIN DISPLAYED")
        return True
    else:
        return False


def goto_config_menu():
    """
    goto_config_menu: press key back until display lateral menu
    :return:
    """
    try:
        menu.is_menu(press=["KEY_BACK"],
                     path="/../../../trunk/tests/templates/netflix/home_menu/",
                     region_frame=stbt.Region(x=158, y=148, width=49, height=93),
                     timeout=3,
                     timeout_is_menu=20,
                     wait_after_press=2,
                     match_parameters=match_parameters_is_menu)
    except:

        menu.is_menu(press=["KEY_BACK"],
                      path="/../../../trunk/tests/templates/netflix/home_menu/",
                      region_frame=stbt.Region(x=52, y=180, width=37, height=66),
                      timeout=3,
                      timeout_is_menu=20,
                      wait_after_press=2,
                      match_parameters=match_parameters_is_menu)

def goto_settings_menu():
    """
    goto_settings_menu: goto settings menu
    :return:
    """
    goto_config_menu()
    menu.is_menu(press=["KEY_DOWN"],
                 path="/../../../trunk/tests/templates/netflix/lateral_menu/",
                 region_frame=stbt.Region(x=3, y=444, width=164, height=163),
                 text="Settings",
                 timeout=3,
                 timeout_is_menu=40,
                 match_parameters=stbt.MatchParameters(confirm_method="normed-absdiff",
                                                       match_threshold=0.8,
                                                       confirm_threshold=0.3))
    if stbt.wait_until(lambda: is_netflix_settings()):
        sc_stbt.debug("MENU Settings IS FOUND")
    else:
        assert False, "MENU Settings IS NOT FOUND"




def select_profile(position_pro):
    """
    select_profile: select a specific profile
    :return:
    """
    sc_stbt.combo_press(combo=["KEY_LEFT"], number_press=5)
    if position_pro == 0:
        pass
    elif position_pro == 1:
        change_profil(region=stbt.Region(x=290, y=173, width=24, height=10))
    elif position_pro == 2:
        change_profil(region=stbt.Region(x=450, y=173, width=24, height=10))
    elif position_pro == 3:
        change_profil(region=stbt.Region(x=632, y=173, width=24, height=10))
    elif position_pro == 4:
        change_profil(region=stbt.Region(x=730, y=173, width=24, height=10))
    else:
        assert False, "POSITION PROFIL NOT EXIST"


def change_profil(region):
    """
    change_profil: press key right until found a profile
    :return:
    """
    menu.is_menu(press=["KEY_RIGHT"],
                 path="/../../../trunk/tests/templates/netflix/profile/",
                 region_frame=region,
                 text="PROFILE",
                 timeout=3,
                 timeout_is_menu=20,
                 wait_after_press=2)
    sc_stbt.press("KEY_OK")
    is_netflix_movie_menu()


def test_switch_profile_netflix():
    """
    test_switch_profile_netflix:
    :return:
    """
    sc_stbt.wait(5)
    # check if we are under profile menu
    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        select_profile(position_change_profil)
        return True
    # back to movie netflix menu
    if back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    # goto config menu in netflix
    goto_config_menu()
    # goto profile menu settings menu
    sc_stbt.combo_press(combo=["KEY_UP"], number_press=5)
    stbts.press_until_match_any_text(press_key="KEY_OK",
                                     text=['watching', 'regarde', 'quiere'],
                                     region=stbt.Region(x=356, y=41, width=278, height=74),
                                     timeout_secs=3,
                                     timeout=20)
    select_profile(position_change_profil)


##################################################################################################################

def open_video_netflix(movie_name=None):
    """
    open_video_netflix: open any video from netflix and check motion
    :return: True when video selected and motion detected, false is not
    """
    sc_stbt.wait(15)
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    play_mode = stbt.get_config("netflix", "play_mode")

    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(10)
    if movie_name is  None:
        movie_name = stbt.get_config("netflix", "movie_name")
    if movie_name == '':
        p_combo_down = ['KEY_DOWN', 'KEY_RIGHT', "KEY_OK"]
        sc_stbt.combo_press(p_combo_down, delay_sec=2)
        if menu.is_menu_template(perf=False,
                                path=netflix_path_template + "/catalogue_movie_selected/",
                                region_frame=stbt.Region(x=64, y=299, width=892, height=143),
                                timeout=3):
            sc_stbt.combo_press(["KEY_RIGHT", "KEY_DOWN"], delay_sec=2)
        sc_stbt.wait(2)
        if play_mode == "resume":
            sc_stbt.press('KEY_OK')
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

    else:
        sc_stbt.search_netflix(movie_name)
    try:
        test_netflix_motion()
        sc_stbt.debug("NETFLIX VIDEO IS OPENED")
        return True
    except:
        assert False, 'NETFLIX VIDEO IS NOT OPENED'


def sign_in_netflix():
    """
    sign_in_netflix: sign_in_netflix in netflix
    (see hwo to use netflix ../trunk/docs/netflix)
    :return:True when sign_in done
    """
    sc_stbt.write_statut_test(statut="test_ko")
    login = stbt.get_config("netflix", "login", type_=str)
    password = stbt.get_config("netflix", "password", type_=str)

    # search menu signin netflix and keyboard
    if language_menu == 'eng':
        try:
            check_keyboard(text=keyboard[0],
                           region_text=stbt.Region(x=74, y=140, width=42, height=19))
        except:
            if check_menu_signin(text=menu_signin[0],
                                 region_text=stbt.Region(x=62, y=152, width=145, height=84)):
                 p_combo = ["KEY_UP", "KEY_UP","KEY_UP"]
                 sc_stbt.combo_press(p_combo)
                 menu.is_menu(press = ["KEY_DOWN"],
                     text = " SIGN IN FOUND ",
                     path="/../../../trunk/tests/templates/netflix/sign_in/",
                     region_frame=stbt.Region(x=60, y=415, width=42, height=34),
                     timeout=3,
                     timeout_is_menu=6,
                     match_parameters =  stbt.MatchParameters(match_method='sqdiff-normed',
                                                              confirm_method='none',
                                                              match_threshold=0.8,
                                                              confirm_threshold=0.3))
                 sc_stbt.press("KEY_OK")
            else:
                assert False, ("MENU SIGNIN NETFLIX NOT DISPLAYED")

    elif language_menu == 'fra':
        try:
            check_keyboard(text=keyboard[1],
                           region_text=stbt.Region(x=74, y=140, width=42, height=19))
        except:
            if check_menu_signin(text=menu_signin[1],
                                 region_text=stbt.Region(x=62, y=152, width=145, height=84)):
                 p_combo = ["KEY_UP", "KEY_UP","KEY_UP"]
                 sc_stbt.combo_press(p_combo)
                 menu.is_menu(press = ["KEY_DOWN"],
                     text = " SIGN IN FOUND ",
                     path="/../../../trunk/tests/templates/netflix/sign_in/",
                     region_frame=stbt.Region(x=60, y=424, width=42, height=20),
                     timeout=3,
                     timeout_is_menu=6,
                     match_parameters =  stbt.MatchParameters(match_method='sqdiff-normed',
                                                              confirm_method='none',
                                                              match_threshold=0.8,
                                                              confirm_threshold=0.3))
                 sc_stbt.press("KEY_OK")
            else:
                assert False, ("MENU SIGNIN NETFLIX NOT DISPLAYED")


    elif language_menu == 'spa':
        try:
            check_keyboard(text=keyboard[2],
                           region_text=stbt.Region(x=74, y=140, width=42, height=19))
        except:
            if check_menu_signin(text=menu_signin[2],
                                 region_text=stbt.Region(x=70, y=180, width=123, height=51)):
                 p_combo = ["KEY_UP", "KEY_UP","KEY_UP"]
                 sc_stbt.combo_press(p_combo)
                 menu.is_menu(press = ["KEY_DOWN"],
                     text = " SIGN IN FOUND ",
                     path="/../../../trunk/tests/templates/netflix/sign_in/",
                     region_frame=stbt.Region(x=60, y=424, width=42, height=20),
                     timeout=3,
                     timeout_is_menu=6,
                     match_parameters =  stbt.MatchParameters(match_method='sqdiff-normed',
                                                              confirm_method='none',
                                                              match_threshold=0.8,
                                                              confirm_threshold=0.3))
                 sc_stbt.press("KEY_OK")
            else:
                assert False, ("MENU SIGNIN NETFLIX NOT DISPLAYED")


    delete_login_password()

    if stbt.wait_until(lambda: sc_stbt.get_text(region=stbt.Region(x=259, y=480, width=19, height=19),
                                                mode=stbt.OcrMode.SINGLE_WORD,
                                                text_color=(248, 249, 249)) != "",
                                                timeout_secs=3) or stbt.wait_until(lambda: menu.is_menu_template(perf=False,
                                                                                    path=netflix_path_template + "/remember_email/enable",
                                                                                    timeout=5,
                                                                                    match_parameters=match_parameters_is_menu),
                                                                                    timeout_secs=5):

        sc_stbt.repeat(lambda: sc_stbt.press("KEY_DOWN"), occurence=7)
        p_combo = ["KEY_RIGHT", "KEY_OK"]
        sc_stbt.combo_press(p_combo)
        sc_stbt.repeat(lambda: sc_stbt.press("KEY_UP"), occurence=4)

        if stbt.wait_until(lambda: sc_stbt.get_text(region=stbt.Region(x=259, y=480, width=19, height=19),
                                                    mode=stbt.OcrMode.SINGLE_WORD,
                                                    text_color=(248, 249, 249)) == "",
                                                    timeout_secs=5) or stbt.wait_until(lambda: menu.is_menu_template(perf=False,
                                                                                        path=netflix_path_template + "/remember_email/disable",
                                                                                        match_parameters=match_parameters_is_menu),
                                                                                        timeout_secs=5):
            sc_stbt.debug("REMEMBER MAIL DISABLED")
        else:
            return False, 'REMEMBER MAIL NOT DISABLE'


    sc_stbt.netflix_enter_account().enter_text(login)
    sc_stbt.wait(5)
    sc_stbt.netflix_enter_password().enter_text(password)

    if stbt.wait_until(lambda: menu.is_menu_template(perf=False,
                                                     path=netflix_path_template + "/after_signin/",
                                                     region_frame=stbt.Region(x=792, y=35, width=133, height=482),
                                                     timeout=5,
                                                     match_parameters =  stbt.MatchParameters(match_method='sqdiff-normed',
                                                              confirm_method='none',
                                                              match_threshold=0.8,
                                                              confirm_threshold=0.3)),
                                                     timeout_secs=30):
        sc_stbt.write_statut_test(statut="test_ok")
        sc_stbt.debug("SIGN IN DONE")
        sc_stbt.wait(5)
    elif stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
        region=stbt.Region(x=356, y=41, width=278, height=74)).match:

        menu.is_menu(press = ["KEY_OK"],
                     text = " SIGN IN DONE ",
                     path ="/../../../trunk/tests/templates/netflix/after_signin/",
                     region_frame=stbt.Region(x=792, y=35, width=133, height=482),
                     timeout=3,
                     timeout_is_menu=6,
                     match_parameters =  stbt.MatchParameters(match_method='sqdiff-normed',
                                                              confirm_method='none',
                                                              match_threshold=0.8,
                                                              confirm_threshold=0.3))
        sc_stbt.write_statut_test(statut="test_ok")
    else:
        assert False, 'SIGN IN NOT DONE'



def sign_out_netflix():
    """
    sign_out_netflix: sign_out from netflix
    :return: True when sign_out done and netflix deconnect
    """
    sc_stbt.wait(5)

    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)

    # back to movie netflix menu
    if back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    # goto get help menu in netflix
    goto_settings_menu()

    if language_profile == 'eng':
        # if stbt.wait_until(lambda: is_netflix_settings()):
        #     sc_stbt.debug("NETFLIX SETTING MENU FOUND")
        # else:
        #     assert False, "NETFLIX SETTINGS MENU NOT FOUND"
        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_signout[0]],
                                         region=stbt.Region(x=367, y=91, width=126, height=42),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)
    elif language_profile == 'fra':
        stbts.press_until_match_any_text(press_key='KEY_OK',
                                         text=[menu_settings[1]],
                                         region=stbt.Region(x=46, y=42, width=186, height=64),
                                         timeout_secs=3,
                                         timeout=20)
        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_signout[1]],
                                         region=stbt.Region(x=367, y=91, width=126, height=42),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)
    elif language_profile == 'spa':
        stbts.press_until_match_any_text(press_key='KEY_OK',
                                         text=[menu_settings[2]],
                                         region=stbt.Region(x=46, y=42, width=186, height=64),
                                         timeout_secs=3,
                                         timeout=30)
        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_signout[2]],
                                         region=stbt.Region(x=367, y=91, width=126, height=42),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)

    p_combo_ok = ["KEY_OK", 'KEY_OK', 'KEY_OK']
    sc_stbt.combo_press(p_combo_ok)
    sc_stbt.wait(30)
    if stbts.match_any_text (text=[menu_signin[0], menu_signin[1],menu_signin[2]],
                                 region=stbt.Region(x=62, y=152, width=145, height=84)).match:

        sc_stbt.debug("SINGN OUT DONE")
        return True
    else:
        sc_stbt.debug("SIGN OUT NOT DONE")
        assert False, 'SIGN OUT NOT DONE'


def test_is_netflix(press_key=None , wait = 5):
    """
    check if netflix menu displayed for 4 menu:
    - signin menu
    - keybord menu
    - profile menu
    - netflix postees menu
    :return: True when netflix menu is dsplayed, False is not
    """
    if press_key is not None:
        sc_stbt.press(press_key)
    sc_stbt.wait(wait)

    # search menu signin netflix and keyboard ##Use cas 1
    if language_menu == 'eng':
        # search menu keyboard
        try:
            check_keyboard(text=keyboard[0],
                           region_text=stbt.Region(x=74, y=140, width=42, height=19))
            return True
        # search menu signin netflix
        except:
            if check_menu_signin(text=menu_signin[0],
                                 region_text=stbt.Region(x=18, y=88, width=259, height=188)):
                return True
            # search menu netflix movie
            # disable config netflix menu
            elif menu.is_menu_template(perf=False,
                                       path=netflix_path_template + "/menu_config_netflix/",
                                       match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                             confirm_method="absdiff",
                                                                             match_threshold=0.8,
                                                                             confirm_threshold=0.3),
                                       timeout=10):
                sc_stbt.press("KEY_BACK")

                if menu.is_menu_template(perf=False,
                                         path=netflix_path_template + "/movie_menu/",
                                         match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                               confirm_method="absdiff",
                                                                               match_threshold=0.8,
                                                                               confirm_threshold=0.3),
                                         timeout=10):

                    sc_stbt.debug("SINGIN MENU DISPLAYED: NETFLIX OPEN")
                    return True
                else:
                    sc_stbt.debug("MENU SIGNIN NETFLIX NOT DISPLAYED")
            # check if menu netflix movie is displayed
            elif menu.is_menu_template(perf=False,
                                       path=netflix_path_template + "/movie_menu/",
                                       match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                             confirm_method="absdiff",
                                                                             match_threshold=0.8,
                                                                             confirm_threshold=0.3),
                                       timeout=10):

                sc_stbt.debug("SINGIN MENU DISPLAYED: NETFLIX OPEN")
                return True
            else:
                sc_stbt.debug("MENU SIGNIN NETFLIX NOT DISPLAYED")

    elif language_menu == 'fra':
        # search menu keyboard
        try:
            check_keyboard(text=keyboard[1],
                           region_text=stbt.Region(x=74, y=140, width=52, height=19))
            return True
        # search menu signin netflix
        except:
            if check_menu_signin(text=menu_signin[1],
                                 region_text=stbt.Region(x=18, y=88, width=259, height=188)):
                return True
            elif menu.is_menu_template(perf=False,
                                       path=netflix_path_template + "/menu",
                                       match_parameters=stbt.MatchParameters(confirm_method="none",
                                                                             match_threshold=0.88,
                                                                             confirm_threshold=0.2)):
                sc_stbt.debug("SINGIN MENU DISPLAYED: NETFLIX OPEN")
                return True
            else:
                sc_stbt.debug("MENU SIGNIN NETFLIX NOT DISPLAYED")

    elif language_menu == 'spa':
        # search menu keyboard
        try:
            check_keyboard(text=keyboard[2],
                           region_text=stbt.Region(x=74, y=140, width=57, height=19))
            return True
        # search menu signin netflix
        except:
            if check_menu_signin(text=menu_signin[2],
                                 region_text=stbt.Region(x=18, y=88, width=259, height=188)):
                return True
            elif menu.is_menu_template(perf=False,
                                       path=netflix_path_template + "/menu",
                                       match_parameters=stbt.MatchParameters(confirm_method="none",
                                                                             match_threshold=0.88,
                                                                             confirm_threshold=0.2)):
                sc_stbt.debug("SINGIN MENU DISPLAYED: NETFLIX OPEN")
                return True
            else:
                sc_stbt.debug("MENU SIGNIN NETFLIX NOT DISPLAYED")

    #check video playing (for android)
    if stbts.match_any_text(text=["watching",'Are', "still"],
                            region=stbt.Region(x=196, y=176, width=562, height=71)).match:
        sc_stbt.press("KEY_OK")
        return True

    # shearching menu profile ##Use cas 2
    if stbts.match_any_text(text=menu_profil,
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        select_profile(position_main_profil)
        sc_stbt.debug("MENU NETFLIX DISPLAYED: NETFLIX OPEN")
        return True
    else:
        sc_stbt.debug("MENU PROFIL NOT DISPLAYED")

    # press key_back until check netflix movie menu
    if back_to_netflix_movie_menu():
        return True
    else:
        sc_stbt.debug("MENU NETFLIX NOT DISPLAYED")
        assert False, 'NETFLIX NOT DISPLAYED'


def test_exit_netflix():
    """
    test_exit_netflix: exit from netflix
    :return: True when exit netflix done
    """
    sc_stbt.get_statut_test("NETFLIX MENU WAS NOT OPENED")
    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)
    # back to movie netflix menu
    if back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    # goto get help menu in netflix
    goto_settings_menu()

    if language_profile == 'eng':
        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_exit[0]],
                                         region=stbt.Region(x=368, y=73, width=103, height=25),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)
        try:
            stbts.press_until_match_any_text(press_key='KEY_OK',
                                             text=[menu_exit[0]],
                                             region=stbt.Region(x=428, y=219, width=82, height=34),
                                             timeout_secs=3,
                                             timeout=30)
            sc_stbt.debug("EXIT NETFLIX DONE")
            return True
        except:
            sc_stbt.debug("EXIT NETFLIX NOT DONE")
            assert False, 'EXIT NETFLIX NOT DONE'
    elif language_profile == 'fra':
        stbts.press_until_match_any_text(press_key='KEY_OK',
                                         text=[menu_settings[1]],
                                         region=stbt.Region(x=46, y=42, width=186, height=64),
                                         timeout_secs=3,
                                         timeout=20)
        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_exit[1]],
                                         region=stbt.Region(x=368, y=73, width=103, height=25),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)
        try:
            stbts.press_until_match_any_text(press_key='KEY_OK',
                                             text=[menu_exit[1]],
                                             region=stbt.Region(x=428, y=219, width=82, height=34),
                                             timeout_secs=3,
                                             timeout=30)
            sc_stbt.debug("EXIT NETFLIX DONE")
            return True
        except:
            sc_stbt.debug("EXIT NETFLIX NOT DONE")
            assert False, 'EXIT NETFLIX NOT DONE'
    elif language_profile == 'spa':

        stbts.press_until_match_any_text(press_key='KEY_DOWN',
                                         text=[tab_exit[2]],
                                         region=stbt.Region(x=368, y=73, width=103, height=25),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=100)
        try:
            stbts.press_until_match_any_text(press_key='KEY_OK',
                                             text=[menu_exit[2]],
                                             region=stbt.Region(x=428, y=219, width=82, height=34),
                                             timeout_secs=3,
                                             threshold=0.8,
                                             timeout=30)
            sc_stbt.debug("EXIT NETFLIX DONE")
            return True
        except:
            assert False, 'EXIT NETFLIX NOT DONE'



def test_close_netflix():
    """
    test_close_netflix: suspend  netflix
    :return: True when suspend netflix is done
    """
    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)
    # back to movie netflix menu
    if back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    # goto get help menu in netflix
    goto_config_menu()
    menu.is_menu(press=["KEY_DOWN"],
                 path="/../../../trunk/tests/templates/netflix/suspend_netflix/",
                 region_frame=stbt.Region(x=13, y=484, width=80, height=33),
                 text="Exit netflix",
                 timeout=3,
                 timeout_is_menu=40,
                 match_parameters=stbt.MatchParameters(confirm_method="none",
                                                       match_threshold=0.9,
                                                       confirm_threshold=0.3))
    sc_stbt.press("KEY_OK")
    sc_stbt.wait(3)
    if menu.is_menu_template(perf=False,
                 path=netflix_path_template+"/suspend_netflix/",
                 region_frame=stbt.Region(x=13, y=484, width=80, height=33),
                 timeout=5,
                 match_parameters=stbt.MatchParameters(confirm_method="none",
                                                       match_threshold=0.9,
                                                       confirm_threshold=0.3)):
        assert False, "NETFLIX IS NOT SUSPENDED"
    else:
        sc_stbt.debug("NETFLIX IS SUSPENDED")



def test_exit_netflix_by_button_home():
    """
    test_close_netflix: suspend  netflix
    :return: True when suspend netflix is done
    """
    android = eval(stbt.get_config("adb", "adb_press"))
    if android:
        press_home = "KEY_HOME"
    else:
        press_home = "KEY_MENU"

    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)
    # back to movie netflix menu

    if back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        assert False, ("NETFLIX MOVIE MENU NOT FOUND")

    sc_stbt.combo_press(combo=[press_home], number_press=2)
    sc_stbt.wait(3)

    exit=False
    try:
        menu.is_menu(path="/../../../trunk/tests/templates/netflix/movie_menu/",
                     text="Menu netflix",
                     region_frame=stbt.Region(x=800, y=475, width=121, height=38),
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed', confirm_method="absdiff",
                                                           match_threshold=0.8, confirm_threshold=0.3),
                     timeout=5,
                     timeout_is_menu=0)
    except:
        exit=True
    if exit:
        sc_stbt.debug("HOME IS FOUND AND NETFLIX IS EXITED")
    else:
        assert False, ("HOME IS NOT FOUND AND NETFLIX IS NOT EXITED")


##################" test navigation and API of navigation ##########################################################


def test_navigation_netflix(navigation_play_video=None, navigation_time_out=None):
    """
    test_navigation_netflix: navigate in netflix
    :param press:
    :return:
    """
    if navigation_play_video is None:
        navigation_play_video = eval(stbt.get_config("netflix", "navigation_play_video"))
    if navigation_time_out is None:
        navigation_time_out = eval(stbt.get_config("netflix", "navigation_time_out"))
    try:
        if back_to_netflix_movie_menu():
            sc_stbt.repeat(lambda: navigation_netflix(navigation_play_video),
                       time_out=navigation_time_out)
        else:
            assert False, "YOUTUBE MENU IS NOT DISPLAYED"
    except:
        if back_to_netflix_movie_menu():
            pass
        else:
            assert False, "Problem in test navigation:"


def navigation_netflix(navigation_play_video):
    """
    navigation_netflix: navigation in menu netflix
    :return:
    """
    sc_stbt.crop(stbt.get_frame(),
                 region=stbt.Region(x=65, y=314, width=887, height=215),
                 file_name="frame")
    sc_stbt.combo_press(combo=["KEY_RIGHT"], number_press=10, delay_sec=0.5)
    sc_stbt.combo_press(combo=["KEY_LEFT"], number_press=8, delay_sec=0.5)
    sc_stbt.combo_press(combo=["KEY_DOWN"], number_press=10, delay_sec=0.5)
    if menu.is_menu_template(perf=False,
                        path=netflix_path_template + "/catalogue_movie_selected/",
                        region_frame=stbt.Region(x=64, y=299, width=892, height=143),
                        timeout=3):
        sc_stbt.press("KEY_DOWN")
    if stbt.match(image="frame.png").match:
        assert False, "NAVIGATION NETFLIX IS NOT DONE"


    else:
        sc_stbt.combo_press(combo=["KEY_UP"], number_press=10, delay_sec=0.5)
        if menu.is_menu_template(perf=False,
                                 text=netflix_path_template + "/catalogue_movie_selected/",
                                 region_frame=stbt.Region(x=64, y=299, width=892, height=143),
                                 timeout=3):
            sc_stbt.press("KEY_UP")
        if navigation_play_video:
            sc_stbt.press("KEY_OK")
            netflix.open(path_mask_blackscreen=path_mask_blackscreen)
            test_netflix_motion(polling_secs=20,
                                test_secs=8,
                                interval_secs=5)
            if back_to_netflix_movie_menu():
                pass
            else:
                assert False, "NAVIGATION NETFLIX IS NOT DONE"

    sc_stbt.debug("NAVIGATION NETFLIX IS DONE")


#################################"API sign in netflix ###########################################################

def delete_login_password():
    """
    delete_login_password
    :return:
    """
    if language_menu == 'eng':
        try:
            menu.is_menu(text='Email',
                         region_text=stbt.Region(x=492, y=170, width=55, height=23),
                         path="/../../../trunk/tests/templates/netflix/delete_login/",
                         region_frame=stbt.Region(x=486, y=167, width=210, height=31),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            return True
        except:
            pass
        try:
            menu.is_menu(text='Password',
                         region_text=stbt.Region(x=494, y=208, width=67, height=16),
                         path="/../../../trunk/tests/templates/netflix/delete_login_password/",
                         region_frame=stbt.Region(x=482, y=199, width=210, height=33),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            delete_login()
        except:
            delete_password()
            delete_login()

    elif language_menu == 'fra':
        try:
            menu.is_menu(text='Adresse',
                         region_text=stbt.Region(x=490, y=170, width=78, height=23),
                         path="/../../../trunk/tests/templates/netflix/delete_login/",
                         region_frame=stbt.Region(x=486, y=167, width=210, height=31),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            return True
        except:
            pass
        try:
            menu.is_menu(text='Mot',
                         region_text=stbt.Region(x=489, y=206, width=32, height=19),
                         path="/../../../trunk/tests/templates/netflix/delete_login_password/",
                         region_frame=stbt.Region(x=482, y=199, width=210, height=33),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            delete_login()
        except:
            delete_password()
            delete_login()

    elif language_menu == 'spa':
        try:
            menu.is_menu(text='Email',
                         region_text=stbt.Region(x=487, y=170, width=152, height=23),
                         path="/../../../trunk/tests/templates/netflix/delete_login/",
                         region_frame=stbt.Region(x=486, y=167, width=210, height=31),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            return True
        except:
            pass
        try:
            menu.is_menu(text='Contrasena',
                         region_text=stbt.Region(x=489, y=206, width=32, height=19),
                         path="/../../../trunk/tests/templates/netflix/delete_login_password/",
                         region_frame=stbt.Region(x=482, y=199, width=367, height=38),
                         match_parameters=match_parameters_is_menu,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout=3,
                         timeout_is_menu=6)
            delete_login()
        except:
            delete_password()
            delete_login()


def delete_login():
    sc_stbt.wait(2)
    goto_cord(")")
    if language_menu == 'eng':
        menu.is_menu(press=['KEY_OK'],
                     path="/../../../trunk/tests/templates/netflix/delete_login/",
                     text="Email",
                     region_text=stbt.Region(x=492, y=170, width=55, height=23),
                     timeout=3,
                     mode=stbt.OcrMode.SINGLE_WORD,
                     timeout_is_menu=300,
                     match_parameters=match_parameters_is_menu)
    elif language_menu == 'fra':
        menu.is_menu(press=['KEY_OK'],
                     text='Adresse',
                     region_text=stbt.Region(x=490, y=170, width=78, height=23),
                     path="/../../../trunk/tests/templates/netflix/delete_login/",
                     region_frame=stbt.Region(x=486, y=167, width=210, height=31),
                     match_parameters=match_parameters_is_menu,
                     mode=stbt.OcrMode.SINGLE_WORD,
                     timeout=3,
                     timeout_is_menu=300)
    elif language_menu == 'spa':
        menu.is_menu(text='Direccion',
                     region_text=stbt.Region(x=487, y=170, width=152, height=23),
                     path="/../../../trunk/tests/templates/netflix/delete_login/",
                     region_frame=stbt.Region(x=486, y=167, width=210, height=31),
                     match_parameters=match_parameters_is_menu,
                     mode=stbt.OcrMode.SINGLE_WORD,
                     timeout=3,
                     timeout_is_menu=300)
    return True


def delete_password():
    sc_stbt.wait(2)
    if language_menu == 'eng':
        try:
            menu.is_menu(path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Password",
                         region_text=stbt.Region(x=493, y=205, width=91, height=23),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=6,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True
        except:
            sc_stbt.debug("cordoneeee")
            goto_cord("&")
            menu.is_menu(press=['KEY_OK'],
                         path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Password",
                         region_text=stbt.Region(x=493, y=205, width=91, height=23),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=300,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True
    elif language_menu == 'fra':
        try:
            menu.is_menu(path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Mot",
                         region_text=stbt.Region(x=493, y=370, width=120, height=30),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=6,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True
        except:
            sc_stbt.debug("cordoneeee")
            goto_cord("&")
            menu.is_menu(press=['KEY_OK'],
                         path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Mot",
                         region_text=stbt.Region(x=493, y=370, width=120, height=30),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=300,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True
    elif language_menu == 'spa':
        try:
            menu.is_menu(path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Contrasena",
                         region_text=stbt.Region(x=493, y=370, width=120, height=30),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=6,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True
        except:
            sc_stbt.debug("cordoneeee")
            goto_cord("&")
            menu.is_menu(press=['KEY_OK'],
                         path="/../../../trunk/tests/templates/netflix/delete_password/",
                         text="Contrasena",
                         region_text=stbt.Region(x=493, y=370, width=120, height=30),
                         timeout=3,
                         mode=stbt.OcrMode.SINGLE_WORD,
                         timeout_is_menu=300,
                         match_parameters=match_parameters_is_menu)
            goto_previous_step(y_previous_step=363)
            return True


#######################
# unit functions of sign_in_netflix for qwerty keyboard
matrix_netflix = {}

# Debut de ligne qwertyuiop
matrix_netflix["q"] = [72, 204]
matrix_netflix["w"] = [109, 203]
matrix_netflix["e"] = [145, 203]
matrix_netflix["r"] = [181, 203]
matrix_netflix["t"] = [217, 203]
matrix_netflix["y"] = [253, 203]
matrix_netflix["u"] = [289, 203]
matrix_netflix["i"] = [325, 203]
matrix_netflix["o"] = [361, 203]
matrix_netflix["p"] = [397, 203]

##debut de ligne asdfghjkl-
matrix_netflix["a"] = [72, 239]
matrix_netflix["s"] = [109, 239]
matrix_netflix["d"] = [145, 239]
matrix_netflix["f"] = [181, 239]
matrix_netflix["g"] = [217, 239]
matrix_netflix["h"] = [253, 239]
matrix_netflix["j"] = [289, 239]
matrix_netflix["k"] = [325, 239]
matrix_netflix["l"] = [361, 239]
matrix_netflix["-"] = [397, 239]

# debut de ligne  zxcvbnm_
matrix_netflix["z"] = [145, 275]
matrix_netflix["x"] = [181, 275]
matrix_netflix["c"] = [217, 275]
matrix_netflix["v"] = [253, 275]
matrix_netflix["b"] = [289, 275]
matrix_netflix["n"] = [325, 275]
matrix_netflix["m"] = [361, 275]
matrix_netflix["_"] = [397, 275]


# bouton majuscule
matrix_netflix["#"] = [73, 275]

# pour les caractere speciaux
matrix_netflix["@"] = [145, 340]
matrix_netflix["."] = [217, 340]

# pour le .com
matrix_netflix["+"] = [253, 340]

# pour la suppression des caractres de login
matrix_netflix[")"] = [325, 340]

# pour la suppression des caractres de password
matrix_netflix["&"] = [325, 311]



#######################
# unit functions of sign_in_netflix for azerty keyboard
matrix_netflix_azerty = {}

# Debut de ligne azertyuiop
matrix_netflix_azerty["a"] = [73, 239]
matrix_netflix_azerty["z"] = [109, 203]
matrix_netflix_azerty["e"] = [145, 203]
matrix_netflix_azerty["r"] = [181, 203]
matrix_netflix_azerty["t"] = [217, 203]
matrix_netflix_azerty["y"] = [253, 203]
matrix_netflix_azerty["u"] = [289, 203]
matrix_netflix_azerty["i"] = [325, 203]
matrix_netflix_azerty["o"] = [361, 203]
matrix_netflix_azerty["p"] = [397, 203]

##debut de ligne qsdfghjklm
matrix_netflix_azerty["q"] = [73, 203]
matrix_netflix_azerty["s"] = [109, 239]
matrix_netflix_azerty["d"] = [145, 239]
matrix_netflix_azerty["f"] = [181, 239]
matrix_netflix_azerty["g"] = [217, 239]
matrix_netflix_azerty["h"] = [253, 239]
matrix_netflix_azerty["j"] = [289, 239]
matrix_netflix_azerty["k"] = [325, 239]
matrix_netflix_azerty["l"] = [361, 239]
matrix_netflix_azerty["m"] = [397, 239]

# debut de ligne  zxcvbnm_
matrix_netflix_azerty["w"] = [145, 275]
matrix_netflix_azerty["x"] = [181, 275]
matrix_netflix_azerty["c"] = [217, 275]
matrix_netflix_azerty["v"] = [253, 275]
matrix_netflix_azerty["b"] = [289, 275]
matrix_netflix_azerty["n"] = [325, 275]
matrix_netflix_azerty["-"] = [361, 275]
matrix_netflix_azerty["_"] = [397, 275]


# bouton majuscule
matrix_netflix_azerty["#"] = [73, 275]

# pour les caractere speciaux
matrix_netflix_azerty["@"] = [145, 340]
matrix_netflix_azerty["."] = [217, 340]

# pour le .com
matrix_netflix_azerty["+"] = [253, 340]

# pour la suppression des caractres de login
matrix_netflix_azerty[")"] = [325, 340]

# pour la suppression des caractres de password
matrix_netflix_azerty["&"] = [325, 311]

any_frame = netflix_path_template + "/any_frame/any_frame.png"
tolerance = 5


def goto_cord(char):
    if char.isupper():
        char = char.lower()

    if menu.is_menu_template(perf=False,
                             path=netflix_path_template + "/keyboard_type/",
                             region_frame=stbt.Region(x=75, y=236, width=37, height=35),
                             match_parameters=match_parameters_is_menu):
        keyborad = 'qwerty'
    else:
        keyborad = 'azerty'

    if keyborad == 'qwerty':
        target = matrix_netflix[char]
    elif keyborad == 'azerty':
        target = matrix_netflix_azerty[char]
    else:
        assert False, 'keyboard type qwerty or azerty not selected'
    target_x = target[0]
    target_y = target[1]

    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y + 4

    start_time = time.time()
    while time.time() - start_time < 300:
        if (target_x - tolerance) <= source_x <= (target_x + tolerance) and (target_y - tolerance) <= source_y <= (
                    target_y + tolerance):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(2)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x, target_y))
            sc_stbt.wait(4)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y + 4
    return False


def turn_majus_min():
    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y + 4

    start_time = time.time()
    while time.time() - start_time < 100:
        if (73 - tolerance) <= source_x <= (73 + tolerance) and (275 - tolerance) <= source_y <= (275 + tolerance):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(2)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x=73, target_y=275))
            sc_stbt.wait(4)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y + 4
    return False


def goto_next_step(y_next_step):
    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y + 4

    start_time = time.time()
    while time.time() - start_time < 100:
        if ((218 - tolerance) <= source_x <= (218 + tolerance) or (217 - tolerance) <= source_x <= (
                    217 + tolerance)) and (y_next_step - tolerance) <= source_y <= (y_next_step + tolerance):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(2)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x=218, target_y=y_next_step))
            sc_stbt.wait(4)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y + 4
    return False


def goto_previous_step(y_previous_step):
    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y + 4

    start_time = time.time()
    while time.time() - start_time < 100:
        if ((73 - tolerance) <= source_x <= (73 + tolerance)) and ((y_previous_step - tolerance)) <= source_y <= (
                (y_previous_step + tolerance)):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(2)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x=218, target_y=y_previous_step))
            sc_stbt.wait(4)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y + 4
    return False


def _next_key(source_x, source_y, target_x, target_y):
    if (311 - tolerance) <= source_y <= (311 + tolerance) and source_y < target_y:
        return "KEY_DOWN"
    if (311 - tolerance) <= source_y <= (311 + tolerance) and source_y > target_y:
        return "KEY_UP"
    if (source_y < target_y - tolerance):
        return "KEY_DOWN"
    if (source_y - tolerance > target_y):
        return "KEY_UP"
    if (source_x < target_x - tolerance):
        return "KEY_RIGHT"
    if (source_x - tolerance > target_x):
        return "KEY_LEFT"
