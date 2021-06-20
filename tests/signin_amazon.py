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
import stbts
import stbt
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

project = os.environ.get('STBT_PROJECT')
amazon_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/templates_amazon/"
any_frame = amazon_path_template + "/sign_in/any_frame/any_frame.png"
amazon_path_template_is_menu = "/../../../trunk/tests/templates/templates_amazon/"

menu = sc_stbt.menu()
amazon_keyboard = sc_stbt.amazon_keyboard()


def is_amazon_signin():
    """
    is_amazon_signin:: check if the sign in page is displayed
    :return:
    """
    if stbts.match_text("prime video",
                        region=stbt.Region(x=47, y=39, width=190, height=38),
                        timeout_secs=30).match:
        sc_stbt.debug("AMAZON APP IS DISPLAYED")
        return True
    else :
        sc_stbt.debug("AMAZON APP IS NOT DISPLAYED")
        return False


def sign_in_amazon(callable=None):
    """
    this function is used to sign in amazon
    :return:
    """
    login = stbt.get_config("amazon", "login")
    password = stbt.get_config("amazon", "password")

    if is_amazon_signin():
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)
        if stbts.match_any_text(text=['Sign', 'Connectez', 'Identificate'],
                            region=stbt.Region(x=32, y=41, width=116, height=32)).match:
            sc_stbt.debug("MENU SIGNIN IS DISPLAYED")
    if stbts.match_text(text="Search",region=stbt.Region(x=44, y=36, width=58, height=20)).match:
        sc_stbt.debug("AMAZON ALREADY SIGNIN")
    else:
        if not menu.is_menu_template(perf=False,
                                     region_frame=stbt.Region(x=644, y=163, width=40, height=47),
                                     path=amazon_path_template + "sign_in/cursor/",
                                     timeout=3):
            list = ["KEY_UP", "KEY_UP", "KEY_UP", "KEY_OK"]
            sc_stbt.combo_press(list)
        else:
            sc_stbt.press("KEY_OK")
        check_keyboard()
        # enter login
        sc_stbt.wait(3)
        amazon_keyboard.enter_text(login)

        if menu.is_menu_template(perf=False,
                                 region_frame=stbt.Region(x=644, y=232, width=40, height=47),
                                 path=amazon_path_template + "sign_in/cursor/",
                                 timeout=3):
            if stbts.match_text(login,
                                region=stbt.Region(x=298, y=176, width=350, height=22),
                                threshold=0.8,
                                timeout_secs=5).match:
                sc_stbt.press("KEY_OK")
                check_keyboard()
                sc_stbt.wait(3)

            else:
                sc_stbt.debug("verify your email")

        amazon_keyboard.enter_text(password)
        sc_stbt.wait(2)
        if menu.is_menu_template(perf=False,
                                 region_frame=stbt.Region(x=286, y=272, width=392, height=31),
                                 path=amazon_path_template + "sign_in/cursor",
                                 timeout=3):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(10)
            if stbts.match_text("Success!",
                                region=stbt.Region(x=252, y=179, width=450, height=88),
                                threshold=0.9,
                                timeout_secs=5).match:
                sc_stbt.debug("Success! Your device is registred")
                if sc_stbt.is_amazon(press="KEY_OK"):
                    sc_stbt.debug("login succeeded")
                else:
                    sc_stbt.debug("verify your password")
            else :
                if sc_stbt.is_amazon(press="KEY_BACK"):
                    sc_stbt.debug("login succeeded")
                else:
                    sc_stbt.debug("verify your password")

def check_keyboard():
    """
    this function is used to identify the keyboard (email keyboard or password keyboard)
    :return:
    """
    if menu.is_menu_template(perf=False,
                        region_frame=stbt.Region(x=265, y=232, width=29, height=30),
                        path=amazon_path_template + "sign_in/keyboard/",
                        timeout=10):
        sc_stbt.debug("keyboard is displayed")

    elif menu.is_menu_template(perf=False,
                        region_frame =stbt.Region(x=659, y=173, width=9, height=26),
                        path=amazon_path_template + "sign_in/cursor/",
                        timeout=10):
            sc_stbt.press("KEY_OK")
            sc_stbt.debug("keyboard is displayed")
    else:
        assert False, "Keyboard is not Displayed"

