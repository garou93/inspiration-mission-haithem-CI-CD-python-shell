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
import stbt
import logging
import time
import enchant
import re
import csv


class menu(object):
    def is_menu_dict(self,
                     perf,
                     text,
                     region_text,
                     dict_lang="en",
                     reg_express=None,
                     replace=None,
                     lang="eng",
                     mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
                     threshold=None,
                     text_color=None,
                     tesseract_user_patterns=None):
        """
        is_menu_dict: check for text with dictionary
        :param perf: Boolean for calculating zap performance between menus
        :param text: searched text
        :param region_text: region where to detect the reference text
        :param dict_lang: language of dictionary to use
        :param reg_express: regular expression to apply to text read with get_text() to ignore some special character
        :param replace: expression to replace some character by others in text read by get_text()
        :param lang: The three-letter ISO-639-3 language code of the language you are
                    attempting to read for example eng for English or deu for German.
        :param mode: Tesseract's layout analysis mode
        :param threshold:
        :param text_color: Color of the text. Specifying this can improve OCR results when
                    tesseract's default thresholding algorithm doesn't detect the text,
                    for example for white text on a light-colored background.
        :param tesseract_user_patterns: tesseract_user_patterns: List of patterns to add to the tesseract dictionary.
                        The tesseract pattern language corresponds roughly to the
                        following regular expressions:
                        tesseract  regex
                        =========  ===========
                        \c         [a-zA-Z]
                        \d         [0-9]
                        \n         [a-zA-Z0-9]
                        \p         [:punct:]
                        \a         [a-z]
                        \A         [A-Z]
                        \*           *
        :return:  True when text found, false where text is not found
        """

        sc_stbt.debug(msg="SEARCHING WITH DICT", text=text)
        start_time_perf = time.time()
        read_text = sc_stbt.get_text(region=region_text,
                                     threshold=threshold,
                                     mode=mode,
                                     tesseract_user_patterns=tesseract_user_patterns,
                                     text_color=text_color,
                                     lang=lang)


        sc_stbt.debug("READ TEXT ", read_text)
        result = False
        dict = enchant.Dict(dict_lang)
        dict.add(text.lower())
        sc_stbt.debug(text.lower())
        if reg_express is not None:
            read_text = re.sub(reg_express, replace, read_text)
        suggest_list = dict.suggest(read_text.lower())
        # test if suggest list is empty
        logging.info("suggest_list = %s", suggest_list)
        if text.lower() in suggest_list:
            sc_stbt.debug(text, " IS FOUND IN SUGGEST LIST")
            result = True

        if perf:
            end_time_perf = (time.time() - start_time_perf)
            sc_stbt.write_csv_file("perf_menu.csv", [["a", end_time_perf]])

        if not result:
            sc_stbt.debug(text, " IS NOT FOUND IN SUGGEST LIST")

        return result


    def is_menu_template(self, perf, path, region_frame=stbt.Region.ALL, timeout=10, match_parameters=None, perf_name='perf_menu'):
        """
        is_menu_template: check Menu is displayed with template method
        :param perf:Boolean for calculating zap performance between menus
        :param path: path to the reference template of menu
        :param region_frame: region where to detect the reference template
        :param timeout:Number of seconds that the image was searched
        :param match_parameters:Customise the image matching algorithm
        :return: True when frame matched, false where not
        """

        starttime_perf = time.time()
        result = sc_stbt.wait_for_many_match(sc_stbt.get_all_templates_in_directory(path),
                                             region=region_frame,
                                             timeout_secs=timeout,
                                             match_parameters=match_parameters)
        if result:
            if perf == True:
                endtime_perf = (time.time() - starttime_perf) - 0.3
                sc_stbt.write_csv_file(str(perf_name) +".csv", [["a", endtime_perf]])
            return result

    def is_menu_ocr(self, perf, text, region_text,
                    threshold=None, text_color=None,
                    mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
                    tesseract_user_patterns=None, lang="eng",
                    timeout=10, interval_secs=0, perf_name="perf_menu", filter=False):
        """
        is_menu_ocr: check Menu is displayed with ocr method
        :param perf: Boolean for calculating zap performance between menus
        :param text: text to the reference text of menu
        :param region_text: region where to detect the reference text
        :param threshold: The maximum allowed difference between any given text and ocr text
        :param text_color: Color of the text. Specifying this can improve OCR results when
                    tesseract's default thresholding algorithm doesn't detect the text,
                    for example for white text on a light-colored background.
        :param mode:Tesseract's layout analysis mode
        :param tesseract_user_patterns: tesseract_user_patterns: List of patterns to add to the tesseract dictionary.
                        The tesseract pattern language corresponds roughly to the
                        following regular expressions:
                        tesseract  regex
                        =========  ===========
                        \c         [a-zA-Z]
                        \d         [0-9]
                        \n         [a-zA-Z0-9]
                        \p         [:punct:]
                        \a         [a-z]
                        \A         [A-Z]
                        \*           *
        :param lang:The three-letter ISO-639-3 language code of the language you are
                    attempting to read for example eng for English or deu for German.
        :param timeout:Number of seconds that the image was searched
        :param interval_secs: The number of seconds to wait for a match before pressing again
        :return: True when text found, false where text is not found
        """
        if threshold is None:
            threshold = stbt.get_config("is_menu", "threshold", type_=float)

        sc_stbt.debug(msg="Searching", text=unicode(text, "utf-8"))
        starttime_perf = time.time()

        result = sc_stbt.ocr_until(region=region_text, menu_text=text,
                                   threshold=threshold, timeout=timeout,
                                   interval_secs=interval_secs, text_color=text_color,
                                   mode=mode, tesseract_user_patterns=tesseract_user_patterns,
                                   lang=lang, filter=filter)

        if result:
            if perf == True:
                endtime_perf = (time.time() - starttime_perf) - 0.3
                sc_stbt.write_csv_file(str(perf_name)+".csv", [["a", endtime_perf]])
        return result

    def checkismenu(self, perf,
                    perf_name,
                    press, text, region_text,
                    path, region_frame,
                    threshold,
                    text_color,
                    mode,
                    tesseract_user_patterns,
                    lang,
                    timeout,
                    interval_secs,
                    match_parameters,
                    wait_after_press,
                    dict_lang,
                    reg_express,
                    replace):
        if press is None:
            pass
        else:
            sc_stbt.combo_press(press)
            sc_stbt.wait(wait_after_press)
        if region_text is None:
            if self.is_menu_template(perf, path, region_frame,
                                     timeout, match_parameters, perf_name):
                return True
            else:
                return False
        elif path is None:
            if self.is_menu_ocr(perf, text, region_text,
                                threshold, text_color,
                                mode, tesseract_user_patterns,
                                lang,
                                timeout, interval_secs,perf_name):
                return True
            elif reg_express is not None:
                if self.is_menu_dict(perf,
                                     text=text,
                                     region_text=region_text,
                                     dict_lang=dict_lang,
                                     reg_express=reg_express,
                                     replace=replace,
                                     lang=lang,
                                     mode=mode,
                                     threshold=threshold,
                                     text_color=text_color,
                                     tesseract_user_patterns=tesseract_user_patterns):
                    return True
                else:
                    return False
        else:
            if self.is_menu_ocr(perf, text, region_text,
                                threshold, text_color,
                                mode, tesseract_user_patterns,
                                lang,
                                timeout, interval_secs,
                                perf_name):
                return True
            elif self.is_menu_template(perf, path, region_frame,
                                       timeout, match_parameters, perf_name):
                return True
            elif reg_express is not None:
                if self.is_menu_dict(perf,
                                     text=text,
                                     region_text=region_text,
                                     dict_lang=dict_lang,
                                     reg_express=reg_express,
                                     replace=replace,
                                     lang=lang,
                                     mode=mode,
                                     threshold=threshold,
                                     text_color=text_color,
                                     tesseract_user_patterns=tesseract_user_patterns):
                    return True
                else:
                    return False

    def is_menu(self, perf=None,
                perf_name="perf_menu",
                press=None,
                text=None, region_text=None,
                path=None, region_frame=stbt.Region.ALL,
                threshold=None,
                timeout=None,
                interval_secs=None,
                text_color=None,
                mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
                tesseract_user_patterns=None,
                lang=None,
                match_parameters=None,
                timeout_is_menu=None,
                wait_after_press=None,
                dict_lang=None,
                reg_express=None,
                replace=None):

        """
        is_menu: check Menu is displayed  with tow methods
                    ocr : is_menu_ocr
                    template : is_menu_template
        :param perf:Boolean for calculating zap performance between menus
        :param press: key press : ["KEY_PRESS"]
        :param text: reference string used to refer to the menu
        :param region_text: region where to detect the reference text
        :param path: path to the reference template of menu
        :param region_frame: region where to detect the reference template
        :param threshold:The maximum allowed difference between any given
		                    text and ocr text
        :param timeout: Number of seconds that the image was searched for 2 methods
				            ocr and template
        :param interval_secs:The number of seconds to wait for a match before pressing again
        :param text_color: Color of the text. Specifying this can improve OCR results when
                            tesseract's default thresholding algorithm doesn't detect the text,
                            for example for white text on a light-colored background.
        :param mode: Tesseract's layout analysis mode
        :param tesseract_user_patterns: List of patterns to add to the tesseract dictionary.
                        The tesseract pattern language corresponds roughly to the
                        following regular expressions:
                        tesseract  regex
                        =========  ===========
                        \c         [a-zA-Z]
                        \d         [0-9]
                        \n         [a-zA-Z0-9]
                        \p         [:punct:]
                        \a         [a-z]
                        \A         [A-Z]
                        \*         *
        :param lang: The three-letter ISO-639-3 language code of the language you are
                        attempting to read for example eng for English or deu for German.
        :param match_parameters:Customise the image matching algorithm
        :param timeout_is_menu: time out of is_menu function
        :return: true when men menu is displayed, false where not
        """
        if perf is None:
            perf = eval(stbt.get_config("is_menu", "perf"))
        if region_frame is None:
            perf = eval(stbt.get_config("is_menu", "region_frame"))
        if timeout is None:
            timeout = stbt.get_config("is_menu", "timeout", type_=int)
        if interval_secs is None:
            interval_secs = stbt.get_config("is_menu", "interval_secs", type_=int)
        if mode is None:
            mode = eval(stbt.get_config("is_menu", "mode"))
        if lang is None:
            lang = stbt.get_config("is_menu", "language")
        if threshold is None:
            threshold = stbt.get_config("is_menu", "threshold", type_=float)
        if timeout_is_menu is None:
            timeout_is_menu = stbt.get_config("is_menu", "timeout_is_menu", type_=float)
        if wait_after_press is None:
            wait_after_press = stbt.get_config("is_menu", "wait_after_press", type_=int)

        if dict_lang is None:
            dict_lang = stbt.get_config("is_menu", "dictionary_language")


        generic_path = sc_stbt.get_generic_template_path()
        if path is None:
            path = None
        else:
            path = generic_path + path

        assert stbt.wait_until(lambda: self.checkismenu(perf,
                                                        perf_name,
                                                        press, text, region_text,
                                                        path, region_frame,
                                                        threshold,
                                                        text_color,
                                                        mode,
                                                        tesseract_user_patterns,
                                                        lang,
                                                        timeout,
                                                        interval_secs,
                                                        match_parameters,
                                                        wait_after_press,
                                                        dict_lang,
                                                        reg_express,
                                                        replace),
                               timeout_secs=timeout_is_menu,
                               interval_secs=0), ("'%s' NOT FOUND" % (text))
        logging.info("%s FOUND", text)


