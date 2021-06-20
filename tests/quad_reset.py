"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""


import sc_stbt

def reset_quad():
    sc_stbt.combo_press(combo=["KEY_RESET"], delay_sec=2, number_press=5)
    sc_stbt.wait(10)
    sc_stbt.combo_press(combo=["KEY_RESOLUTION_1080P"], delay_sec=2, number_press=5)


