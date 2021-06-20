# -*- coding: utf-8 -*-

import stbt
import networkx as nx
import sc_stbt
import time

class amazon_keyboard():

    """
    Helper for navigating an on-screen amazon keyboard using the remote control.
    to use this class simply follow this example :
    keyboard = amazon_keyboard()
    keyboard.enter_text("hunger games")
    """
    selection_highlight = sc_stbt.get_generic_template_path() + \
                          "/../../../trunk/tests/templates/templates_amazon/keyboard/amazon_highlight_1.png"

    abc_grid = stbt.Grid(region=stbt.Region(x=264, y=231, width=356, height=141),
                        data=["1234567890",
                              "QWERTYUIOP",
                              "ASDFGHJKL-",
                              "ZXCVBNM@._"])
    clear_maj_special = stbt.Grid(region=stbt.Region(x=624, y=231, width=68, height=176),
                                data=[["CLEAR"],["MAJ"],["SYMBOLS_2"],["SYMBOLS"],["SEARCH"]])
     
    space_grid = stbt.Grid(region=stbt.Region(x=335, y=372, width=214, height=31),
                        data=[[" "]])

    clear_all = stbt.Grid(region=stbt.Region(x=263, y=375, width=69, height=33),
                        data=[["CLEAR_ALL"]])

    special_chars = stbt.Grid(region=stbt.Region(x=264, y=231, width=356, height=141),
                        data=["!:#$%~&*;+",
                              "\"\'()~./<^>",
                              "?@[\\]^_{|}",
                              "£€¥Š÷×××××"])

    G1 = nx.union_all([stbt.grid_to_navigation_graph(abc_grid),
                          stbt.grid_to_navigation_graph(clear_maj_special),
                          stbt.grid_to_navigation_graph(space_grid),
                          stbt.grid_to_navigation_graph(clear_all)])

    G2 = nx.union_all([stbt.grid_to_navigation_graph(special_chars),
                          stbt.grid_to_navigation_graph(clear_maj_special),
                          stbt.grid_to_navigation_graph(space_grid),
                          stbt.grid_to_navigation_graph(clear_all)])


    for i in range(len(abc_grid.data)):
        G1.add_edge(abc_grid.data[i][-1], clear_maj_special.data[i][0], key="KEY_RIGHT")
        G1.add_edge(abc_grid.data[i][0], clear_maj_special.data[i][0], key="KEY_LEFT")
        G1.add_edge(clear_maj_special.data[i][0], abc_grid.data[i][-1], key="KEY_LEFT")
        G1.add_edge(clear_maj_special.data[i][0], abc_grid.data[i][0], key="KEY_RIGHT")
    for k in range(len(special_chars.data)):
        G2.add_edge(special_chars.data[k][-1], clear_maj_special.data[k][0], key="KEY_RIGHT")
        G1.add_edge(abc_grid.data[k][0], clear_maj_special.data[k][0], key="KEY_LEFT")
        G2.add_edge(clear_maj_special.data[k][0], special_chars.data[k][-1], key="KEY_LEFT")
        G1.add_edge(clear_maj_special.data[k][0], abc_grid.data[k][0], key="KEY_RIGHT")

    j = 3
    while j < 7:
        G1.add_edge(abc_grid.data[-1][j], space_grid.data[0][0], key="KEY_DOWN")
        G2.add_edge(special_chars.data[-1][j], space_grid.data[0][0], key="KEY_DOWN")
        j += 1
    
    x = 0
    while x < 3:
        G1.add_edge(abc_grid.data[-1][x], clear_all.data[0][0], key="KEY_DOWN")
        G2.add_edge(special_chars.data[-1][x], clear_all.data[0][0], key="KEY_DOWN")
        x += 1


    G1.add_edge(space_grid.data[0][0], abc_grid.data[-1][5], key="KEY_UP")
    G2.add_edge(space_grid.data[0][0], special_chars.data[-1][5], key="KEY_UP")
    
    G1.add_edge(clear_all.data[0][0], abc_grid.data[-1][1], key="KEY_UP")
    G2.add_edge(clear_all.data[0][0], special_chars.data[-1][1], key="KEY_UP")

    G1.add_edge(clear_all.data[0][0], space_grid.data[0][0], key="KEY_RIGHT")
    G1.add_edge(space_grid.data[0][0], clear_all.data[0][0], key="KEY_LEFT")
    G2.add_edge(clear_all.data[0][0], space_grid.data[0][0], key="KEY_RIGHT")
    G2.add_edge(space_grid.data[0][0], clear_all.data[0][0], key="KEY_LEFT")


    _kb = stbt.Keyboard(G1, G2)

    @property
    def is_visible(self):
        return True

    def refresh(self):
        return amazon_keyboard()

    @property
    def selection(self):
        m = stbt.match(self.selection_highlight, region=stbt.Region(x=264, y=231, width=428, height=176))
        for grid in [self.abc_grid, self.clear_maj_special, self.space_grid, self.clear_all]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    @property
    def selection_2(self):
        m = stbt.match(self.selection_highlight, region=stbt.Region(x=264, y=231, width=428, height=176))
        for grid in [self.special_chars, self.clear_maj_special, self.space_grid, self.clear_all]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass
    
    def enter_text(self, text):
        page = self
        keyboard_state = False
        special_char = False
        switch_char = ["@",".","_","-"]
        for letter in text:
            if letter.upper() in self.G1:
                if special_char:
                    self._kb.navigate_to("MAJ", page)
                    stbt.press("KEY_OK")
                    time.sleep(1)
                    special_char = False

                if letter.isupper() and keyboard_state is False:
                    self._kb.navigate_to("MAJ", page)
                    assert stbt.wait_until(
                        lambda:stbt.press_and_wait
                        ("KEY_OK", match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method='none',
                                                                           match_threshold=0.9999,
                                                                           confirm_threshold=0.3),
                                    region = page.selection.region),
                         timeout_secs = 1.5), "KEY OK FAILED"
                    time.sleep(1)
                    keyboard_state = True

                elif (letter.isdigit() or letter in switch_char) and keyboard_state:
                    self._kb.navigate_to("MAJ", page)
                    assert stbt.wait_until(
                        lambda:stbt.press_and_wait
                        ("KEY_OK", match_parameters = stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method='none',
                                                                           match_threshold=0.9999,
                                                                           confirm_threshold=0.3),
                                    region = page.selection.region),
                         timeout_secs=1.5), "KEY OK FAILED"
                    time.sleep(1)
                    keyboard_state = False

                elif letter.islower() and keyboard_state is False:
                    letter = letter.upper()

                elif letter.islower() and keyboard_state:
                    self._kb.navigate_to("MAJ", page)
                    assert stbt.wait_until(
                        lambda :stbt.press_and_wait
                        ("KEY_OK", match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                         confirm_method='none',
                                                                         match_threshold=0.9999,
                                                                         confirm_threshold=0.3),
                                    region=page.selection.region),
                         timeout_secs=1.5), "KEY OK FAILED"
                    time.sleep(1)
                    letter = letter.upper()
                    keyboard_state = False

            #else letter is a special char
            else:
                if letter not in self.G2:
                    raise ValueError("'%s' isn't in the keyboard" % (letter,))

                if special_char is False:
                    self._kb.navigate_to("SYMBOLS", page)
                    assert stbt.wait_until(
                        lambda:stbt.press_and_wait
                        ("KEY_OK", match_parameters = stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method='none',
                                                                           match_threshold=0.9999,
                                                                           confirm_threshold=0.3),
                                    region = page.selection.region),
                        timeout_secs = 1.5), "KEY OK FAILED"
                    time.sleep(1)
                    special_char = True

            page = self._kb.navigate_to(letter, page)
            assert stbt.wait_until(
                lambda :stbt.press_and_wait
                ("KEY_OK", match_parameters = stbt.MatchParameters(match_method='sqdiff-normed',
                                                                   confirm_method='none',
                                                                   match_threshold=0.9999,
                                                                   confirm_threshold=0.3),
                        region = stbt.Region(x=261, y=188, width=440, height=22)),
                timeout_secs = 1.5), "KEY OK FAILED"
            
        # after typing the text navigate to search and press OK
        self.navigate_to("SEARCH")
        stbt.press("KEY_OK")
    

    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)

