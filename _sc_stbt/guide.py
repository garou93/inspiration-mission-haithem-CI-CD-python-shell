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



class guide(object):
    def epg_scroll_ocr(self, press, region, text, lang, timeout, wait, threshold=0.8):
        """
        epg_scroll_ocr, guide, check whether the scroll was done

        after scroll , record a present event and service name  and compare them
        press; key_press
        path: path to the reference template of menu
        text: reference string used to refer event and service name
        lang: lang text menu
        timeout: duration of epg_scroll_ocr
        region: region where to detect the reference text

        """
        start_time = time.time()
        result = False
        while time.time() - start_time < timeout and result == False:
            sc_stbt.press(press)
            sc_stbt.wait(wait)
            if stbt.wait_until(
                lambda: not sc_stbt.fuzzy_match(stbt.ocr(region=region,lang=lang), str(text), threshold),
                                                    timeout_secs=8,
                                                    interval_secs=0):
                    result = True
        assert result == True, ("%s :NO SCROLL DONE" % text)


    def epg_scroll(self, press, region, lang, timeout, wait):
        """
        epg_scroll, guide, scroll in all directions in guide menu

        record a present event and service with ocr and scoll
        press; key_press
        path: path to the reference template of menu
        wait: time between press
        lang: lang text menu
        timeout: duration of epg_scroll_ocr
        region: region where to detect the reference text

        """
        text = stbt.ocr(frame=stbt.get_frame(), region=region, lang=lang)
        text = text.encode('utf8')
        str(text)
        self.epg_scroll_ocr(press, region, text, lang, timeout, wait)


    def crop_press (self, press, region_found):
        """
        crop_press, guide,crop a frame and press key

        crop a frame with a specific region and press key
        press; key_press
        region_found: region of frame croped

        """
        sc_stbt.wait(2)
        sc_stbt.crop(stbt.get_frame(),
                     region=region_found,
                     file_name="frame")
        sc_stbt.press(press)


    def noeffect_in_press(self, press, region, region_found):
        """
        noeffecti_in_press, guide, check if a press has an effect

        crop a frame and then press
        a key and check if the frame has changed
        press; key_press
        region_found: region of frame croped
        region: region of research

        """
        self.crop_press(press, region_found)
        sc_stbt.wait(5)
        assert stbt.wait_until(lambda: stbt.match("frame.png",
                                                  region=region),
                               timeout_secs=10), ("CANT MATCH CROPED FRAME")

