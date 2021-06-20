# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

from __future__ import absolute_import

import stbt
import time
import logging
import os
import csv
import cv2
import inspect
import subprocess
import stbts
import unicodedata
from multiprocessing.pool import ThreadPool

logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO)


def write_csv_file(file_name, rows, mode="a"):
    """

    write_csv_file  append to a csv file the rows passed on params if the file is exist
    and create it if not
    file_name: is the csv file name
    rows is a list of lines (rows) and not just one line
    mode:method of write into the csv file, default mode is append
    Example:
    write_csv_file("csv_file_name.csv", [ ["a", 1], ["b", 2], ["c", 3] ])
    the csv file will contain
    a | 1
    b | 2
    c | 3

    """
    csv_file = open(file_name, mode)
    writer = csv.writer(csv_file)
    writer.writerows(rows)


def detect_many_match(image, timeout_secs=10, match_parameters=None, region=stbt.Region.ALL):
    count = 0
    _exit = False
    # import time
    while (count < len(image) and _exit == False):
        if stbt.detect_match(image[count], timeout_secs=timeout_secs, match_parameters=match_parameters,
                             region=region).next().match:
            _exit = True
        count += 1
        # time.sleep(0.1)
    return _exit


def wait_for_many_match(image, timeout_secs=5, match_parameters=None, region=stbt.Region.ALL):
    _exit = False
    if stbt.wait_until(lambda: detect_many_match(image=image,
                                                 region=region,
                                                 match_parameters=match_parameters,
                                                 timeout_secs=10),
                       timeout_secs=timeout_secs,
                       interval_secs=0):
        _exit = True
        # time.sleep(0.3)
    return _exit


def press_until_many_match(key, image, max_presses=1, interval_secs=3, region=stbt.Region.ALL,match_parameters=None):
    occurence = 0
    _exit = False
    if match_parameters is None:
        match_parameters = stbt.get_config("navigation", "match_param_template")
    while not _exit and (occurence < max_presses):
        press(key)
        wait(interval_secs)
        for i in range(0, len(image)):
            try:
                _exit = stbt.wait_for_match(image=image[i],
                                            timeout_secs=interval_secs,
                                            region=region,
                                            match_parameters=match_parameters).match
                if _exit is True:
                    break
                time.sleep(0.3)
            except:
                pass
        occurence += 1
    return _exit


def wait(interval_secs):
    time.sleep(interval_secs)


def get_all_templates_in_directory(_path):
    result_templates = []
    list_dir = os.listdir(_path)
    for element in list_dir:
        if element.endswith(".png"):
            if _path.endswith("/"):
                result_templates.append(_path + element)
            else:
                result_templates.append(_path + "/" + element)

    return result_templates


def fuzzy_match(string1, string2, threshold=None):
    import difflib
    # logging.info("(found: %s - wanted: %s)", str(string1), str(string2))
    # logging.info(str(difflib.SequenceMatcher(None, string1, string2).ratio()))
    if difflib.SequenceMatcher(None, string1, string2).ratio() >= threshold:
        # stbt.draw_text("FOUND: " + "'" + string1 + "'", duration_secs=4)
        return True
    else:
        # stbt.draw_text("NOT FOUND: " + "'" + string2 + "'", duration_secs=4)
        return False
        # return difflib.SequenceMatcher(None, string1, string2).ratio() >= threshold


def crop(frame, region, file_name):
    frame_region = stbt.Region(x=0, y=0, width=frame.shape[1], height=frame.shape[0])
    region = stbt.Region.intersect(frame_region, region)
    stbt.save_frame(frame[region.y:region.bottom, region.x:region.right], file_name + ".png")


