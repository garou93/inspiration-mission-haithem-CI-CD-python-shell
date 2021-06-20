#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import logging
import time
import sc_stbt
import stbt
import video
import menu

generic_path = sc_stbt.get_generic_template_path()
live = video.video()
menu = menu.menu()
current_lcn = 0
COMBO_3_EXIT = ["KEY_EXIT", "KEY_EXIT", "KEY_EXIT"]


def check_subtitles(min_legnth_text=None, subtitles_language=None, subtitles_color=None, subtitles_region=None, frame=None):
    """
    Function: Check for subtitles
    :param min_legnth_text: min length of reading subtitles to return True
    :return: True if we found text that his length > min_legnth_text
             False if not
    """
    if min_legnth_text is None:
        min_legnth_text = stbt.get_config("subtitles", "min_legnth_text", type_=float)

    if subtitles_language is None:
        subtitles_language = stbt.get_config("subtitles", "subtitles_language")

    if subtitles_color is None:
        subtitles_color = eval(stbt.get_config("subtitles", "subtitles_color"))

    if subtitles_region is None:
        subtitles_region = eval(stbt.get_config("subtitles", "subtitles_region"))

    subtitles = sc_stbt.get_text(region=subtitles_region,
                                 text_color=subtitles_color,
                                 lang=subtitles_language,
                                 frame=frame)
    if len(subtitles) > min_legnth_text:
        sc_stbt.debug("Subtitles FOUND")
        return True
    return False


def zap_to_channel(lcn, interpress_delay_secs=0.5, interval_secs=0):
    """
    Function: zap_to_channel: is based on <stbt.press> command control for remote
              Send the specified key-press to the system under test

    Examples: zap_to_channel("13")
              zap_to_channel("13", 0.7):
                1) KEY_PRESS_1
                2) wait 0.7 seconds
                3) KEY_PRESS_3

    NB: if we don't pass the param interpress_delay_secs, STS Tester will get
        it from config file specific to current project

    :param lcn: channel number to zap
    :param interpress_delay_secs: inter press delay
    :return: time system after press
    """
    for i in range(0, len(lcn)):
        sc_stbt.press('KEY_' + lcn[i],
                   delay_sec=interpress_delay_secs)
    sc_stbt.debug("ZAP TO ", str(lcn))
    start_time_perf = time.time()
    sc_stbt.wait(interval_secs)
    return start_time_perf


def zap_up_down(action="UP",interval_secs=0, up=None):
    """
    Function: zap_up_down: is based on "stbt.press" command control for remote
              Send the specified key-press to the system under test.

    Examples: zap_up_down("UP") : if the current channel is 1
                                  we zap to channel 2
              zap_up_down("DOWN"): if the current channel is 2
                                  we zap to channel 1

    :param action: can be "UP" or "DOWN" (CH+ or CH-)
    :return: time system after press
    """

    if action not in ["UP", "DOWN","RIGHT","LEFT"]:
        logging.error('Bad argument action, action should be "UP" or "DOWN" ')
        raise Exception('Bad argument action, action should be "UP" or "DOWN" ')
    else:
        if up :
            sc_stbt.press('KEY_' + action)
        else:
            sc_stbt.press('KEY_CHANNEL' + action)
        logging.info(str(action))
        start_time_perf = time.time()
        sc_stbt.wait(interval_secs)
    return start_time_perf


def zap_line_up_down(action="UP"):

    if action not in ["UP", "DOWN"]:
        logging.error('Bad argument action, action should be "UP" or "DOWN" ')
        raise Exception('Bad argument action, action should be "UP" or "DOWN" ')
    else:
        sc_stbt.press('KEY_' + action)
        logging.info(str(action))
        start_time_perf = time.time()
    return start_time_perf


def read_lcn(lcn, lcn_region=None,current=False):
    """
    Function: read_lcn : apply OCR filters to extract the lcn from the info banner

    :param lcn: channel number to try reading
    :return: fail in case we can't read the lcn until timeout

    NB: default timeout = 10 seconds
                <timeout> is a param from section <zapping> on
                config file specific to current project
        region : is where the filter applyed on info_banner to read the lcn
        threshold: percentage of tolerance (default value in config file)
        timeout: time out before test failing (default value is 10)
        mode: the mode of OCR
        tesseract_user_patterns: a format of text searching
            Example: tesseract_user_patterns=[r'\d\d\d\d']
                    we search for a number that contain  4 digits
            NB: \d = [0-9]
    """
    if lcn_region is None:
        lcn_region=eval(stbt.get_config("zapping", "lcn_region"))

    result = sc_stbt.ocr_until(region=lcn_region,
                      menu_text=lcn,
                      threshold=stbt.get_config("zapping",
                                                "threshold",
                                                type_=float),
                      timeout=stbt.get_config("zapping",
                                              "timeout",
                                              type_=float),
                      interval_secs=stbt.get_config("zapping",
                                                    "interval_secs",
                                                    type_=float),
                      mode=stbt.OcrMode.SINGLE_WORD,
                      tesseract_user_patterns=[r'\d\d\d\d'])
   
    if current :
        current_lcn = sc_stbt.is_text(region=lcn_region,
                                threshold = stbt.get_config("zapping","threshold",type_=float),
                                mode=stbt.OcrMode.SINGLE_WORD,
                                tesseract_user_patterns=[r'\d\d\d\d'])
        set_current_lcn(current_lcn)
    if result == True:
        sc_stbt.debug("The lcn is detected")
    else:
        sc_stbt.debug("The lcn is not detected")

    return result

