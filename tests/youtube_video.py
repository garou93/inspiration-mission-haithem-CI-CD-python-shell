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
import stbts


# ----------------------- Parameteres and variable --------------------------

youtube_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/youtube/"
path_mask_blackscreen = youtube_path_template + "/black/mask_black.png"
path_mask_motion = youtube_path_template + "/motion/mask_motion.png"

threshold = stbt.get_config("youtube", "threshold", type_=float)
consecutive_frames = stbt.get_config("youtube", "consecutive_frames")
noise_threshold = stbt.get_config("youtube", "noise_threshold", type_=float)

key_pause = stbt.get_config("youtube", "key_pause")
key_forward = stbt.get_config("youtube", "key_forward")
key_back = stbt.get_config("youtube", "key_back")

pause_frame = eval(stbt.get_config("youtube", "pause_frame"))

polling_secs = stbt.get_config("youtube", "polling_secs", type_=int)
test_secs = stbt.get_config("youtube", "test_secs", type_=int)
interval_secs = stbt.get_config("youtube", "interval_secs", type_=int)
wait_pause_secs = stbt.get_config("youtube", "wait_pause_secs", type_=int)

occurence_forward = stbt.get_config("youtube", "occurence_forward", type_=int)
occurence_rewind = stbt.get_config("youtube", "occurence_rewind", type_=int)

match_parameters_is_menu = eval(stbt.get_config("youtube", "match_parameters_is_menu"))
match_parameters_youtube = stbt.MatchParameters(match_method='sqdiff-normed',
                                                           confirm_method='none',
                                                           match_threshold=0.85,
                                                           confirm_threshold=0.3)
match_parameters = eval(stbt.get_config("youtube", "match_parameters"))

region_current_timer = eval(stbt.get_config("youtube", "region_current_timer"))
region_end_timer = eval(stbt.get_config("youtube", "region_end_timer"))



# ------------------------ Constructor ---------------------------------

menu = sc_stbt.menu()
youtube = sc_stbt.video_tests(path_mask_motion=path_mask_motion,
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


# -------------------------------- check publicity -------------------------------

def check_timer():
    if stbt.wait_until(lambda: sc_stbt.timer(region_current_timer, region_end_timer),
                       timeout_secs=12):
        sc_stbt.debug("TIMER DETECTED")
        return True
    else:
        sc_stbt.debug("TIMER NOT DETECTED")
        return False


def skip_publicities_timer():
    sc_stbt.debug("CHECK PUBLICITIES")
    if not check_timer():
        sc_stbt.wait(4)
        if check_timer():
            return True
        else:
            assert False, ("PUBLICITIES DETECTED")
    else:
        return False


def check_cursor():
    """
    check_cursor: check cursor of live
    :return:
    """
    try:
        menu.is_menu(press=['KEY_UP'],
                     text="Cursor motion",
                     path="/../../../trunk/tests/templates/youtube/cursor_motion/",
                     region_frame=stbt.Region(x=44, y=326, width=869, height=32),
                     timeout=2,
                     timeout_is_menu=15,
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                           confirm_method='none',
                                                           match_threshold=0.9,
                                                           confirm_threshold=0.3))
        sc_stbt.debug("CUROSR MOTION DETECTED")
        sc_stbt.wait(5)
        return True
    except:
        sc_stbt.debug("CUROSR MOTION NOT DETECTED")
        return False


def skip_publicities_cursor():
    """
    skip_publicities: check if publicity is displayed and skip it
    :return:
    """
    sc_stbt.debug("SHEARCHING PUBLICITY")
    if check_cursor():
        sc_stbt.debug('PUBLICITY NOT DETECTED')
        return True
    else:
        sc_stbt.debug('PUBLICITY DETECTED')
        sc_stbt.wait(5)
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(8)
        if check_cursor():
            sc_stbt.debug("PUBLICITIES SKIPPED")
            return True
        else:
            assert False, ("PUBLICITIES DETECTED AND NOT SKIPPED")


def check_pause_youtube_timer():
    """
    check_pause_youtube_timer:
    :return:
    """
    if check_timer():
        return True
    else:
        assert False, ("PAUSE IS NOT DONE IN YOUTUBE")


def check_pause_youtube_cursor():
    """
    check_pause_youtube_cursor: when pause is done, check if the video is paused in youtube video
    :return:
    """
    sc_stbt.debug("CHECK YOUTUBE IS PAUSED")
    if check_cursor():
        sc_stbt.debug('YOUTUBE IS PAUSED')
        return True
    else:
        assert False, ("PAUSE IS NOT DONE IN YOUTUBE")