def get_text(region, frame=None, menu_text=None, threshold=None, mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
             tesseract_user_patterns=None, text_color=None, lang="eng"):
    """
    get_text, core, read text with ocr and compared with menu_text
    region: region where to detect the reference text
    Frame: None or disable parameter ==> detect frame automatically in real time

    """
    if threshold is None:
        threshold = stbt.get_config("core", "fuzzy_threshold", type_=float)

    text = stbt.ocr(frame=frame, region=region, mode=mode, lang=lang,
                    tesseract_user_patterns=tesseract_user_patterns, text_color=text_color)
    if menu_text is None:
        return text
    else:
        if not(isinstance(menu_text, str)):
            menu_text = menu_text.encode("utf-8")
        else:
            menu_text  = unicode(menu_text, "utf-8")
        return fuzzy_match(text, menu_text, threshold)


def is_text(region, frame=None, threshold=None, mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
             tesseract_user_patterns=None, text_color=None, lang="eng", timeout=7):
    """
    is_text: get text
    :return: True when text is not empty
    """
    if threshold is None:
        threshold = stbt.get_config("core", "fuzzy_threshold", type_=float)
    start_time = time.time()
    while time.time() - start_time < timeout:
        text = get_text(frame=frame,
                        threshold=threshold,
                        region=region,
                        mode=mode,
                        text_color=text_color,
                        tesseract_user_patterns=tesseract_user_patterns,
                        lang=lang)
        if text != "":
            debug("Text is not empty")
            return text
    assert False, "Empty text"

def ocr_until(region, menu_text, threshold, timeout, interval_secs, text_color=None,
              mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
              tesseract_user_patterns=None, lang="eng", filter=False):
    """
    ocr_until, core, implements get_text until found text or timeout

    region: region where to detect the reference text
    menu_text:  reference string used to refer to the menu

    """
    if filter == True:

        if filter_template(thresh_value=None,
                           callable=lambda: stbt.wait_until(lambda: get_text(region=region,
                                                                             frame=stbt.load_image("end_frame.png"),
                                                                             menu_text=menu_text,
                                                                             threshold=threshold,
                                                                             mode=mode,
                                                                             tesseract_user_patterns=tesseract_user_patterns,
                                                                             text_color=text_color,
                                                                             lang=lang),
                                                            timeout_secs=timeout,
                                                            interval_secs=interval_secs)):
            debug("FOUND: " + "'" +str(menu_text) + "'")
            return True
        else:
            return False
    else:
        frame = None
        if stbt.wait_until(
                lambda: get_text(region, frame, menu_text, threshold, mode, tesseract_user_patterns, text_color, lang),
                timeout_secs=timeout, interval_secs=interval_secs):
            debug("FOUND: " + "'" +str(menu_text) + "'")
            return True
        else:
            debug("NOT FOUND: " + "'" + str(menu_text) + "'")
            return False


def repeat(callable, occurence=None, time_out=1000, tolerance=None, wait_=2):
    """
    repeat, core, repeat a callable

    Repeating a processing of the functions for occurrence times
    time_out: unity time of execution on the function callable
    occurence: numbers of repeat
    tolerance: time added to global time_out
    """

    if occurence is not None:
        time_out = time_out * occurence
        if tolerance is None:
            tolerance = 10 * time_out / 100

    else:
        if tolerance is None:
            tolerance = 0

    start = time.time()
    repeat_test = 0
    while time.time() - start < (time_out + tolerance):
        callable()
        wait(wait_)
        if occurence is not None:
            repeat_test += 1
            if repeat_test == occurence:
                break


def debug(msg=None, text=""):
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    if not( isinstance(msg, str) ):
        msg=msg.encode("utf-8")
    if not( isinstance(text, str) ):
        text=text.encode("utf-8")

    #logging.info("%s: %s", msg, str(text))
    #print "%s" % inspect.stack()[1][3]
    # Dump the message + the name of this function to the log.
    message = msg + text
    logging.info("%s in %s:%i : %s " % (func.co_name, func.co_filename, func.co_firstlineno, message))
    stbt.draw_text(msg + ":" + text, duration_secs=3)






