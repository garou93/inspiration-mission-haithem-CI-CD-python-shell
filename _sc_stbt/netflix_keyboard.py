# -*- coding: utf-8 -*-

"""
Description : Helper for navigating on-screen netflix keyboard
three keyboards are implemented : netflix_enter_account , netflix_enter_password & netflix_search_movie
"""

# TODO: Check that KEY_OK adds to the search text? With a property on the
#   page object? OCR might be too unreliable for incomplete words. We don't
#   use press_and_wait because the text-box might be masked out (some UIs
#   have a blinking cursor there).

import stbt
import networkx as nx
import sc_stbt


class netflix_enter_password():

    """
    Helper for navigating an on-screen netflix password keyboard using the remote control.
    to use this class simply follow this example :

    netflix_password_keyboard = netflix_enter_password()
    netflix_password_keyboard.enter_text("$aGemcom Softw@re & Technologies")

    """

    selection_highlight = sc_stbt.get_generic_template_path() + \
                          "/../../../trunk/tests/templates/netflix/cursor_highlight/netflix-highlight.png"

    letters = stbt.Grid(region=stbt.Region(x=75, y=164, width=360, height=109),
                        data=["1234567890",
                              "QWERTYUIOP",
                              "ASDFGHJKL-"])

    MAJ = stbt.Grid(region=stbt.Region(x=111, y=272, width=35, height=34),
                    data=[["MAJ"]])

    letters_2 = stbt.Grid(region=stbt.Region(x=148, y=273, width=286, height=35),
                          data=["ZXCVBNM'"])

    symbols = stbt.Grid(region=stbt.Region(x=76, y=308, width=142, height=36),
                        data=[["SYMBOLS", "SYMBOLS_2"]])

    space_clear = stbt.Grid(region=stbt.Region(x=219, y=308, width=215, height=36),
                            data=[[" ", "CLEAR"]])

    special_chars = stbt.Grid(region=stbt.Region(x=76, y=164, width=358, height=144),
                              data=["`~!@#$%^&*",
                                    "()-_=+[]{}",
                                    "\|;:'é,.<>",
                                    "/?¡¿a°c€£¥"])

    _next = stbt.Grid(region=stbt.Region(x=221, y=360, width=214, height=42),
                      data=[["NEXT"]])

    # first keyboard with no special chars
    G1 = nx.union_all([stbt.grid_to_navigation_graph(letters),
                       stbt.grid_to_navigation_graph(MAJ),
                       stbt.grid_to_navigation_graph(letters_2),
                       stbt.grid_to_navigation_graph(space_clear),
                       stbt.grid_to_navigation_graph(symbols),
                       stbt.grid_to_navigation_graph(_next)])

    # second keyboard with special chars
    G2 = nx.union_all([stbt.grid_to_navigation_graph(special_chars),
                       stbt.grid_to_navigation_graph(symbols),
                       stbt.grid_to_navigation_graph(space_clear)])

    # MAJ & letters
    G1.add_edge(letters.data[-1][0], MAJ.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters.data[-1][1], MAJ.data[0][0], key="KEY_DOWN")
    G1.add_edge(MAJ.data[0][0], letters.data[2][0], key="KEY_UP")
    G1.add_edge(MAJ.data[0][0], letters.data[2][1], key="KEY_UP")

    # MAJ & letters_2
    G1.add_edge(letters_2.data[0][0], MAJ.data[0][0], key="KEY_LEFT")
    G1.add_edge(MAJ.data[0][0], letters_2.data[0][0], key="KEY_RIGHT")

    # letters & letters_2
    for k, j in zip(letters_2.data[0], letters.data[-1][2:]):
        G1.add_edge(k, j, key="KEY_UP")
        G1.add_edge(j, k, key="KEY_DOWN")

    # symbols & letter_2 & MAJ
    G1.add_edge(symbols.data[0][0], MAJ.data[0][0], key="KEY_UP")
    G1.add_edge(symbols.data[0][1], letters_2.data[0][0], key="KEY_UP")
    G1.add_edge(symbols.data[0][1], letters_2.data[0][1], key="KEY_UP")
    G1.add_edge(MAJ.data[0][0], symbols.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][0], symbols.data[0][1], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][1], symbols.data[0][1], key="KEY_DOWN")

    # space_clear & letter2 & symbols
    G1.add_edge(symbols.data[0][1], space_clear.data[0][0], key="KEY_RIGHT")
    G1.add_edge(space_clear.data[0][0], symbols.data[0][1], key="KEY_LEFT")
    # letters & space
    G1.add_edge(space_clear.data[0][0], letters_2.data[0][2], key="KEY_UP")
    G1.add_edge(space_clear.data[0][0], letters_2.data[0][3], key="KEY_UP")
    G1.add_edge(space_clear.data[0][0], letters_2.data[0][4], key="KEY_UP")

    G1.add_edge(letters_2.data[0][2], space_clear.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][3], space_clear.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][4], space_clear.data[0][0], key="KEY_DOWN")

    # letters & clear
    G1.add_edge(space_clear.data[0][1], letters_2.data[0][5], key="KEY_UP")
    G1.add_edge(space_clear.data[0][1], letters_2.data[0][6], key="KEY_UP")
    G1.add_edge(space_clear.data[0][1], letters_2.data[0][7], key="KEY_UP")

    G1.add_edge(letters_2.data[0][5], space_clear.data[0][1], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][6], space_clear.data[0][1], key="KEY_DOWN")
    G1.add_edge(letters_2.data[0][7], space_clear.data[0][1], key="KEY_DOWN")

    # next & upper row
    G1.add_edge(_next.data[0][0], space_clear.data[0][0], key="KEY_UP")
    G1.add_edge(_next.data[0][0], space_clear.data[0][1], key="KEY_UP")
    G1.add_edge(_next.data[0][0], symbols.data[0][0], key="KEY_UP")
    G1.add_edge(_next.data[0][0], symbols.data[0][1], key="KEY_UP")

    G1.add_edge(space_clear.data[0][0], _next.data[0][0], key="KEY_DOWN")
    G1.add_edge(space_clear.data[0][1], _next.data[0][0], key="KEY_DOWN")
    G1.add_edge(symbols.data[0][0], _next.data[0][0], key="KEY_DOWN")
    G1.add_edge(symbols.data[0][1], _next.data[0][0], key="KEY_DOWN")

    ########################### Special chars graph ###########################

    # ABC UP
    G2.add_edge(symbols.data[0][0], special_chars.data[-1][0], key="KEY_UP")
    G2.add_edge(symbols.data[0][0], special_chars.data[-1][1], key="KEY_UP")
    # ABC DOWN
    G2.add_edge(special_chars.data[-1][0], symbols.data[0][0], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][1], symbols.data[0][0], key="KEY_DOWN")
    # AAA UP
    G2.add_edge(symbols.data[0][1], special_chars.data[-1][2], key="KEY_UP")
    G2.add_edge(symbols.data[0][1], special_chars.data[-1][3], key="KEY_UP")
    # AAA DOWN
    G2.add_edge(special_chars.data[-1][2], symbols.data[0][1], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][3], symbols.data[0][1], key="KEY_DOWN")
    # AAA RIGHT
    G2.add_edge(symbols.data[0][1], space_clear.data[0][0], key="KEY_RIGHT")
    # SPACE UP
    G2.add_edge(space_clear.data[0][0], special_chars.data[-1][4], key="KEY_UP")
    G2.add_edge(space_clear.data[0][0], special_chars.data[-1][5], key="KEY_UP")
    G2.add_edge(space_clear.data[0][0], special_chars.data[-1][6], key="KEY_UP")
    # SPACE DOWN
    G2.add_edge(special_chars.data[-1][4], space_clear.data[0][0], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][5], space_clear.data[0][0], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][6], space_clear.data[0][0], key="KEY_DOWN")
    # SPACE LEFT
    G2.add_edge(space_clear.data[0][0], symbols.data[0][1], key="KEY_LEFT")
    # CLEAR UP
    G2.add_edge(space_clear.data[0][1], special_chars.data[-1][7], key="KEY_UP")
    G2.add_edge(space_clear.data[0][1], special_chars.data[-1][8], key="KEY_UP")
    G2.add_edge(space_clear.data[0][1], special_chars.data[-1][9], key="KEY_UP")
    # CLEAR DOWN
    G2.add_edge(special_chars.data[-1][7], space_clear.data[0][1], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][8], space_clear.data[0][1], key="KEY_DOWN")
    G2.add_edge(special_chars.data[-1][9], space_clear.data[0][1], key="KEY_DOWN")

    _kb = stbt.Keyboard(G1,G2)


    @property
    def is_visible(self):
        return True

    def refresh(self):
        return netflix_enter_password()

    @property
    def selection(self):
        m = stbt.match(self.selection_highlight, region=stbt.Region(x=76, y=165, width=359, height=238))
        for grid in [self.letters, self.MAJ, self.letters_2, self.symbols ,self.space_clear, self._next]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    @property
    def selection_2(self):
        m = stbt.match(self.selection_highlight, region=stbt.Region(x=76, y=165, width=359, height=238))
        for grid in [self.special_chars, self.symbols, self.space_clear]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    def enter_text(self, text):

        # Keyboard state is False for lowercase and True for uppercase
        # The default keyboard state at the beginning is equal to lower, so we're gonna set this variable to False
        keyboard_state = False
        special_char = False

        for letter in text:
            if letter.upper() in self.G1:
                if special_char:
                    self.navigate_to("SYMBOLS")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection.region),
                                           timeout_secs=1.5), "STB Timed out"
                    special_char = False

                if letter.isupper() and keyboard_state is False:
                    self.navigate_to("MAJ")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection.region),
                                           timeout_secs=1.5), "STB Timed out"
                    keyboard_state = True

                elif letter.islower() and keyboard_state is False:
                    letter = letter.upper()

                elif letter.islower() and keyboard_state:
                    self.navigate_to("MAJ")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection.region),
                                           timeout_secs=1.5), "STB Timed out"
                    letter = letter.upper()
                    keyboard_state = False
            # else letter is a special char
            else:
                if letter not in self.G2:
                    raise ValueError("'%s' isn't in the keyboard" % (letter,))

                if special_char is False:
                    self.navigate_to("SYMBOLS")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection_2.region),
                                            timeout_secs=1.5), "STB Timed out"
                    special_char = True

            self.navigate_to(letter)
            stbt.press("KEY_OK")

        # after typing the text navigate to search and press OK
        self.navigate_to("NEXT")
        assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                           region=self.selection.region),
                               timeout_secs=1.5), "STB Timed out"

    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)


