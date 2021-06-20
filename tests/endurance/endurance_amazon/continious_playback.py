
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


while True:

	if stbts.match_text(text="prime video",
                    region=stbt.Region(x=286, y=224, width=384, height=78),
                    threshold=0.8,
                    timeout_secs=5).match:

		sc_stbt.press("KEY_OK")
		sc_stbt.debug("You have reach the 6th episodes")

	else :
		pass