def press(press, delay_sec=2, second_press=None, hold=False):
    """
     Press key using some delay

    """
    from android import press_adb
    quad = eval(stbt.get_config("quad","quad_press"))
    adb  = eval(stbt.get_config("adb","adb_press"))
    automate = eval(stbt.get_config("bluetooth" , "automate"))
    usb_automate = stbt.get_config("bluetooth" , "usb_automate")
    ble_press = eval(stbt.get_config("ble_rcu" , "ble_press"))
    if ble_press :
        blePress(press ,delay_sec, second_press, hold)
    elif adb :
         press_adb(key=press)
    elif quad :
        quad_press(key=press)
    elif automate :
        subprocess.call(get_generic_template_path()+"/../../../trunk/tests/bleutooth/./wakeup_by_RC_multi /dev/ttyUSB"+usb_automate+" "+press+" "+str(delay_sec*10), shell=True)

    else:
        stbt.press(press, interpress_delay_secs=delay_sec)
        logging.info("Pressing %s", str(press))




_dicBlePres= { "KEY_OK" : "101001" , "KEY_POWER" : "110001" , "KEY_1" : "111001" , "KEY_2" : "100001" , "KEY_3" : "101101" , "KEY_4" : "110101",
               "KEY_5" : "111101" , "KEY_6" : "100101" , "KEY_7" : "101011" , "KEY_8" : "110011" ,  "KEY_9" : "111011" ,  "KEY_0" : "100011",
               "KEY_MUTE" : "101111"  , "KEY_UP" : "110111" , "KEY_DOWN" : "111111" , "KEY_RIGHT" : "100111" , "KEY_VOICE" : "201001",
               "KEY_LEFT" : "210001" ,  "KEY_CHANNELUP" : "211001" ,  "KEY_CHANNELDOWN" : "200001" ,  "KEY_VOLUMEDOWN" : "201101",
               "KEY_VOLUMEUP" : "210101", "KEY_BACK" : "211101" , "KEY_STOP" : "200101" , "KEY_PLAY" : "200101" , "KEY_FASTFORWARD" : "201011",
               "KEY_REWIND" : "210011", "KEY_RECORD" : "211011" , "KEY_EXIT" : "200011" , "KEY_RED" : "201111",
               "KEY_GREEN" : "210111" , "KEY_YELLOW" : "211111" , "KEY_BLUE" : "200111", "KEY_MENU" : "301001",
               "KEY_ZOOM" : "310001" , "KEY_VIDEO_NEXT" : "311001" , "KEY_VIDEO_PREV" : "300001"  }


#dictionary for mapping pin-address
#Pins reserved pin1 to pin36
 
 #dic_pin = { "pin1" : "101001" | "pin9" :  "101011" | "pin17" : "201001" | "pin25" : "201011" | "pin33" : "301001" | "pin41" : "301011" |
            # "pin2" : "110001" | "pin10" : "110011" | "pin18" : "210001" | "pin26" : "210011" | "pin34" : "310001" | "pin42" : "310011" |
            # "pin3" : "111001" | "pin11" : "111011" | "pin19" : "211001" | "pin27" : "211011" | "pin35" : "311001" | "pin43" : "311011" |
            # "pin4" : "100001" | "pin12" : "100011" | "pin20" : "200001" | "pin28" : "200011" | "pin36" : "300001" | "pin44" : "300011" |
            # "pin5" : "101101" | "pin13" : "101111" | "pin21" : "201101" | "pin29" : "201111" | "pin37" : "301101" | "pin45" : "301111" |
            # "pin6" : "110101" | "pin14" : "110111" | "pin22" : "210101" | "pin30" : "210111" | "pin38" : "310101" | "pin46" : "310111" |
            # "pin7" : "111101" | "pin15" : "111111" | "pin23" : "211101" | "pin31" : "211111" | "pin39" : "311101" | "pin47" : "311111" |
            # "pin8" : "100101" | "pin16" : "100111" | "pin24" : "200101" | "pin32" : "200111" | "pin40" : "300101" | "pin48" : "300111" }



