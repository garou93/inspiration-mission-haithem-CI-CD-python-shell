#!/usr/bin/env python
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


sc_stbt.go_to_youtube()
sc_stbt.test_open_video_youtube(video_name="ruby lebanese")
sc_stbt.test_youtube_motion(test_secs=86000,
                        polling_secs=80)