# --------------------------- Tests Youtube -----------------------------

def test_open_video_youtube(video_name = None , callable = None):
    """
    test_open_video_youtube: open video and detect blackscreen
    :return: true when blackscreen is detected , false is not
    """
    sc_stbt.wait(5)
    sc_stbt.write_statut_test(statut="test_ko")
    if is_youtube():
        if video_name is None:
            video_name = stbt.get_config("youtube", "video_name")
            if video_name != "":

                sc_stbt.search_video(video_name,callable)
                sc_stbt.write_statut_test(statut="test_ok")
            else:
                try:
                    youtube.open(path_mask_blackscreen=path_mask_blackscreen)
                    sc_stbt.debug('YOUTUBE VIDEO START')
                    sc_stbt.wait(3)
                    sc_stbt.write_statut_test(statut="test_ok")
                except:
                    assert False, "Video NOT OPENED"
        else:
            sc_stbt.search_video(video_name,callable)
            sc_stbt.write_statut_test(statut="test_ok")
    else:
        # if test_open_video_youtube() fail ,the rest of youtube tests fail to
        sc_stbt.write_statut_test(statut="test_ko")
        assert False, ("YOUTUBE APPLICATION NOT START")


def test_youtube_motion(test_secs=test_secs,
                        polling_secs=polling_secs,
                        interval_secs=interval_secs):
    """
    test_youtube_motion: detect motion from youtube video
    :return:true where motion is detected , False is not
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    youtube.test_motion(polling_secs=polling_secs,
                        test_secs=test_secs,
                        interval_secs=interval_secs)


def test_youtube_pause(test_secs=test_secs,
                       polling_secs=polling_secs,
                       interval_secs=interval_secs):
    """
    test_youtube_pause: check video is paused
    :return:    *if moition is not detected (video paused )==> play() (make video play ==> pause (make video
                pause)
                * elif motion is detected (video pause) ==> pause (make video pause)

                return false when:
                1) if video paused: when play() not done (motion not detected)
                2) if video paused ==>  play() done ==> when pause() not done (motion detected)
                3) if video played ==> when pause() not done (motion detected)
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()

    youtube.pause(test_secs=test_secs,
                  polling_secs=polling_secs,
                  interval_secs=interval_secs,
                  key_pause=key_pause)
    try:
        check_pause_youtube_timer()
    except:
        check_pause_youtube_cursor()


def test_youtube_play(test_secs=test_secs,
                      polling_secs=polling_secs,
                      interval_secs=interval_secs):
    """
    test_youtube_play: check video is played
    :return: *if moition is detected (video played ) ==> pause() (make video pause)==> play (make video play)
                * elif motion is not detected (video paused) ==> play (make video play)

                return false when:
                1) if video played: when pause() not done (motion detected)
                2) if video played ==>  pause() done ==> when play() not done (motion not detected)
                3) if video paused ==> when play() not done (motion not detected)
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    youtube.play(test_secs=test_secs,
                 polling_secs=polling_secs,
                 interval_secs=interval_secs,
                 key_pause=key_pause)


def test_youtube_fastforward(occurence_forward=occurence_forward):
    """
    test_youtube_fastforward: check motion is forwarded
    :return:
            * Make video play with test_youtube_play()
            * use trick_mode with press= forward of video class (see how to use video)
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    key_fastforward = eval(stbt.get_config("remotes", "key_fastforward"))
    if key_fastforward:
        youtube.fastforward(occurence_forward=occurence_forward,
                            key_forward=key_forward,
                            key_pause=key_pause)
    else:
        if check_cursor():
            sc_stbt.press("KEY_RIGHT")
            try:
                youtube.motion(polling_secs=5)
            except:
                sc_stbt.crop(stbt.get_frame(), region=stbt.Region(x=1, y=2, width=955, height=337), file_name="frame")
                sc_stbt.combo_press(["KEY_RIGHT"], number_press=occurence_forward)
                if not stbt.wait_until(lambda: stbt.match("frame.png",
                                                          region=stbt.Region(x=1, y=2, width=955, height=337),
                                                          match_parameters=match_parameters).match,
                                       timeout_secs=5):
                    sc_stbt.press("KEY_OK")
                    return True
                else:
                    assert False, "fastforward not done"
            assert False, "fastforward not done"

        else:
            assert False, "Video not opened"


