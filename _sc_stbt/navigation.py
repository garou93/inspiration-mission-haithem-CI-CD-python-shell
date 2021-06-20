# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import time
import stbt
import stbts
import sc_stbt


class parameters():
    """
    A class parameter defines all values that is used for  object generator
    """

    def __init__(self, step_x, step_y, x_init, y_init, menu):
        """
        Constructor
        attributes :
		step_x= width of (item/button) + tolerance
		step_y= height of (item/button) + tolerance
		x_init and y_init : initial position of item or button in menu
		menu : list of items in menu/keyboard
        """
        self.step_x = step_x
        self.step_y = step_y
        self.x_init = x_init
        self.y_init = y_init
        self.menu = menu


# -------------------------Object of type generator-----------------------------------------------------------------------------------

# if portal not clear, we can not use "ocr mode"  to read target_text
# to get position x and y of target so we can use this object
# to generate all positions (x,y) of menu/keyboard item


def generate_position(parameters):
    """
    generate_position : browse  the menu to calculate for each menu item  the position x and y
    :param parameters:
	:return: text, pos_x and pos_y using the keyword" yield "

    """
    # x = colo,  y = line
    for x in range(len(parameters.menu[0])):
        for y in range(len(parameters.menu)):
            text = parameters.menu[y][x]
            yield (text, (parameters.x_init + (parameters.step_x) * x), (parameters.y_init + (parameters.step_y) * y))


# -------------------------------------------------------------------------------------------------------------------------------------

class target(object):
    def __init__(self, x=0, y=0, region_target=None, text_color=None):
        """
        Constructor of class target
        Attributes:
        :param x: position: x of target
        :param y: position: y of target
        :param region_target:
        :param text_color:
        """
        self.x = x
        self.y = y

        # use the followings attributes when you can read target_text with ocr
        # so you need to define a specific region and more then that text_color
        self.region_target = region_target
        self.text_color = text_color

    # use this function when you can't read your target_text with ocr_mode
    # so you must get positions of target with generator
    def search_position(self, item, parameters):
        """
        search_position : recuperate an object of type target(x,y)
		with creation of generator

        :param item: looking for
        :param parameters: defines all necessary parameters to generate positions of items in menu
        :return: an object of type target
        """
        targ = target()
        gener = generate_position(parameters)
        for text, pos_x, pos_y in gener:
            # print ("text=%c \t position_x=%d  \t position_y=%d \n", text, pos_x, pos_y)
            if text == item:
                targ.x = pos_x
                targ.y = pos_y
                return targ

    # use this function when you can read your target_text with ocr_mode
    def select_target(self, text_target, gototarget):
        """
        select_target: navigate to an item exist menu/keyboard then select it
        :param text_target: target looking for
        :param gototarget: constructor
        :return: False: when item not selected
               else True
        """
        start_time = time.time()
        target = stbt.match_text(text=text_target,
                                 region=self.region_target,
                                 text_color=self.text_color)
        # search the position of target with match_text
        while (time.time() - start_time < 200) and target.match == False:
            target = stbt.match_text(text=text_target,
                                     region=self.region_target,
                                     text_color=self.text_color)
        assert target.match, ("%s IS NOT FOUND" % (text_target))
        sc_stbt.debug(text_target + " " + "IS FOUND")
        assert gototarget.go_to_target(target.region), ("'%s'IS NOT SELECTED" % (text_target))


