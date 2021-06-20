from __future__ import absolute_import

import time
import logging
import os
import csv
import cv2
import inspect
import difflib
import stbt
import sc_stbt


_debug_level = None

def get_debug_level():
    global _debug_level
    if _debug_level is None:
        _debug_level = stbt.get_config('global', 'verbose', type_=int)
    return _debug_level


def info(s, draw_secs=3):
    """ Get the previous frame in the stack,
        otherwise it would be this function!!!
        Print the given string if `--verbose` was given.
    """

    if get_debug_level() > 0:
        func = inspect.currentframe().f_back.f_code
        logging.info("%s in %s:%i : %s " % (func.co_name,
                                            func.co_filename, func.co_firstlineno, s))
        stbt.draw_text(s, duration_secs=draw_secs)


def ddebug(s):
    """ Get the previous frame in the stack,
        otherwise it would be this function!!!
        Print the given string if `--verbose` was given.
        Extra verbose debug for stbt developers, not end users
    """

    if get_debug_level() > 1:
        func = inspect.currentframe().f_back.f_code
        logging.info("%s in %s:%i : %s " % (func.co_name,
                                            func.co_filename, func.co_firstlineno, s))


def any_match(path, region=stbt.Region.ALL, match_parameters=None):
    """ match any images inside selected path
    return: MatchResult stbt class
    """
    limages = sc_stbt.get_all_templates_in_directory(path)
    count = 0
    results = False
    while count < len(limages):
        results = stbt.match(limages[count], region=region, match_parameters=match_parameters)
        if results.match:
            return results
        # move to next image
        count += 1
    return results


def wait_any_match(path, region=stbt.Region.ALL, match_parameters=None, stable_secs=0, timeout_secs=10):
    return stbt.wait_until(lambda: any_match(path, region=region, match_parameters=match_parameters),
                           predicate=lambda x: x.match,
                           stable_secs=stable_secs,
                           timeout_secs=timeout_secs)


def get_gray_threshold(frame=None):
    if frame is None:
        stbt.save_frame(stbt.get_frame(), 'get_threshold.png')
        frame = cv2.imread('get_threshold.png', 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(frame)
    logging.info("Store clahe.png")
    cv2.imwrite('clahe.png', cl1)
    # binarisation
    im_gray = cv2.imread('clahe.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    ddebug("Threshold=%s " % str(thresh))
    return thresh


def get_blackscreen_threshold(frame=None, mask=None):
    thresh = 0
    while not stbt.is_screen_black(frame, mask=mask, threshold=thresh) and thresh < 250:
        thresh += 5
        ddebug("Black screen is not detected %s" % str(thresh))
    ddebug("Black screen is detected %s" % str(thresh))
    return thresh


# sc_stbt.match_text(text="4.0.3701.02kt(nzdev)", frame=frame, region=voda_mw, mode=stbt.OcrMode.SINGLE_WORD, timeout_secs=1)
def wait_for_match_text(text, frame=None, region=stbt.Region.ALL,
                        mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD, lang="eng",
                        tesseract_config=None, case_sensitive=False,
                        text_color=None, threshold=1, stable_secs=0, timeout_secs=5):
    return stbt.wait_until(lambda: stbt.match_text(text=text,
                                                   frame=frame,
                                                   region=region,
                                                   mode=mode,
                                                   lang=lang,
                                                   tesseract_config=tesseract_config,
                                                   case_sensitive=case_sensitive,
                                                   text_color=text_color,
                                                   threshold=threshold),
                           predicate=lambda x: x.match,
                           stable_secs=stable_secs,
                           timeout_secs=timeout_secs)




def match_text(text, frame=None, region=stbt.Region.ALL,
               mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD, lang="eng",
               tesseract_config=None, case_sensitive=False,
               text_color=None, threshold=1, stable_secs=0, timeout_secs=5):
    """
        1- use default match_text
        2- use scale gray
        3- use binarization based on OTSU ALGO
    """
    result = wait_for_match_text(text=text, frame=frame, region=region, mode=mode,
                                 lang=lang, tesseract_config=tesseract_config,
                                 case_sensitive=case_sensitive, text_color=text_color,
                                 threshold=threshold, stable_secs=0, timeout_secs=timeout_secs)
    ocr = stbt.ocr(frame, region, lang=lang, mode=mode, tesseract_user_words=[text])
    ratio = difflib.SequenceMatcher(None, ocr, text).ratio()

    if not result.match and ratio > 0.5:
        # Try with gray scale
        ddebug("Convert frame BGR2GRAY")
        if frame is None:
            frame = stbt.get_frame()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = wait_for_match_text(text=text, frame=gray_frame, region=region, mode=mode,
                                     lang=lang, tesseract_config=tesseract_config,
                                     case_sensitive=case_sensitive,
                                     threshold=threshold, timeout_secs=timeout_secs)
        stbt.ocr(frame, region, lang=lang, mode=mode, tesseract_user_words=[text])
        if not result.match:
            ddebug("Convert frame GRAY2BICOLOR")
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl1 = clahe.apply(gray_frame)
            thresh = cv2.threshold(cl1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[0]
            bin_frame = cv2.threshold(cl1, thresh, 255, cv2.THRESH_BINARY)[1]
            # stbt.save_frame(bin_frame,str(thresh)+'frame.png')
            ocr = stbt.ocr(bin_frame, region, lang=lang, mode=mode, tesseract_user_words=[text])
            ratio = difflib.SequenceMatcher(None, ocr, text).ratio()
            # print ratio
            while ratio > 0.5:
                result = wait_for_match_text(text=text, frame=bin_frame, region=region, mode=mode,
                                             lang=lang, tesseract_config=tesseract_config,
                                             case_sensitive=case_sensitive,
                                             threshold=threshold, timeout_secs=timeout_secs)
                stbt.save_frame(bin_frame, 'frame.png')
                if not result.match:
                    thresh += 10
                    ddebug("Threshold: %s" % str(thresh))
                    bin_frame = cv2.threshold(cl1, thresh, 255, cv2.THRESH_BINARY)[1]
                    ocr = stbt.ocr(bin_frame, region, lang=lang, mode=mode, tesseract_user_words=[text])
                    ratio = difflib.SequenceMatcher(None, ocr, text).ratio()
                    ddebug(ratio)
                    # stbt.save_frame(bin_frame, str(thresh)+'frame.png')
                else:
                    break
    return result

def _press(key, interpress_delay_secs=None):
    """ Press key using interpress_delay_secs is a dely before press
        return: time
    """

    sc_stbt.press(key, delay_sec=interpress_delay_secs)
    start_time = time.time()
    logging.info(key)
    return start_time