class netflix_enter_account():

    """
    Helper for navigating an on-screen netflix account keyboard using the remote control.
    to use this class simply follow this example :

    netflix_account_keyboard = netflix_enter_account()
    netflix_account_keyboard.enter_text("aba_tester")
    """

    selection_highlight = sc_stbt.get_generic_template_path() +\
                          "/../../../trunk/tests/templates/netflix/cursor_highlight/netflix-highlight.png"

    letters = stbt.Grid(region=stbt.Region(x=75, y=164, width=360, height=109),
                        data=["1234567890",
                              "QWERTYUIOP",
                              "ASDFGHJKL-"])

    MAJ = stbt.Grid(region=stbt.Region(x=111, y=272, width=35, height=34),
                    data=[["MAJ"]])

    letters_login_2 = stbt.Grid(region=stbt.Region(x=148, y=273, width=286, height=35),
                            data=["ZXCVBNM_"])

    symbols_login = stbt.Grid(region=stbt.Region(x=76, y=337, width=142, height=36),
                          data=[["SYMBOLS", "@"]])

    com_clear = stbt.Grid(region=stbt.Region(x=255, y=337, width=142, height=34),
                          data=[["COM", "CLEAR"]])

    emails = stbt.Grid(region=stbt.Region(x=75, y=308, width=360, height=29),
                       data=[["HOTMAIL", "GMAIL", "YAHOO"]])

    dot = stbt.Grid(region=stbt.Region(x=219, y=337, width=36, height=36),
                    data=["."])

    _next = stbt.Grid(region=stbt.Region(x=221, y=390, width=214, height=42),
                      data=[["NEXT"]])

    G1 = nx.union_all([stbt.grid_to_navigation_graph(letters),
                       stbt.grid_to_navigation_graph(MAJ),
                       stbt.grid_to_navigation_graph(letters_login_2),
                       stbt.grid_to_navigation_graph(com_clear),
                       stbt.grid_to_navigation_graph(symbols_login),
                       stbt.grid_to_navigation_graph(emails),
                       stbt.grid_to_navigation_graph(dot),
                       stbt.grid_to_navigation_graph(_next)])

    # MAJ & letters
    G1.add_edge(letters.data[-1][0], MAJ.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters.data[-1][1], MAJ.data[0][0], key="KEY_DOWN")
    G1.add_edge(MAJ.data[0][0], letters[-1][0], key="KEY_UP")
    G1.add_edge(MAJ.data[0][0], letters[-1][1], key="KEY_UP")

    # MAJ & letters_login_2
    G1.add_edge(letters_login_2.data[0][0], MAJ.data[0][0], key="KEY_LEFT")
    G1.add_edge(MAJ.data[0][0], letters_login_2[0][0], key="KEY_RIGHT")

    # letters & letters_login_2
    for k, j in zip(letters_login_2.data[0], letters.data[-1][2:]):
        G1.add_edge(k, j, key="KEY_UP")
        G1.add_edge(j, k, key="KEY_DOWN")

    # hotmail & MAJ & Letters
    G1.add_edge(emails.data[0][0], MAJ.data[0][0], key="KEY_UP")
    G1.add_edge(emails.data[0][0], letters_login_2[0][0], key="KEY_UP")
    G1.add_edge(MAJ.data[0][0], emails.data[0][0], key="KEY_DOWN")
    G1.add_edge(letters_login_2[0][0], emails.data[0][0], key="KEY_DOWN")
    # gmail & letters
    for j in range(1, 4):
        G1.add_edge(letters_login_2.data[0][j], emails.data[0][1], key="KEY_DOWN")
        G1.add_edge(emails.data[0][1], letters_login_2.data[0][j], key="KEY_UP")
    # yahoo & letters
    for j in range(5, 7):
        G1.add_edge(letters_login_2.data[0][j], emails.data[0][2], key="KEY_DOWN")
        G1.add_edge(emails.data[0][2], letters_login_2.data[0][j], key="KEY_UP")
    # hotmail & symbols_login
    G1.add_edge(symbols_login.data[0][0], emails.data[0][0], key="KEY_UP")
    G1.add_edge(symbols_login.data[0][1], emails.data[0][0], key="KEY_UP")
    G1.add_edge(emails.data[0][0], symbols_login.data[0][0], key="KEY_DOWN")
    G1.add_edge(emails.data[0][0], symbols_login.data[0][1], key="KEY_DOWN")
    # gmail & dot & .COM
    G1.add_edge(dot.data[0][0], emails.data[0][1], key="KEY_UP")
    G1.add_edge(com_clear.data[0][0], emails.data[0][1], key="KEY_UP")
    G1.add_edge(emails.data[0][1], dot.data[0][0], key="KEY_DOWN")
    G1.add_edge(emails.data[0][1], com_clear.data[0][0], key="KEY_DOWN")
    # yahoo & clear
    G1.add_edge(com_clear.data[0][1], emails.data[0][2], key="KEY_UP")
    G1.add_edge(emails.data[0][2], com_clear.data[0][1], key="KEY_DOWN")
    # dot left & right
    G1.add_edge(dot.data[0][0], symbols_login.data[0][1], key="KEY_LEFT")
    G1.add_edge(symbols_login.data[0][1], dot.data[0][0], key="KEY_RIGHT")
    G1.add_edge(dot.data[0][0], com_clear.data[0][0], key="KEY_RIGHT")
    G1.add_edge(com_clear.data[0][0], dot.data[0][0], key="KEY_LEFT")
    # next and upper row
    for i, j in zip(symbols_login.data[0], com_clear.data[0]):
        G1.add_edge(i, _next.data[0][0], key="KEY_DOWN")
        G1.add_edge(_next.data[0][0], i, key="KEY_UP")
        G1.add_edge(j, _next.data[0][0], key="KEY_DOWN")
        G1.add_edge(_next.data[0][0], j, key="KEY_UP")
    G1.add_edge(dot.data[0][0], _next.data[0][0], key="KEY_DOWN")
    G1.add_edge(_next.data[0][0], dot.data[0][0], key="KEY_UP")

    #keyboard
    _kb = stbt.Keyboard(G1)


    @property
    def is_visible(self):
        return True

    def refresh(self):
        return netflix_enter_account()

    @property
    def selection(self):
        m = stbt.match(self.selection_highlight, region=stbt.Region(x=77, y=166, width=355, height=266))
        for grid in [self.letters, self.MAJ , self.letters_login_2 ,
                     self.symbols_login , self.com_clear, self.emails, self.dot, self._next]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    def enter_text(self, text):

        #shortcuts related to netflix account keyboard
        shortcut = ''
        for item in ['@hotmail.com', '@gmail.com', '@yahoo.com', '.com']:

            if item in text and item != '.com':
                shortcut = (text.split('@')[1].split('.')[0]).upper()
                text = text.split('@')[0]
                break
            elif item in text and item == '.com':
                text = text[:-4]
                shortcut = "COM"
                break

        # Keyboard state is False for lowercase and True for uppercase
        # The default keyboard state at the beginning is equal to lower, so we're gonna set this variable to False
        keyboard_state = False

        for letter in text:
            if letter.upper() in self.G1:

                if letter.isupper() and keyboard_state == False:
                    self.navigate_to("MAJ")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection.region),
                                           timeout_secs=1.5), "STB Timed out"
                    keyboard_state = True

                elif letter.islower() and keyboard_state == False:
                    letter = letter.upper()

                elif letter.islower() and keyboard_state:
                    self.navigate_to("MAJ")
                    assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                       region=self.selection.region),
                                           timeout_secs=1.5), "STB Timed out"
                    letter = letter.upper()
                    keyboard_state = False
            else:
                raise ValueError("'%s' isn't in the keyboard" % (letter,))

            self.navigate_to(letter)
            stbt.press("KEY_OK")

        if shortcut != '':
            self.navigate_to(shortcut)
            stbt.press("KEY_OK")

        # after typing the text navigate to search and press OK
        self.navigate_to("NEXT")
        assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                           region=self.selection.region),
                               timeout_secs=1.5), "STB Timed out"

    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)