def set_current_lcn(lcn):
    """

    :param lcn:
    :return:
    """
    global current_lcn
    current_lcn = lcn

def get_current_lcn():
    """

    :return:
    """
    return current_lcn



def test_zap_black_screen_on(path):
    """
    Function:  test_zap_black_screen_on: check for existence of the black screen

    NB: a mask is used to detect the black screen

    :param path: path of black screen templates used in matching
    :return: True: if the black screen is matched
             False: if the black screen is not matched until timeout
    """
    path += "/mask_blackscreen/mask.png"
    if stbt.wait_until(lambda: stbt.is_screen_black(mask=path)):
        logging.info("The BLACK SCREEN is MATCHED")
        return True
    else:
        logging.info("The BLACK SCREEN is NOT MATCHED")
        return False


def test_zap_black_screen_off(path):
    """
    Function:  test_zap_black_screen_off: check for disappearance of the black screen

    :param path: path of black screen templates used in matching
    :return: True: if the black screen is not matched until timeout
             False:  if the black screen is matched
    """
    path += "/mask_blackscreen/mask.png"
    if stbt.wait_until(lambda: not stbt.is_screen_black(mask=path)):
        logging.info("The BLACK SCREEN is NOT MATCHED")
        return True
    else:
        logging.info("The BLACK SCREEN is MATCHED")
        return False


def test_zap_info_banner(path, lcn, confirm_method=False, banner_region=None, lcn_region=None):
    """
    Function: test_zap_info_banner: used to detect the info_banner to check zapping
              if: the info_banner is matched , the zapping is OK
              else : the zapping is KO
    :param path: path of info_banner templates used in matching
    :param lcn: channel number to zap
    :return: True: if the info banner is matched
             False: if the info_banner is not matched until the timeout
    """
    match_parameters_zapping = eval(stbt.get_config("zapping","match_parameters_zapping"))
    path += "/info_banner"
    if confirm_method:
        mp = match_parameters_zapping
    else:
        mp = stbt.MatchParameters(confirm_method='absdiff')
    if banner_region is None:
        banner_region = eval(stbt.get_config("zapping","banner_region"))

    if sc_stbt.wait_for_many_match(sc_stbt.get_all_templates_in_directory(path), match_parameters=mp,
                                   region=banner_region,
                                   timeout_secs=stbt.get_config("zapping",
                                                                "timeout",
                                                                type_=float)):
        sc_stbt.debug("The INFO BANNER is MATCHED")

        return True
    else:
        return False


def is_live(time_out=30, polling_secs=10):
    """
    Function: is_live: check for live motion

    Example: is_live(40, 20)
            1) wait 20 seconds
            2) check for motion until 40 seconds

    NB: polling_secs is used to synchronize live motion
        for example when zapping, some service need from 15 to 20
        seconds to start live motion

    :param time_out: time out to check for motion
    :param polling_secs: time to wait before start checking for motion
    :return: fail if we passed the timeout without detecting a motion
    """
    sc_stbt.wait(polling_secs)
    stbt.wait_for_motion(timeout_secs=time_out,
                         consecutive_frames="5/500")
    logging.info("MOTION DETECTED")


def zap_with_info_banner(callable, path, lcn):
    callable()
    test_zap_info_banner(path, lcn)


def zap_with_black_screen(callable, path):
    callable()
    test_zap_black_screen_on(path)




