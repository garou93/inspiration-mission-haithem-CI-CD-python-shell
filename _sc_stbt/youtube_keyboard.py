# -*- coding: utf-8 -*-

import stbt
import networkx as nx
import sc_stbt


class youtube_keyboard():

    """
    Helper for navigating an on-screen youtube keyboard using the remote control.
    to use this class simply follow this example :
    youtube = youtube_keyboard('eng') # for ENG keyboard  / youtube_keyboard('spa') # for SPA keyboard
    youtube.enter_text("hunger games")
    """
    def __init__(self, lang):
        self.lang = lang
        if self.lang == 'eng':
            self.KEYBOARD_GRID = stbt.Grid(region=stbt.Region(x=341, y=81, width=247, height=139),
                                           data=["ABCDEFG",
                                                 "HIJKLMN",
                                                 "OPQRSTU",
                                                 "VWXYZ-'"])
        elif self.lang =='spa':
            self.KEYBOARD_GRID = stbt.Grid(region=stbt.Region(x=341, y=81, width=247, height=139),
                                           data=["ABCDEFG",
                                                 "HIJKLMN",
                                                u'Ñ'+"OPQRST",
                                                 "UVWXYZ'"])
        else :
            raise Exception('%s keyboard language is not supported, perhaps a typo ?' %(self.lang))

        self.BOTTOM_GRID = stbt.Grid(region=stbt.Region(x=345, y=220, width=260, height=40),
                                data=[[" ", "CLEAR", "SEARCH"]])

        self.G1 = nx.compose(stbt.grid_to_navigation_graph(self.KEYBOARD_GRID),
                        stbt.grid_to_navigation_graph(self.BOTTOM_GRID))

        # Pressing down from the bottom row always goes to SPACE:
        for k in self.KEYBOARD_GRID.data[-1]:
            self.G1.add_edge(k, "SPACE", key="KEY_DOWN")

        # Pressing back up from the space/clear/search row can go to any column
        # in the bottom row:
        for k in self.KEYBOARD_GRID.data[-1]:
            for j in self.BOTTOM_GRID .data[-1]:
                self.G1.add_edge(j, k, key="KEY_UP")

        self._kb = stbt.Keyboard(self.G1)

    selection_highlight = sc_stbt.get_generic_template_path() + \
                          "/../../../trunk/tests/templates/youtube/cursor_highlight/selection-highlight.png"
    @property
    def is_visible(self):
        return True

    def refresh(self):
        return youtube_keyboard(self.lang)

    @property
    def selection(self):

        m = stbt.match(self.selection_highlight, region=stbt.Region(x=347, y=82, width=246, height=180))
        for grid in [self.KEYBOARD_GRID, self.BOTTOM_GRID]:
            try:
                text = grid.get(region=m.region).data
                return stbt.Keyboard.Selection(text, m.region)
            except IndexError:
                pass

    def enter_text(self, text):
        # we can't use press and wait for space
        for letter in text:
            self.navigate_to(letter.upper())
            if letter != ' ':
                assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                                region=stbt.Region(x=70, y=35, width=431, height=31)),
                                       timeout_secs=1.5), "STB Timed out"
            else:
                stbt.press("KEY_OK")

        # after writing the text navigate to search and press OK
        self.navigate_to("SEARCH")
        assert stbt.wait_until(lambda: stbt.press_and_wait(key="KEY_OK",
                                                           region=stbt.Region(x=181, y=323, width=655, height=146)),
                               timeout_secs=1.5), "STB Timed out"

    def navigate_to(self, target):
        return self._kb.navigate_to(target, page=self)