# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import vodafone
import sc_stbt

youtube_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/youtube/"
path_mask_motion1 = youtube_path_template + "/motion/mask_motion.png"



youtube = sc_stbt.video_tests(path_mask_motion1)
vodafone.goto_youtube()
sc_stbt.test_open_video_youtube()
sc_stbt.test_youtube_motion(test_secs=1)

vodafone.goto_amazon()
sc_stbt.is_amazon()
sc_stbt.open_library()
sc_stbt.goto_movies_menu()
sc_stbt.select_free_video()
sc_stbt.start_movie()
sc_stbt.detect_movie(test_secs=1)