class navigation(object):
    def find_player(self, selected_image, unselected_image, any_frame):
        """
        Navigates to the specified player.

        Precondition: In the OnDemand Players screen.

        Uses `unselected_image` to find where the player is on screen;
        navigates there;
        uses `selected_image` to know that it has reached the player.
        any_frame is an image cropped such that it will match any player
        """
        #path frames
        path = sc_stbt.get_generic_template_path()
        any_frame = path + any_frame
        selected_image = path + selected_image
        unselected_image = path + unselected_image

        while not stbt.match(selected_image):
            target = stbt.match(unselected_image)
            if stbt.wait_until(lambda: stbt.match(any_frame,
                                                  match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                        confirm_method='none',
                                                                                        match_threshold=0.96,
                                                                                        confirm_threshold=0.3)).match,
                                                  timeout_secs=3):
                source = stbt.match(any_frame,
                                    match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                            confirm_method='none',
                                                                                            match_threshold=0.97,
                                                                                            confirm_threshold=0.3))
                sc_stbt.press(self._next_key(source.position, target.position))
                sc_stbt.wait(3)


                source_after_navigation = stbt.match(any_frame,
                                                    match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                                          confirm_method='none',
                                                                                          match_threshold=0.97,
                                                                                          confirm_threshold=0.3))

                if source_after_navigation.position == source.position:
                    assert False, "NAVIGATION IS NOT DONE"


            else:
                assert False, "CURSOR IS NOT FOUND"



    def _wait_for_selection_to_move(self, source, any_frame):
        """
        Wait for selection to start moving:
        """


        # Wait for selection to stop moving:
        stbt.wait_for_match(any_frame,
                            consecutive_matches=2,
                            match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                  confirm_method='none',
                                                                  match_threshold=0.97, confirm_threshold=0.3))

    def _next_key(self, source, target):
        """
        Returns the key to press to get closer to the target position.
        """
        if self._less(target.x, source.x):
            return "KEY_LEFT"
        if self._less(source.y, target.y):
            return "KEY_DOWN"
        if self._less(target.y, source.y):
            return "KEY_UP"
        if self._less(source.x, target.x):
            return "KEY_RIGHT"

    def _less(self, a, b, tolerance=22):
        """
        An implementation of '<' with a tolerance of what is considered equal.
        """
        return a < (b - tolerance)