def setCommand(frame_key, init_frame="000000000000000"):
    """
    setCommand: configure frame key
    :param frame_key: frame key
    :return: new frame configured
    """
    # logging.info("Frame BLE %s", frame_key)

    if frame_key[0]=="1":
        key = frame_key[1:]+ init_frame[5:]

    elif frame_key[0]=="2":
        key = init_frame[:5] + frame_key[1:]+ init_frame[10:]

    elif frame_key[0]=="3":
        key = init_frame[:10] + frame_key[1:]

    else:
        return frame_key
    return key


def blePress(press, delay_sec, second_press, hold):
    """
    blePress: unit function to press with ble rcu
    :param press: keyt press
    :param delay_sec:  delay seconds between press
    :param second_press: the second press
    :param hold: enable hold press
    :return:
    """
    uart = stbt.get_config("ble_rcu", "uart")
    device = stbt.get_config("ble_rcu", "device")

    press_frame_init = _dicBlePres.get(press)
    press_frame = setCommand(press_frame_init)

    if second_press is not None:
        second_press_frame = _dicBlePres.get(second_press)
        second_press_frame = setCommand(second_press_frame)
        press_frame = setCommand(press_frame_init,second_press_frame)

    press_frame = uart + press_frame + "1"

    os.system("stty -F "+device+" 9600 cs8 -cstopb -parenb")

    subprocess.call("echo -e '"+press_frame+"' >"+device+"", shell=True)
    if second_press is not None:
        press = press+"+"+second_press
    logging.info("Pressing BL %s", press)
    stbt.draw_text(press)

    if hold:
        wait(delay_sec)

    subprocess.call("echo -e '00000000000000000' >"+device+"" , shell=True)


def quad_press(key):
    # Take the path of the valid folders
    dir_path = get_generic_template_path()+'/../../../trunk/_sc_stbt/'
    INTERPRESS_DELAY_SECS=0.3
    #Check the STB id on config file
    stb_id=stbt.get_config("quad","stb-id")
    logging.info("Pressing %s", str(press))
    #Printing the remote commands on the fifo file
    with open(dir_path + '/ir_commands', 'w') as fifo:
        ir_commands = "{} ".format(stb_id) + key + "\n"
        print ("Sending : " + ir_commands)
        fifo.write(ir_commands)
        fifo.flush()
        fifo.close()
        time.sleep(INTERPRESS_DELAY_SECS)
        stbt.draw_text(key)
        logging.info("Pressing %s", str(key))
        


def combo_press(combo=None, delay_sec=2, number_press=None):
    """
    combo_press ; press combo list press
    """
    if number_press is None:
        for i in range(0, len(combo)):
            press(combo[i], delay_sec=delay_sec)
    else:
        for j in range(number_press):
            for i in range(0, len(combo)):
                press(combo[i], delay_sec=delay_sec)


def get_generic_template_path():
    path = os.environ.get('STBT_PROJECT_PATH')
    return path


def write_statut_test(statut):
    """

    :return:
    """
    import os
    config_file = os.environ.get('STBT_CONFIG_FILE_CUSTOM')

    command = "sed -i -e 's,^'state' =.*,'state' = '" + statut + "',' " + config_file

    os.system(command)


def get_statut_test(message):
    """

    :return:
    """
    state = stbt.get_config("global", "state")
    if state == "test_ko":
        assert False, 'TEST IS BLOCKED: %s' % message


def write_statut_boot_test(statut):
    """

    :return:
    """
    import os
    config_file = os.environ.get('STBT_CONFIG_FILE_CUSTOM')

    command = "sed -i -e 's,^'boot_state' =.*,'boot_state' = '" + statut + "',' " + config_file

    os.system(command)


def get_statut_boot_test(message):
    """

    :return:
    """
    state = stbt.get_config("global", "boot_state")
    if state == "test_ko":
        assert False, 'TEST IS BLOCKED: %s' % message

list_timer = []