def zapping(callable,android=None, lcn=None, path=generic_path, perf=None, confirm_method=None, black_screen=None,
            info_banner=None, motion=None, banner_region=None, lcn_region=None):
    """
    zapping is a function that test zapping, black screen , info banner
    and motion with or without perf
    black_screen: check black screen or not
    info_banner: check info banner or not
    motion: check motion or not

    :param callable: function of zapping(go_to_channel, zap_up_down)
    :param lcn: channel number to zap
    :param path: the global path of current project
    :param perf: calculate performance
    """
    if android is None:
        android = False
    else :
        android = True

    if not android :
        if black_screen is None:
            black_screen = eval(stbt.get_config("zapping", "check_black_screen"))

        if info_banner is None:
            info_banner = eval(stbt.get_config("zapping", "check_info_banner"))

        if motion is None:
            motion = eval(stbt.get_config("zapping", "check_motion"))

        if perf is None:
            perf = eval(stbt.get_config("zapping", "perf"))
    else :
        if black_screen is None:
            black_screen = eval(stbt.get_config("zapping", "check_black_screen_android"))

        if info_banner is None:
            info_banner = eval(stbt.get_config("zapping", "check_info_banner_android"))

        if motion is None:
            motion = eval(stbt.get_config("zapping", "check_motion_android"))

        if perf is None:
            perf = eval(stbt.get_config("zapping", "perf_android"))

    start_time_perf = callable()
    if black_screen:
        assert sc_stbt.test_zap_black_screen_on(path), \
            "The black screen is NOT DETECTED"
    if perf:
        result_black_screen_off = test_zap_black_screen_off(path)
        if result_black_screen_off is True:
            end_time_perf = time.time()
            diff_time = end_time_perf - start_time_perf
            sc_stbt.write_csv_file("perf_zapping.csv", [[lcn, diff_time]])
        else:
            sc_stbt.debug("Black screen still ON within 10 seconds")
            sc_stbt.debug("No perf time saved for this service")

    if info_banner:
        assert test_zap_info_banner(path=path,
                                    lcn=lcn,
                                    confirm_method=confirm_method,
                                    banner_region=banner_region,
                                    lcn_region=lcn_region),\
           "No info banner matched"
    if motion:
        is_live()



def zap_two_channel(interval_secs, chan1=None, chan2=None):
    """
    zap_two_channel : this is a zapping from chan1 to chan2,

    for those following param : if there are not passed to a function => get them from stbt configuration file
    :param chan1 : channel
    :param chan2 : channel
    :param interval_secs : time between zapping from chan1 => chan2

    """
    if chan1 is None:
        chan1 = stbt.get_config("zapping", "chan_num_1")
    if chan2 is None:
        chan2 = stbt.get_config("zapping", "chan_num_2")

    sc_stbt.zap_to_channel(chan1, interval_secs=interval_secs)
    sc_stbt.zap_to_channel(chan2, interval_secs=interval_secs)


def endurance_zapping(callable, iteration=None, pref_chan=None, interval_secs=None, path_mask_motion=None,
                      check_pop_up=False):
    """
    endurance_zapping: repeat the callable function n times
    :param callable: function of zapping(zap_two_channel, zap_up_down)

    for those following param : if there are not passed to a function => get them from stbt configuration file
    :param iteration : occurence of callable
    :param interval_secs : unity time of execution on the function callable
    :param perf_chan :the perefred channel for checking live
    :param path_mask_motion: the path of mask motion(if we need a specific mask
           else it work with the generic mask motion of the project)
    :param check_pop_up: check for the pop_up received signal after endurance
           zapping and before test for live

    """
    if iteration is None:
        iteration = stbt.get_config("zapping", "iteration", type_=float)
    if pref_chan is None:
        pref_chan = stbt.get_config("zapping", "pref_chan")
    if interval_secs is None:
        interval_secs = stbt.get_config("zapping", "interval_secs_endurance", type_=float)

    sc_stbt.repeat(lambda: callable(),
                   occurence=iteration,
                   wait_=interval_secs)
    sc_stbt.debug("FINISH ZAPPING AND CHECKING FOR LIVE")
    sc_stbt.wait(5)

    # test for pop_up received signal
    if check_pop_up == True:
        # if menu.is_menu_ocr(perf=False,
        #                     text=stbt.get_config("pop_up", "text_reception_signal_missing"),
        #                     region_text=eval(stbt.get_config("pop_up", "region_reception_signal_missing")),
        #                     text_color=eval(stbt.get_config("pop_up", "text_color_reception_signal_missing"))):
        #     sc_stbt.press("KEY_OK")
        sc_stbt.combo_press(COMBO_3_EXIT)
    zapping(lambda: zap_to_channel(lcn=pref_chan, interval_secs=1),
            lcn=pref_chan, path=generic_path, perf=False, confirm_method=None, black_screen=None,
            info_banner=None, motion=False, banner_region=None, lcn_region=None)

    sc_stbt.wait(5)
    return live.is_motion(path=path_mask_motion,
                          consecutive_frames="5/30",
                          noise_threshold=0.95)