def test_youtube_rewind(occurence_rewind=occurence_rewind):
    """
    test_youtube_fastforward: check motion is rewinded
    :return: * Make video play with test_youtube_play()
             * use trick_mode with press= rewind of video class (see how to use video)
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    key_rewind = eval(stbt.get_config("remotes", "key_rewind"))
    if key_rewind:
        youtube.rewind(occurence_rewind=occurence_rewind,
                       key_pause=key_pause)
    else:
        if check_cursor():
            sc_stbt.press("KEY_LEFT")
            try:
                youtube.motion(polling_secs=5)
            except:
                sc_stbt.crop(stbt.get_frame(), region=stbt.Region(x=1, y=2, width=955, height=337), file_name="frame")
                sc_stbt.combo_press(["KEY_LEFT"], number_press=occurence_forward)
                if not stbt.wait_until(lambda: stbt.match("frame.png",
                                                          region=stbt.Region(x=1, y=2, width=955, height=337),
                                                          match_parameters=match_parameters).match,
                                       timeout_secs=5):
                    sc_stbt.press("KEY_OK")
                    return True
                else:
                    assert False, "rewind not done"
            assert False, "rewind not done"
        else:
            assert False, "Video not opened"


def test_youtube_next_video(test_next_video_motion=None):
    """
    test_youtube_next_video: go to next video and detect blackscreen
    :return: * Make video play with test_youtube_play()
                * use change_video with press = next_video of video class (see how to use video)

                return False when:
                1) blackscreen not detected
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    key_next_video = eval(stbt.get_config("remotes", "key_next_video"))
    if key_next_video:
        youtube.next_video(key_pause=key_pause)
    else:
        sc_stbt.wait(6)
        if check_timer():
            sc_stbt.combo_press(["KEY_RIGHT"], number_press=3)
            youtube.open(path_mask_blackscreen=path_mask_blackscreen)
            if test_next_video_motion:
                sc_stbt.wait(5)
                test_youtube_motion()
        else:
            assert False, "Video not opened"


def test_youtube_previous_video():
    """
    test_youtube_next_video: go to next video and detect blackscreen
    :return: * Make video play with test_youtube_play()
                * use change_video with press = next_video of video class (see how to use video)

                retunr False when:
                1) blackscreen not detected
    """
    sc_stbt.wait(5)
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    try:
        skip_publicities_timer()
    except:
        skip_publicities_cursor()
    key_previous_video = eval(stbt.get_config("remotes", "key_rewind"))
    if key_previous_video:
        youtube.previous_video(key_pause=key_pause)
    else:
        if check_timer():
            sc_stbt.press('KEY_LEFT')
            youtube.open(path_mask_blackscreen=path_mask_blackscreen)
        else:
            assert False, "Video not opened"


def test_exit_youtube():
    """
    test_exit_youtube: exit from youtube live or menu
    :return:
            * press key back or exit until detect popup exit youtube menu
            * press key right and key ok
            * if device is magewelle: check if menu youtube is not displayed and return true
            * else detect blackscreen and return true

    """
    sc_stbt.get_statut_test("YOUTUBE MENU NOT FOUND")
    sc_stbt.wait(5)
    android = eval(stbt.get_config("adb", "adb_press"))
    if not android:
        # searching exit popup
        stbts.press_until_match_any_text(press_key="KEY_BACK",
                                         text=["YouTube"],
                                         region=stbt.Region(x=606, y=52, width=336, height=30),
                                         timeout_secs=3,
                                         threshold=0.8,
                                         timeout=30)
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(2)
        if not stbts.match_text(text="YouTube",
                                region=stbt.Region(x=606, y=43, width=336, height=44),
                                timeout_secs=2,
                                threshold=0.8).match:
            sc_stbt.debug("EXIT YOUTUBE DONE")
        else:
            assert False, "EXIT YOUTUBE NOT DONE"


    else:
        if is_youtube('KEY_EXIT'):
            sc_stbt.press('KEY_HOME')
        else:
            assert False, "LOST OF KEY EXIT"
    sc_stbt.wait(5)  # wait time for exit close and exit form youtube menu
    # if menu youtube is closed
    if not menu.is_menu_template(perf=False,
                                path=youtube_path_template +"/home_youtube/" ,
                                region_frame=stbt.Region(x=26, y=145, width=26, height=24),
                                timeout=3):
        sc_stbt.debug("EXIT YOUTUBE DONE")
    else:
        sc_stbt.debug("EXIT YOUTUBE NOT DONE")
        assert False, ("EXIT YOUTUBE NOT DONE")


