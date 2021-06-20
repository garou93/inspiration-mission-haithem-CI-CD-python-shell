
# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""


import stbt
import sc_stbt


def play_pause() :
	sc_stbt.test_amazon_pause()
	sc_stbt.test_amazon_play()

def stress_seak ():
	sc_stbt.repeat(lambda : play_pause(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=3)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_rewind(),occurence=2)
	sc_stbt.wait(30)
	sc_stbt.repeat(lambda : play_pause(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_rewind(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=1)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_rewind(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_rewind(),occurence=1)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=2)
	sc_stbt.repeat(lambda : sc_stbt.test_amazon_fastforward(),occurence=1)
	sc_stbt.repeat(lambda : play_pause(),occurence=1)

sc_stbt.repeat(lambda : stress_seak(),occurence = 100)