class gototarget(object):
    def __init__(self, cursor_template, region_cursor, tolerance_x=8, tolerance_y=8, match_param_cursor=None):
        """
        Constructor of class gototarget
        Attributes:
        :param cursor_template: template of navigation cursor to get current position of source
        :param region_cursor:specific region to search cursor_template
        :param tolerance_x:  tolerance of position x
        :param tolerance_y: tolerance of position y
        :param match_param_cursor:
        """
        self.cursor_template = cursor_template
        self.region_cursor = region_cursor
        self.tolerance_x = tolerance_x
        self.tolerance_y = tolerance_y
        self.match_param_cursor = match_param_cursor

    def get_position_template(self, item_temp, region_menu, match_param_template=None):
        """
		get_position_template: find the position (x,y) of template(x,y)
        :param item_temp: template of  the first item in menu or the first
        key in the keyboard
        :param region_menu: specific region to search template
        :return: position x and y of item_temp

	   """
        if match_param_template is None:
            match_param_template = eval(stbt.get_config("navigation", "match_param_template"))

        if stbt.wait_until(lambda: stbt.match(image=item_temp,
                                              region=region_menu, match_parameters=match_param_template).match,
                           timeout_secs=5):
            return stbt.match(image=item_temp, region=region_menu, match_parameters=match_param_template).region

    def next_key(self, source, target, tolerance_x, tolerance_y):

        """
        next_key:  press key (down/up/left/right )
        to get closer to the target position.
        -if you don't need to press key_up/key_down in your menu => maximize tolerance_y
        -if you don't need to press key_right/left => maximize  tolerance_x
        :param source : cursor of navigation
        :param target: item in menu, wish looking for
        :param tolerance_x: tolerance of position x
        :param tolerance_y: tolerance of position y

        :return: False if source.x == target.x and
		target.y == target.y (no press)
           else True
        """

        if self.less(source.y, target.y, tolerance=tolerance_y):
            sc_stbt.press("KEY_DOWN")
            return True
        if self.less(target.y, source.y, tolerance=tolerance_y):
            sc_stbt.press("KEY_UP")
            return True

        if self.less(source.x, target.x, tolerance=tolerance_x):
            sc_stbt.press("KEY_RIGHT")
            return True

        if self.less(target.x, source.x, tolerance=tolerance_x):
            sc_stbt.press("KEY_LEFT")
            return True

    def less(self, a, b, tolerance):
        # An implementation of '<' with a tolerance of what is considered equal.
        return a < (b - tolerance)

    def go_to_target(self, target):
        """
	    go_to_target: get position of the current cursor(using match template)
		 and compare it with target position to press next key to get
		 closer to target position
		 !)precondition: you must initialize constructor gototarget()
        :param target:  position (x,y) of item we are looking for
        :return: True if target found
              else False
        """

        if self.match_param_cursor is None:
            self.match_param_cursor = eval(stbt.get_config("navigation", "match_param_cursor"))
        result = False
        start_time = time.time()

        while (result == False) and (time.time() - start_time < 200):
            source = self.get_position_template(item_temp=self.cursor_template, region_menu=self.region_cursor,
                                                match_param_template=self.match_param_cursor)
            if source is not None:
                # print ("source_x=%d , source_y=%d", source.x, source.y)
                if self.next_key(source, target, self.tolerance_x, self.tolerance_y):
                    sc_stbt.wait(5)
                    result = False
                else:
                    result = True
            else:
                result = False
                assert result, "CURSOR NOT FOUND"

        return result

    def read_target(self, target_text, initial_region, key="KEY_DOWN", duration_after_press=10, mode=stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,threshold=None,timeout=250):
        """
        read_target: read target in vertical menu from dynamic region_selected
        -get position of the current cursor
        -use this position to construct a region wish called: region_item_selected
        -read with ocr_mode text exist in this region_item_selected
        :param target_text: target looking for
        :param initial_region: is an object to define the initial region to start reading the item_text
        :return: the region_item_selected of target_text else
        fail with assert if item_text is not found
        """
        if threshold is None :
            threshold= 0.9
        result = False
        start_time = time.time()
        while (result == False) and (time.time() - start_time < timeout):
            source = self.get_position_template(item_temp=self.cursor_template, region_menu=self.region_cursor,
                                                match_param_template=self.match_param_cursor)

            if source is not None:
                region_item_selected = stbt.Region(x=source.x + self.tolerance_x, y=source.y + self.tolerance_y,
                                                   width=initial_region.width,
                                                   height=initial_region.height)

                if stbts.match_text(text=target_text,
                                      region=region_item_selected,
                                      timeout_secs=1, threshold=threshold, mode=mode):
                    sc_stbt.debug(target_text + " " + "IS FOUND")
                    return region_item_selected
                else:
                    sc_stbt.press(key)
                    sc_stbt.wait(duration_after_press)
                    result = False
        assert result, ("%s NOT FOUND" % (target_text))