def is_youtube(press=None, wait_app=5):
    """
    is_youtube: check if youtube menu is displayed
    :return: True when youtube menu is displayed
    """
    if press is not None:
        sc_stbt.press(press)
    sc_stbt.wait(wait_app)
    if stbts.match_text(text="Youtube",
                        region=stbt.Region(x=119, y=77, width=78, height=40),
                        timeout_secs=5,
                        threshold=0.9).match:
       sc_stbt.debug('Welcome Found')
       try:
           menu.is_menu(press=['KEY_DOWN'],
                     path="/../../../trunk/tests/templates/youtube/new_signin/skip/",
                     region_frame=stbt.Region(x=606, y=367, width=323, height=79),
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                           confirm_method='none',
                                                           match_threshold=0.9,
                                                           confirm_threshold=0.3),
                     wait_after_press=3,
                     timeout_is_menu=6)
       except:
           menu.is_menu(press=['KEY_DOWN'],
                     path="/../../../trunk/tests/templates/youtube/new_signin/skip/",
                     region_frame=stbt.Region(x=619, y=336, width=46, height=40),
                     match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                           confirm_method='none',
                                                           match_threshold=0.9,
                                                           confirm_threshold=0.3),
                     wait_after_press=3,
                     timeout_is_menu=6)
       sc_stbt.press("KEY_OK")

    if menu.is_menu_template(perf=False,
                             path=youtube_path_template + "/new_signin/",
                             region_frame=stbt.Region(x=600, y=167,width=152,height=125),
                             match_parameters=match_parameters_youtube,
                             timeout=3):
        menu.is_menu(press=['KEY_DOWN'],
                     text="Skip",
                     path="/../../../trunk/tests/templates/youtube/new_signin/skip/",
                     region_frame=stbt.Region(x=606, y=220, width=323, height=79),
                     match_parameters=match_parameters_youtube,
                     timeout=2,
                     timeout_is_menu=4)
        sc_stbt.press("KEY_OK")

    # searching new signin popup
    elif stbts.match_any_text(text=["Welcome"],
                            region=stbt.Region(x=616, y=73, width=248, height=49),
                            timeout_secs=5,
                            threshold=0.9).match or menu.is_menu_template(perf=False,
                                                                          path=youtube_path_template + "/new_signin//",
                                                                          region_frame=stbt.Region(x=183, y=167,
                                                                                                   width=152,
                                                                                                   height=125),
                                                                          match_parameters=match_parameters_youtube,
                                                                          timeout=2):
        sc_stbt.debug('Welcome Found')
        menu.is_menu(press=['KEY_DOWN'],
                     text="Skip",
                     path="/../../../trunk/tests/templates/youtube/new_signin/skip/",
                     region_frame=stbt.Region(x=606, y=367, width=323, height=79),
                     match_parameters=match_parameters_youtube,
                     wait_after_press=6,
                     timeout_is_menu=6)
        sc_stbt.press("KEY_OK")
    try:
        menu.is_menu(text = "youtube home",
                    path="/../../../trunk/tests/templates/youtube/home_youtube/" ,
                    region_frame=stbt.Region(x=26, y=145, width=26, height=24),
                    timeout=3,
                    timeout_is_menu=3)
        return True
    except:
        try:
            menu.is_menu(press=["KEY_BACK"],
                        path="/../../../trunk/tests/templates/youtube/home_youtube/",
                        region_frame=stbt.Region(x=26, y=145, width=26, height=24),
                        text="youtube home",
                        timeout=3,
                        timeout_is_menu=12)
            return True
        except:
            return False


def back_to_youtube_menu():
    """
    back_to_youtube_menu: back to youtube menu and check if it is displayed
    :return:
    """
    try:
        try:
            menu.is_menu(text = "youtube home",
                    path="/../../../trunk/tests/templates/youtube/home_youtube/" ,
                    region_frame=stbt.Region(x=26, y=145, width=26, height=24),
                    timeout=3,
                    timeout_is_menu=3)
            sc_stbt.debug("MENU YOUTUBE IS DISPLAYED")
            return True
        except:
            menu.is_menu(press=["KEY_EXIT"],
                        path="/../../../trunk/tests/templates/youtube/home_youtube/",
                        region_frame=stbt.Region(x=26, y=145, width=26, height=24),
                        text="youtube home",
                        timeout=3,
                        timeout_is_menu=12)
            sc_stbt.debug("MENU YOUTUBE IS DISPLAYED")
            return True
    except:
        sc_stbt.debug("MENU YOUTUBE IS NOT DISPLAYED")
        return False