def write_text(text, callable):
    """
    write_text: this function is used to write text in input by keyboard
    :param text:
    :return:
    """
    special = 0
    for i in range(len(text)):
        if i == 0:
            if (text[i]).isupper():
                goto_cord('*',callable)
            if not ((text[i]).isalpha() or (text[i]).isalnum()):
                special = 1
                goto_cord('&')
            goto_cord(text[i].lower(), callable)
        if i != 0:
            if not ((text[i]).isalpha() or (text[i]).isalnum()):
                special = 1
            goto_cord(text[i].lower(),callable)

        if i < len(text) - 1:
            if special == 1:
                if (text[i + 1]).isalpha() or (text[i + 1]).isalnum():
                    special = 0
                    goto_cord('*')
                    if (text[i + 1]).isupper():
                        goto_cord('*')
            if (text[i]).isalnum():
                if (text[i + 1]).isupper():
                    goto_cord('*')

            if (text[i]).isupper() and ((text[i + 1]).islower() or (text[i + 1]).isalnum()):
                goto_cord('*')

            if not ((text[i + 1]).isalpha() or (text[i + 1]).isalnum()):
                goto_cord('&')


def goto_cord(char, callable = None):
    """

    :param char:
    :return:
    """
    target = matrix_amazon[char]
    if callable is not None :
        final_dict = callable()
        target = final_dict[char]

    target_x = target[0]
    target_y = target[1]

    source = stbt.match(any_frame).position
    source_x = source.x
    source_y = source.y

    global tolerance
    tolerance = 18
    start_time = time.time()
    while time.time() - start_time < 300:
        if source_x in range((target_x - tolerance), (target_x + tolerance)) and source_y in range(
                (target_y - tolerance), (target_y + tolerance)):
            sc_stbt.press("KEY_OK")
            sc_stbt.wait(1)
            return True
        else:
            sc_stbt.press(_next_key(source_x, source_y, target_x, target_y, tolerance))
            sc_stbt.wait(1)
            source = stbt.match(any_frame).position
            source_x = source.x
            source_y = source.y



def _next_key(source_x, source_y, target_x, target_y, tolerance):
    if (source_y < target_y - tolerance):
        return "KEY_DOWN"
    if (source_y - tolerance > target_y):
        return "KEY_UP"
    if (source_x < target_x - tolerance):
        return "KEY_RIGHT"
    if (source_x - tolerance > target_x):
        return "KEY_LEFT"


