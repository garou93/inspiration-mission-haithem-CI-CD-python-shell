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
import time
import stbts

cbeebies_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/cbeebies/"
path_mask_blackscreen = cbeebies_path_template + "/black/mask_black.png"
path_mask_motion = cbeebies_path_template + "/motion/mask_motion.png"
threshold = stbt.get_config("cbeebies", "threshold", type_=float)
consecutive_frames = stbt.get_config("cbeebies", "consecutive_frames")
noise_threshold = stbt.get_config("cbeebies", "noise_threshold", type_=float)
key_pause = stbt.get_config("cbeebies", "key_pause")
key_forward = stbt.get_config("cbeebies", "key_forward")
pause_frame = eval(stbt.get_config("cbeebies", "pause_frame"))
polling_secs = stbt.get_config("cbeebies", "polling_secs", type_=int)
test_secs = stbt.get_config("cbeebies", "test_secs", type_=int)
interval_secs = stbt.get_config("cbeebies", "interval_secs", type_=int)
wait_pause_secs = stbt.get_config("cbeebies", "wait_pause_secs", type_=int)
occurence_forward = stbt.get_config("cbeebies", "occurence_forward", type_=int)
occurence_rewind = stbt.get_config("cbeebies", "occurence_rewind", type_=int)
match_parameters = eval(stbt.get_config("cbeebies", "match_parameters"))
region_current_timer = eval(stbt.get_config("cbeebies", "region_current_timer"))
region_end_timer = eval(stbt.get_config("cbeebies", "region_end_timer"))



cbeebies = sc_stbt.video_tests(path_mask_motion=path_mask_motion,
                              path_mask_blackscreen=path_mask_blackscreen,
                              threshold=threshold,
                              consecutive_frames=consecutive_frames,
                              noise_threshold=noise_threshold,
                              key_pause=key_pause,
                              key_forward=key_forward,
                              pause_frame=pause_frame,
                              polling_secs=polling_secs,
                              test_secs=test_secs,
                              interval_secs=interval_secs,
                              wait_pause_secs=wait_pause_secs,
                              occurence_forward=occurence_forward,
                              occurence_rewind=occurence_rewind,
                              match_parameters=match_parameters,
                              region_current_timer=region_current_timer,
                              region_end_timer=region_end_timer)

def test_cbeebies_fastforward(occurence_forward=occurence_forward,
                             key_forward=key_forward,
                             wait_pause_secs=wait_pause_secs):
    """
    test_netflix_fastforward: check motion is forwarded
    :return:
            * Make video play with test_youtube_play()
            * use trick_mode with press= forward of video class (see how to use video)
    """
    cbeebies.fastforward(occurence_forward=occurence_forward,
                        key_forward=key_forward,
                        key_pause=key_pause,
                        wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY', 'KEY_PLAY'])
    sc_stbt.wait(10)


def test_cbeebies_rewind(occurence_rewind=occurence_rewind,
                        wait_pause_secs=wait_pause_secs):
    """
    test_netflix_fastforward: check motion is rewinded
    :return: * Make video play with test_youtube_play()
             * use trick_mode with press= rewind of video class (see how to use video)
    """
    cbeebies.rewind(occurence_rewind=occurence_rewind,
                   key_pause=key_pause,
                   wait_pause_secs=wait_pause_secs)
    sc_stbt.combo_press(['KEY_PLAY', 'KEY_PLAY'])
    sc_stbt.wait(10)


def test_cbeebies_motion(polling_secs=10, test_secs=40, interval_secs=2):
    """
    test_cbeebies_motion: detect motion from CBEEBIES video
    :return: true where motion is detected , False is not
    """
    sc_stbt.wait(10)
    cbeebies.test_motion(polling_secs=polling_secs,
                        test_secs=test_secs,
                        interval_secs=interval_secs)

