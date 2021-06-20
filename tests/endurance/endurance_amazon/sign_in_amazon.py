# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import android
import sc_stbt
import stbt

android1 = eval(stbt.get_config("android","android"))
if android1 == True :
	android.open_app(apps="Amazon", callable= lambda : sc_stbt.is_amazon_signin())
	sc_stbt.sign_in_amazon()
else :
	# sc_stbt.is_amazon_signin(press="KEY_OK")
	sc_stbt.sign_in_amazon()