########################################"SIGN IN WITH AMAZON WEBSITE ####################################
def open_amazon_website():
    """
    OPEn the amazon website (www.amazon.com)
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
    browser.get("https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&switch_account=")
    browser.save_screenshot('screenshot_web.png')
    try:
            ui.WebDriverWait(browser, 20).until(EC.title_is("Amazon Sign-In"))
            browser.save_screenshot('screenshot_web.png')
            sc_stbt.debug("Sign In Window is Displayed")
    except:
            browser.save_screenshot('screenshot_web.png')
            browser.quit()
            assert False, "Sign In Window is not Displayed"

def sign_in_website():
    """
    sign_in_amazon_website ::  get the username and the password from the config file and registre in the amazon website
    :return:
    """
    username= stbt.get_config("amazon","login")
    password= stbt.get_config("amazon","password")

    browser.save_screenshot('screenshot_web.png')
    browser.find_element_by_name("email").send_keys(username)
    inputElement = browser.find_element_by_css_selector('.a-button-input')
    inputElement.click()
    browser.save_screenshot('screenshot_web.png')
    browser.find_element_by_name("password").send_keys(password)
    ui.WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,"#signInSubmit"))).click()
    browser.save_screenshot('screenshot_web.png')
    try:
            ui.WebDriverWait(browser, 20).until(EC.title_is("Amazon.com: Online Shopping for Electronics, Apparel, Computers, Books, DVDs & more"))
            browser.save_screenshot('screenshot_web.png')
            sc_stbt.debug("LOGIN successful")
    except:
            browser.save_screenshot('screenshot_web.png')
            browser.quit()
            assert False, "LOGIN Failed"

def register_device_window():
    """
    go_to_your_prime_video :: API that Take u from the Amazon website to Ur Prime VIdeo Account after Sign in
    :return:
    """
    browser.get("https://www.amazon.com/gp/video/ontv/code/ref=atv_set_rd_reg")
    browser.save_screenshot('screenshot_web.png')
    try:
            ui.WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#av-cbl-code")))
            browser.save_screenshot('screenshot_web.png')
            sc_stbt.debug("Register STB by code")
    except:
            browser.save_screenshot('screenshot_web.png')
            assert False, "menu register with code is not displayed "


def generate_signin_code(lang="fra"):
    """
    signin_stb_with_website : Api that select the website signin methode in STB menu
    :param lang:
    :return:
    """
    if is_amazon_signin():
        menu.is_menu(press=["KEY_DOWN"],
                         path= amazon_path_template_is_menu + "/Settings/register_on_the_amazon_website/",
                         region_frame=stbt.Region(x=59, y=400, width=299, height=45),
                         timeout=4,
                         timeout_is_menu=8)
        if lang =="eng":
            menu.is_menu(press=["KEY_OK"],
                         text="Register Your Device",
                         region_text=stbt.Region(x=33, y=37, width=201, height=40),
                         timeout=4,
                         timeout_is_menu=8)
            sc_stbt.debug("MENU SIGNIN IS DISPLAYED")
        elif lang =="fra":
            menu.is_menu(press=["KEY_OK"],
                     text="Enregistrez votre appareil",
                     region_text=stbt.Region(x=33, y=37, width=254, height=40),
                     timeout=4,
                     timeout_is_menu=8)
            sc_stbt.debug("MENU enregistement est affiche")
        else:
            assert False , ("lang selected is not supported")
        sc_stbt.wait(5)
    else:
        assert False, ("MENU SIGNIN NOT DISPLAYED")

def get_code_stb_to_website():
    """
    get_code_stb_to_website :: API that grep the code from Stb and set it in the amazon website than it press on signin button to confirm registration
    :return:
    """
    code = sc_stbt.get_signin_code()
    element = browser.find_element_by_css_selector("#av-cbl-code")
    element.send_keys(code)
    browser.save_screenshot('screenshot_web.png')
    ui.WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"._2V-I1s"))).click()
    browser.save_screenshot('screenshot_web.png')
    signin = False

    while not signin :
        try :
            ui.WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"._2yAJYN > span:nth-child(2)")))
            browser.save_screenshot('screenshot_web.png')
            sc_stbt.debug("That's an invalid code")
            sc_stbt.get_new_signin_code()
            code1 = sc_stbt.get_signin_code()
            open_amazon_website()
            sign_in_website()
            register_device_window()
            browser.save_screenshot('screenshot_web.png')
            browser.find_element_by_css_selector("#av-cbl-code").send_keys(code1)
            browser.save_screenshot('screenshot_web.png')
            sc_stbt.wait(2)
            ui.WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"._2V-I1s"))).click()
            browser.save_screenshot('screenshot_web.png')
            signin = False
        except:

            sc_stbt.debug("Success! Your device is registered to your Prime Video account")
            if stbts.match_text(text="Success!",
                        region=stbt.Region(x=318, y=155, width=85, height=36),
                        threshold=0.8,
                        timeout_secs=5).match:
                sc_stbt.press("KEY_OK")
                sc_stbt.is_amazon()
            else :
                assert False, "Problem Occurred"
            signin = True

def close_interface():
    """
    close_interface :: quit the web interface
    :return:
    """
    browser.quit()

def signin_by_web():

    generate_signin_code(lang="fra")
    open_amazon_website()
    sign_in_website()
    register_device_window()
    get_code_stb_to_website()
    close_interface()


matrix_amazon = {}
#1234567890
matrix_amazon["1"] = [264, 231]
matrix_amazon["2"] = [300, 231]
matrix_amazon["3"] = [336, 231]
matrix_amazon["4"] = [372, 231]
matrix_amazon["5"] = [408, 231]
matrix_amazon["6"] = [444, 231]
matrix_amazon["7"] = [480, 231]
matrix_amazon["8"] = [516, 231]
matrix_amazon["9"] = [552, 231]
matrix_amazon["0"] = [588, 231]
#qwertyuiop
matrix_amazon["q"] = [264, 267]
matrix_amazon["w"] = [300, 267]
matrix_amazon["e"] = [336, 267]
matrix_amazon["r"] = [372, 267]
matrix_amazon["t"] = [408, 267]
matrix_amazon["y"] = [444, 267]
matrix_amazon["u"] = [480, 267]
matrix_amazon["i"] = [516, 267]
matrix_amazon["o"] = [552, 267]
matrix_amazon["p"] = [588, 267]
#asdfghjkl
matrix_amazon["a"] = [264, 303]
matrix_amazon["s"] = [300, 303]
matrix_amazon["d"] = [336, 303]
matrix_amazon["f"] = [372, 303]
matrix_amazon["g"] = [408, 303]
matrix_amazon["h"] = [444, 303]
matrix_amazon["j"] = [480, 303]
matrix_amazon["k"] = [516, 303]
matrix_amazon["l"] = [552, 303]
#zxcvbnm
matrix_amazon["z"] = [264, 339]
matrix_amazon["x"] = [300, 339]
matrix_amazon["c"] = [336, 339]
matrix_amazon["v"] = [372, 339]
matrix_amazon["b"] = [408, 339]
matrix_amazon["n"] = [444, 339]
matrix_amazon["m"] = [480, 339]
# ABC
matrix_amazon["*"] = [624, 267]
# space
matrix_amazon["#"] = [336, 375]
# Entrer
matrix_amazon["/"] = [624, 375]
# char special
matrix_amazon["&"] = [624, 339]
# -$$=_.@+
matrix_amazon["-"] = [408, 267]
matrix_amazon["$"] = [372, 231]
matrix_amazon["="] = [552, 267]
matrix_amazon["_"] = [480, 303]
matrix_amazon["."] = [444, 267]
matrix_amazon["@"] = [300, 303]
matrix_amazon["+"] = [588, 231]