class netflix_search_movie():

    """
    Helper for navigating an on-screen netflix search keyboard using the remote control.
    to use this class simply follow this example :
    netflix_search = netflix_search_movie()
    netflix_search.enter_text("hunger games")
    """

    KEYBOARD_GRID = stbt.Grid(region=stbt.Region(x=79, y=76, width=198, height=189),
                          data=["ABCDEF",
                                "GHIJKL",
                                "MNOPQR",
                                "STUVWX",
                                "YZ1234",
                                "567890"])

    UPPER_GRID = stbt.Grid(region=stbt.Region(x=79, y=44, width=198, height=31),
                      data=[[" ", "CLEAR"]])

    selection_highlight = sc_stbt.get_generic_template_path() + \
                          "/../../../trunk/tests/templates/netflix/cursor_highlight/netflix-search-highlight.png"

    G1 = nx.compose(stbt.grid_to_navigation_graph(KEYBOARD_GRID),
                    stbt.grid_to_navigation_graph(UPPER_GRID))

    # Pressing UP for the 3 first letters in first row always goes to SPACE:
    # Pressing UP for the 3 last letters in first row always goes to CLEAR:
    for k,j in zip (KEYBOARD_GRID.data[0][:3], KEYBOARD_GRID.data[0][3:]):
        G1.add_edge(k, "SPACE", key="KEY_UP")
        G1.add_edge("SPACE", k, key="KEY_DOWN")
        G1.add_edge(j, "CLEAR", key="KEY_UP")
        G1.add_edge("CLEAR", j, key="KEY_DOWN")

    _kb = stbt.Keyboard(G1)

    @property
    def is_visible(self):
        return True

    def refresh(self):
        return netflix_search_movie()

    @property
    def selection(self):

        m = stbt.match(self.selection_highlight, region=stbt.Region(x=79, y=44, width=198, height=230))
        for grid in [self.KEYBOARD_GRID, self.UPPER_GRID]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    def enter_text(self, text):
        page = self
        page = self._kb.enter_text(text.upper(), page)

    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)