def timer(region_current_timer,
          region_end_timer,
          timer_value=False,
          press="KEY_UP",
          wait_after_press=1):
    """

    :param timer_value:
    :return:
    """
    import re
    global list_timer
    check_current_time = None
    check_end_time = None
    check_end_time2 = None
    list_timer.__init__()
    current_time = ''
    end_time = ''
    start_time = time.time()
    while (check_current_time is None and (
            check_end_time is None or check_end_time2 is None)) and time.time() - start_time < 5:
        # Read current time & end time
        current_time = get_text(region=region_current_timer,
                                mode=stbt.OcrMode.SINGLE_WORD,
                                tesseract_user_patterns=[r'\d\d\d\d\d']).replace(" ", "")
        end_time = get_text(region=region_end_timer,
                            mode=stbt.OcrMode.SINGLE_WORD,
                            tesseract_user_patterns=[r'\d\d\d\d\d']).replace(" ", "")

        # delete all caracteres only 0-9
        current_time = re.sub(r"[^0-9:]+", '', current_time)
        end_time = re.sub(r"[^0-9:]+", '', end_time)
        # check if current_time and end_time content a  right time format

        check_current_time = re.match(r"\d?\:?\d+\d?:\d+\d+", current_time)
        check_end_time = re.match(r"\d+\d?\:+\d+\d?", end_time)
        check_end_time2 = re.match(r"\d+\:+\d+\d?\:+\d+\d?", end_time)

    if (check_current_time is not None) or (check_end_time is not None or check_end_time2 is not None):
        # debug("CURRENT TIME",current_time)
        # debug("END_TIME",end_time)
        if timer_value:
            list_timer.append(current_time)
            list_timer.append(end_time)
        return True
    else:
        import sc_stbt
        if press is None:
            return False
        else:
            sc_stbt.press(press)
            wait(wait_after_press)
            return False


def get_timer_value(region_current_timer,
                    region_end_timer,
                    timer_value=True,
                    press="KEY_UP",
                    wait_after_press=1):
    """
    get_timer_value: get timer
    :return:
    """
    if timer(region_current_timer=region_current_timer,
             region_end_timer=region_end_timer,
             timer_value=timer_value,
             press=press,
             wait_after_press=wait_after_press):
        return list_timer
    else:
        assert False, "timer not detected"