# ----------------------- Test navigation youtube -----------------

def test_navigation_youtube(navigation_play_video=None, navigation_time_out=None):
    """
    test_navigation_youtube: navigate in youtube
    :param press:
    :return:
    """
    if navigation_play_video is None:
        navigation_play_video = eval(stbt.get_config("youtube", "navigation_play_video"))
    if navigation_time_out is None:
        navigation_time_out = eval(stbt.get_config("youtube", "navigation_time_out"))
    try:
        if back_to_youtube_menu():
            sc_stbt.repeat(lambda: navigation_youtube(navigation_play_video),
                           time_out=navigation_time_out)
        else:
            assert False, "YOUTUBE MENU IS NOT DISPLAYED"
    except:
        if back_to_youtube_menu():
            pass
        else:
            assert False, "Problem in test navigation:"


def navigation_youtube(navigation_play_video):
    """
    navigation_youtube: navigation in menu youtube
    :return:
    """
    sc_stbt.write_statut_test(statut="test_ok")
    sc_stbt.crop(stbt.get_frame(),
                 region=stbt.Region(x=114, y=256, width=566, height=103),
                 file_name="frame")
    sc_stbt.combo_press(combo=["KEY_RIGHT"], number_press=10, delay_sec=0.5)
    sc_stbt.combo_press(combo=["KEY_LEFT"], number_press=10, delay_sec=0.5)
    if menu.is_menu_template(perf=False,
                             path=youtube_path_template+"/mobile/",
                             region_frame=stbt.Region(x=606, y=367, width=323, height=79),
                             timeout=3):
        sc_stbt.press("KEY_RIGHT")
    sc_stbt.combo_press(combo=["KEY_DOWN"], number_press=10, delay_sec=0.5)
    if stbt.match(image="frame.png").match:
        assert False, "NAVIGATION YOUTUBE IS NOT DONE"


    else:
        sc_stbt.combo_press(combo=["KEY_UP"], number_press=10, delay_sec=0.5)
        if menu.is_menu_template(perf=False,
                             path=youtube_path_template+"/mobile/up/",
                             region_frame=stbt.Region(x=154, y=55, width=21, height=7),
                             timeout=5):
            sc_stbt.press("KEY_DOWN")
        if navigation_play_video:
            sc_stbt.press("KEY_OK")
            youtube.open(path_mask_blackscreen=path_mask_blackscreen)
            sc_stbt.wait(5)
            test_youtube_motion(polling_secs=20,
                                test_secs=8,
                                interval_secs=5)
            if back_to_youtube_menu():
                pass
            else:
                assert False, "NAVIGATION YOUTUBE IS NOT DONE"

    sc_stbt.debug("NAVIGATION YOUTUBE IS DONE")





    # check if video will be end after 3 minute with timer
    # def recheck_end():
    #     import datetime
    #     global x
    #     x = []
    #     list = []
    #     assert stbt.wait_until(lambda:timer(timer_value = True),timeout_secs= 20)
    #     list.append(x[0])
    #     list.append(x[1])
    #     z = str(x[0]).split(":")
    #     v = str(x[1]).split(":")
    #     if z.__len__() < 3 or v.__len__() < 3:
    #         t = datetime.time(0,int(z[0]),int(z[1]))
    #         tf = datetime.time(0,int(v[0]),int(v[1]))
    #     elif z.__len__() < 3 and v.__len__() == 3:
    #         t = datetime.time(0,int(z[0]),int(z[1]))
    #         tf = datetime.time(int(v[0]),int(v[1]),int(v[2]))
    #     else:
    #         t = datetime.time(int(z[0]),int(z[1]),int(z[2]))
    #         tf = datetime.time(int(v[0]),int(v[1]),int(v[2]))
    #     from datetime import datetime
    #     if (datetime.strptime(str (tf), '%H:%M:%S') -\
    #         datetime.strptime(str(t), '%H:%M:%S')).total_seconds() < 150:
    #         print (datetime.strptime(str (tf), '%H:%M:%S') -\
    #         datetime.strptime(str(t), '%H:%M:%S')).total_seconds()
    #         print ">>>>>>>>>LE FILM est presque fini"
    #         return False
    #     else:
    #         print ">>>>>>>>>YOU COULD DO THE TRICKMODE"
    #         return True
    #
    # def check_end():
    #     skip_publicities()
    #     if stbt.wait_until(lambda:recheck_end(),timeout_secs=60):
    #         return True
    #     else:
    #         skip_publicities()