########################### New Method SEARCH ##############################

class amazon_search():
    """
    Helper for navigating an on-screen amazon search keyboard using the remote control.
    to use this class simply follow this example :
    _search = amazon_search_movie()
    _search.enter_text("hunger games")
    """
    _highlight = sc_stbt.get_generic_template_path() + \
                          "/../../../trunk/tests/templates/templates_amazon/keyboard/amazon_search.png"

    letters_grid_1 = stbt.Grid(region=stbt.Region(x=245, y=369, width=251, height=106),
                          data=["QWERTYU",
                                "ASDFGHJ",
                                "ZXCVBNM"])

    letters_grid_2 = stbt.Grid(region=stbt.Region(x=498, y=370, width=104, height=69),
                          data=["IOP",
                                "KL\\"])
    # "\" refer to MAJ button
    _space = stbt.Grid(region=stbt.Region(x=497, y=442, width=106, height=33),
                         data=[" "])
    _special = stbt.Grid(region=stbt.Region(x=245, y=369, width=358, height=106),
                         data=["1234567890",
                               "-/:;()*&\"\\",
                               ".,?!%$'@+#"])

    _clear = stbt.Grid(region=stbt.Region(x=604, y=368, width=108, height=107),
                         data=[["DEL"],["clear_search"],["clear_history"]])

    G1 = nx.union_all([stbt.grid_to_navigation_graph(letters_grid_1),
                    stbt.grid_to_navigation_graph(letters_grid_2),
                    stbt.grid_to_navigation_graph(_space),
                    stbt.grid_to_navigation_graph(_clear)])

    G2 = nx.union_all([stbt.grid_to_navigation_graph(_clear),
                        stbt.grid_to_navigation_graph(_special)])

    # linking keyboards of G1
    # edge between letters_grid 1 --> (letters_grid2 / _space :navigation RIGHT)
    G1.add_edge(letters_grid_1.data[0][-1], letters_grid_2.data[0][0], key="KEY_RIGHT")
    G1.add_edge(letters_grid_1.data[1][-1], letters_grid_2.data[1][0], key="KEY_RIGHT")
    G1.add_edge(letters_grid_1.data[2][-1], _space.data[0][0], key="KEY_RIGHT")

    # edge between letters_grid 2 --> (letters_grid1 :navigation LEFT)
    G1.add_edge(letters_grid_2.data[0][0], letters_grid_1.data[0][-1], key="KEY_LEFT")
    G1.add_edge(letters_grid_2.data[1][0], letters_grid_1.data[1][-1], key="KEY_LEFT")

    # edge between _space --> (letters_grid1 :navigation LEFT)
    G1.add_edge(_space.data[0][0],letters_grid_1.data[2][-1], key="KEY_LEFT")

    # edge between letters_grid 1 --> ( _clear :both navigation RIGHT & LEFT)
    for i in range(len(_clear)):
        G1.add_edge(letters_grid_1.data[i][0], _clear.data[i][0], key="KEY_LEFT")
        G1.add_edge(_clear.data[i][0], letters_grid_1.data[i][0], key="KEY_RIGHT")

    # edge between _clear --> (letters_grid 2 / _space:both navigation LEFT & RIGHT)
    for i in range(0,2):
        G1.add_edge(_clear.data[i][0], letters_grid_2.data[i][-1], key="KEY_LEFT")
        G1.add_edge(letters_grid_2.data[i][-1], _clear.data[i][0], key="KEY_RIGHT")
    G1.add_edge(_clear.data[2][0], _space.data[0][0], key="KEY_LEFT")
    G1.add_edge(_space.data[0][0], _clear.data[2][0], key="KEY_RIGHT")

    # edge between _space --> (letters_grid 2 :both navigation UP & DOWN)
    G1.add_edge(_space.data[0][0], letters_grid_2.data[1][1], key="KEY_UP")
    G1.add_edge(letters_grid_2.data[1][-1], _space.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters_grid_2.data[1][1], _space.data[0][0], key="KEY_DOWN")

    # edge between letters_grid_2 --> (letters_grid 1 : navigation DOWN)
    G1.add_edge(letters_grid_2.data[1][0], letters_grid_1.data[-1][-1], key="KEY_DOWN")

    # linking keyboards of G2
    # edge between (_special & _clear) :both navigation RIGHT & LEFT
    for i in range(len(_clear)):
        G2.add_edge(_special.data[i][-1], _clear.data[i][0], key="KEY_RIGHT")
        G2.add_edge(_special.data[i][0], _clear.data[i][0], key="KEY_LEFT")
        G2.add_edge(_clear.data[i][0], _special.data[i][-1], key="KEY_LEFT")
        G2.add_edge(_clear.data[i][0], _special.data[i][0], key="KEY_RIGHT")

    _kb = stbt.Keyboard(G1,G2)

    @property
    def is_visible(self):
        return True

    def refresh(self):
        return amazon_search()

    @property
    def selection(self):
        m = stbt.match(self._highlight, region=stbt.Region(x=245, y=371, width=466, height=104))
        for grid in [self.letters_grid_1, self.letters_grid_2, self._space, self._clear]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    @property
    def selection_2(self):
        m = stbt.match(self._highlight, region=stbt.Region(x=245, y=371, width=466, height=106))
        for grid in [self._special, self._clear]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    def enter_text(self, text):
        page = self
        special_char = False
        for letter in text:
            if letter.upper() in self.G1:
                if special_char:
                    self.navigate_to("\\")
                    assert stbt.wait_until(
                        lambda:stbt.press_and_wait
                        ("KEY_OK", match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method='none',
                                                                           match_threshold=0.9999,
                                                                           confirm_threshold=0.3),
                                    region = page.selection.region),
                         timeout_secs = 1.5), "KEY OK FAILED"
                    special_char = False

            else:
                if letter not in self.G2:
                    raise ValueError("'%s' isn't in the keyboard" % (letter,))

                if special_char is False :

                    self.navigate_to("\\")
                    assert stbt.wait_until(
                        lambda:stbt.press_and_wait
                        ("KEY_OK", match_parameters=stbt.MatchParameters(match_method='sqdiff-normed',
                                                                           confirm_method='none',
                                                                           match_threshold=0.9999,
                                                                           confirm_threshold=0.3),
                                    region = page.selection.region),
                         timeout_secs = 1.5), "KEY OK FAILED"
                    special_char = True
            self.navigate_to(letter.upper())
            assert stbt.wait_until(
                lambda :stbt.press_and_wait
                ("KEY_OK", match_parameters = stbt.MatchParameters(match_method='sqdiff-normed',
                                                                   confirm_method='none',
                                                                   match_threshold=0.9999,
                                                                   confirm_threshold=0.3),
                        region = stbt.Region(x=241, y=318, width=476, height=36)),
                timeout_secs = 1.5), "KEY OK FAILED"


    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)