def filter_template(thresh_value=None, callable=None):
    """

    :return:
    """
    stbt.save_frame(stbt.get_frame(), 'start_frame.png')
    img = cv2.imread('start_frame.png', 0)
    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(img)
    cv2.imwrite('clahe.png', cl1)

    # binarisation
    im_gray = cv2.imread('clahe.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    debug("Thresh detected:", str(thresh))
    if thresh_value is not None:
        thresh_compter = thresh_value
    else:
        thresh_compter = thresh
    if callable is None:
        debug("callable none")
        im_bw_1 = cv2.threshold(im_gray, thresh_compter, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite('end_frame.png', im_bw_1)
        debug("save end_frame with filter")
        return True
    else:
        while thresh_compter < 255:
            im_bw_1 = cv2.threshold(im_gray, thresh_compter, 255, cv2.THRESH_BINARY)[1]
            # cv2.imwrite('end_frame.png',im_bw_1)
            stbt.save_frame(im_bw_1, 'end_frame.png')
            thresh_compter += 10
            debug("Thresh", str(thresh_compter))
            if callable():
                return True
    return False


def write_technical_information(callable):
    """
    write_technical_information: this function write in file.txt the technical information
    :param callable: it is a function wish return two parametres: UI and MW
    :return: True if
    """
    ui_version, mw_version = callable()
    if ui_version and mw_version is not None:
        file = open('technical_information.txt', 'a')
        printinfo = "UI:" + ui_version + '\n' "MW:" + mw_version + '\n'
        file.write(printinfo.encode('utf8'))
        file.close()
        return True
    else:
        return False


def convert_mask_to_regions(path_mask):
    """
    Function: convert a mask to list of regions
    :param path_mask:
    :return: list of regions if mask contain white spaces
             None if passed mask is black screen
    """
    mask = cv2.imread(path_mask, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    regions_list = []
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 0:
            [x, y, width, height] = cv2.boundingRect(contour)
            region = stbt.Region(x=x, y=y, width=width, height=height)
            regions_list.append(region)

    if regions_list:
        return regions_list
    else:
        return None


def play_voice_command(command = None, android_ = None):
    """
    play_voice_command
    :return:
    """
    if android_ is None :

       android_ = eval(stbt.get_config("voice","android"))

    if android_ :
       voice_path= get_generic_template_path() + "/../../../android/tests/templates"
    else :
       voice_path= get_generic_template_path()

    command_=command.replace(" ","_")
    voice_path=(voice_path+"/../voice_templates/"+command_+".mp3")
    empty_path=(get_generic_template_path() + "/../../../android/tests/voice_templates/empty.mp3")
    # os.system("cvlc --play-and-exit "+empty_path)   #old api take much time in execution
    # os.system("cvlc --play-and-exit "+voice_path)   #old api take much time in execution
    os.system("mpg123  "+empty_path) #new api take less time in execution
    os.system("mpg123  "+voice_path) #new api take less time in execution

def press_voice_command(device=None, android_=True, port_voice=None ,press_time=None):
    """
    press_voice_command
    :param device:
    :param android_:
    :param port_voice:
    :param press_time:
    :return:
    """

    from android import remote_ATV_press,press_adb

    if port_voice is None :
       port_voice = stbt.get_config("voice", "port_voice")
    if press_time is None :
       press_time = stbt.get_config("voice", "press_time")

    debug("waiting for key voice")
    if device is None :
        usb_automate = stbt.get_config("bluetooth", "usb_automate")
        subprocess.call(get_generic_template_path()+"/../../../android/tests/bluetooth/./wakeup_by_RC_multi /dev/ttyUSB"+usb_automate+" "+port_voice+" "+press_time, shell=True)
    else :
        remote_ATV_press("KEY_VOICE")

    if android_ :
        if wait_for_many_match(get_all_templates_in_directory(get_generic_template_path()+ "/../../../android/tests/templates/voice/" ),
                                                 region=eval(stbt.get_config("voice","logo_voice")),
                                                 timeout_secs=10):
            debug("Key voice pressed")
        else :
            assert False , "No Key Voice"
    else:
        if wait_for_many_match(get_all_templates_in_directory(get_generic_template_path()+ "/voice/" ),
                                                 region=eval(stbt.get_config("voice","logo_voice")),
                                                 timeout_secs=10):
            debug("Key voice pressed")
        else :
            assert False , "No Key Voice"




def voice_command(callable=None, command=None, device=None, port_voice=None, press_time=None, android_= None,wait_ = 5,threshold = 0.8):
    """
    Press on KEY_VOICE and command the box then check if the callable is done
    :return: True when the command is excecuted , False if not
    """
    press_voice_command(device ,android_ , port_voice , press_time)
    wait(1)
    play_voice_command(command , android_)

    if stbts.match_text(text=command,region=eval(stbt.get_config("voice","region_command")) ,threshold=threshold, timeout_secs=5):
        debug("Your command is "+ command)
    else:
        assert False, "Your request is not considered"
    wait(wait_)
    if callable is None :
        pass
    else :
        if callable():
            return True, " OK  voice command executed "
        else:
            assert False ," FAIL  voice command NOT executed "



def multi_threading(callable_1, callable_2, callable_3=None, callable_4=None):
    """
    multi_threading:  run 4 API in parallel
    :param callable_1: API 1
    :param callable_2: API 2
    :param callable_3: API 3
    :param callable_4: API 4
    :return:
    """
    if callable_3 is None and callable_4 is None:
        pool = ThreadPool(processes=2)
        pool.map(apply, [callable_1, callable_2])
        pool.terminate()

    if (callable_3 is not None or callable_4 is not None) and (callable_3 is None or callable_4 is None):
        pool = ThreadPool(processes=3)
        pool.map(apply, [callable_1, callable_2, callable_3])
        pool.terminate()


    if callable_3 is not None and callable_4 is not None:
        pool = ThreadPool(processes=4)
        pool.map(apply, [callable_1, callable_2, callable_3, callable_4])
        pool.terminate()
