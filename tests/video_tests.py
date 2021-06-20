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
import os



video = sc_stbt.video()

video_tests_path_template = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates/video_tests/"
generic_path = sc_stbt.get_generic_template_path() + "/../../../trunk/tests/templates"

path_mask_blackscreen = video_tests_path_template + "/black/mask_black.png"
path_mask_motion = video_tests_path_template + "/motion/mask_motion.png"

threshold = stbt.get_config("video_tests", "threshold", type_=float)
consecutive_frames = stbt.get_config("video_tests", "consecutive_frames")
noise_threshold = stbt.get_config("video_tests", "noise_threshold", type_=float)

key_pause = stbt.get_config("video_tests", "key_pause")
key_forward = stbt.get_config("video_tests", "key_forward")


pause_frame = eval(stbt.get_config("video_tests", "pause_frame"))

timeout_black_screen = stbt.get_config("video_tests", "timeout_black_screen", type_=int)
polling_secs = stbt.get_config("video_tests", "polling_secs", type_=int)
test_secs = stbt.get_config("video_tests", "test_secs", type_=int)
interval_secs =stbt.get_config("video_tests", "interval_secs", type_=int)
wait_pause_secs = stbt.get_config("video_tests", "wait_pause_secs", type_=int)

occurence_forward = stbt.get_config("video_tests", "occurence_forward", type_=int)
occurence_rewind = stbt.get_config("video_tests", "occurence_rewind", type_=int)

match_parameters = eval(stbt.get_config("video_tests", "match_parameters"))

audio = eval(stbt.get_config("global", "audio"))
polling_secs_audio = 20
test_secs_audio = 20

class video_tests(object):

    def __init__(self,
                 path_mask_motion=path_mask_motion,
                 path_mask_blackscreen=path_mask_blackscreen,
                 timeout_black_screen=timeout_black_screen,
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
                 region_current_timer=None,
                 region_end_timer=None):
        """

        :param path_mask_motion:
        :param path_mask_blackscreen:
        :param threshold:
        :param consecutive_frames:
        :param noise_threshold:
        :param key_pause:
        :param key_back:
        :param pause_frame:
        :param time_out_detect_motion:
        :param delay_pause:
        :param timeout_motion:
        :param interval_secs:
        :param wait_pause_secs:
        :param occurence_forward:
        :param occurence_rewind:
        :param key_forward:
        :param match_parameters:
        :return:
        """
        self.path_mask_motion = path_mask_motion
        self.path_mask_blackscreen = path_mask_blackscreen
        self.timeout_black_screen = timeout_black_screen
        self.threshold = threshold
        self.consecutive_frames = consecutive_frames
        self.noise_threshold = noise_threshold
        self.key_pause = key_pause
        self.key_forward = key_forward
        self.pause_frame = pause_frame
        self.polling_secs = polling_secs
        self.timeout_motion = test_secs
        self.interval_secs = interval_secs
        self.wait_pause_secs = wait_pause_secs
        self.occurence_forward = occurence_forward
        self.occurence_rewind = occurence_rewind
        self.match_parameters = match_parameters
        self.region_current_timer = region_current_timer
        self.region_end_timer = region_end_timer

    def motion(self, polling_secs=polling_secs):
        """
        motion: detect motion from  video
        :return:true where motion is detected , False is not
        """
        sc_stbt.wait(5)
        assert video.is_motion(self.path_mask_motion, self.consecutive_frames, self.noise_threshold,
                             time_out_detect_motion=polling_secs), ("NO MOTION DETECTED")
        if audio:
            sc_stbt.wait(1)
            aud = sc_stbt.audio_tests()
            aud.is_audio(polling_secs_audio=20)

    def test_motion(self, polling_secs=polling_secs,
                          test_secs=test_secs,
                          interval_secs=interval_secs , polling_secs_audio=polling_secs_audio , test_secs_audio=test_secs_audio):
        """
        motion: detect motion from  video
        :return:true where motion is detected , False is not
        """
        sc_stbt.wait(5)
        assert video.test_motion(self.path_mask_motion, self.consecutive_frames, self.noise_threshold,
                                      time_out_detect_motion=polling_secs,
                                      test_secs=test_secs,
                                      interval_secs=interval_secs), ("NO MOTION DETECTED")
        if audio:
            sc_stbt.wait(1)
            aud = sc_stbt.audio_tests()
            assert not aud.test_audio(polling_secs_audio,test_secs_audio)
        else:
            pass

    def test_motion_audio(self, test_secs=test_secs):
        """
        test_motion_audio:
        :param test_secs:
        :return:
        """
        sc_stbt.repeat(lambda: self.motion(), time_out=test_secs)

    def pause(self, test_secs=test_secs,
                    polling_secs=polling_secs,
                    interval_secs=interval_secs,
                    key_pause=key_pause,
                    check_timer=False,
                    match_parameters=match_parameters,
                    wait_pause_secs=wait_pause_secs):
        """
        pause: check video is paused for test_secs time
        :return:    *if moition is not detected (video paused )==> play() (make video play for timeout_motion=20s and
                        with time_out_detect_motion=20)==> pause (make video pause for delay_pause=20s and with
                        time_out_detect_motion=20)
                    * elif motion is detected (video pause) ==> pause (make video pause for delay_pause=20s)

                    return false when:
                    1) if video paused: when play() not done (motion not detected)
                    2) if video paused ==>  play() done ==> when pause() not done (motion detected)
                    3) if video played ==> when pause() not done (motion detected)
        """
        sc_stbt.wait(5)
        assert video.test_pause(self.path_mask_motion,
                                self.consecutive_frames,
                                self.noise_threshold,
                                time_out_detect_motion=polling_secs,
                                delay_pause=test_secs,
                                timeout_motion=20,
                                interval_sec_motion=interval_secs,
                                wait_pause_secs=wait_pause_secs,
                                key_pause=key_pause,
                                pause_frame=self.pause_frame,
                                match_parameters=match_parameters), ("VIDEO NOT PAUSED")
        if audio:
            sc_stbt.wait(1)
            aud = sc_stbt.audio_tests()
            assert not aud.test_mute(polling_secs_audio=20, test_secs_audio=20)
        else:
            pass
        if check_timer:
            if stbt.wait_until(lambda:sc_stbt.timer(self.region_current_timer,
                                                    self.region_end_timer),
                       timeout_secs=12):
                sc_stbt.debug("Timer DETECTED")
            else:
                assert False, ("HANG STB")



    def unit_pause(self, test_secs=test_secs,
                         polling_secs=polling_secs,
                         interval_secs=interval_secs,
                         wait_pause_secs=wait_pause_secs,
                         key_pause=key_pause):
        """
        unit_pause: check video is paused
        :return:
        """
        assert video.pause(mask=self.path_mask_motion,
                          noise_threshold=self.noise_threshold,
                          time_out_detect_motion=polling_secs,
                          delay_pause=test_secs,
                          interval_sec_motion=interval_secs,
                          wait_pause_secs=wait_pause_secs,
                          key_pause=key_pause), ("VIDEO NOT UNIT PAUSED")
        if audio:
           sc_stbt.wait(1)
           aud = sc_stbt.audio_tests()
           aud.is_mute(polling_secs_audio=20)
        else:
            pass

    def play(self, test_secs=test_secs,
                    polling_secs=polling_secs,
                    interval_secs=interval_secs,
                    key_pause=key_pause,
                    match_parameters=match_parameters,
                    wait_pause_secs=wait_pause_secs):
        """
        play: check video is played for test_scs time
        :return: *if moition is detected (video played ) ==> pause() (make video pause for delay_pause=20s and with
                    time_out_detect_motion=20)==> play (make video play for timeout_motion=20s and with time_out_detect_motion=20)
                    * elif motion is not detected (video paused) ==> play (make video play for timeout_motion=20s)

                    return false when:
                    1) if video played: when pause() not done (motion detected)
                    2) if video played ==>  pause() done ==> when play() not done (motion not detected)
                    3) if video paused ==> when play() not done (motion not detected)
        """
        assert video.test_play(self.path_mask_motion,
                               self.consecutive_frames,
                               self.noise_threshold,
                               time_out_detect_motion=polling_secs,
                               delay_pause=20,
                               timeout_motion=test_secs,
                               interval_sec_motion=interval_secs,
                               wait_pause_secs=wait_pause_secs,
                               key_pause=key_pause,
                               pause_frame=self.pause_frame,
                               match_parameters=match_parameters), ("VIDEO NOT PLAYED")
        if audio:
            sc_stbt.wait(1)
            aud = sc_stbt.audio_tests()
            aud.is_audio(polling_secs_audio=20)
        else:
            pass

    def unit_play(self, test_secs=test_secs,
                        polling_secs=polling_secs,
                        interval_secs=interval_secs):
        """
        unit_play: check video is played
        :return:
        """
        sc_stbt.wait(5)
        assert video.play(mask=self.path_mask_motion,
                          consecutive_frames=self.consecutive_frames,
                          noise_threshold=self.noise_threshold,
                          time_out_detect_motion=polling_secs,
                          timeout_motion=test_secs,
                          interval_sec_motion=interval_secs), ("VIDEO NOT UNIT PLAYED")
        if audio:
            sc_stbt.wait(1)
            aud = sc_stbt.audio_tests()
            aud.is_audio(polling_secs_audio=20)
        else:
            pass




    def fastforward(self, occurence_forward=occurence_forward,
                    key_pause=key_pause,
                    key_forward=key_forward,
                    match_parameters=match_parameters,
                    wait_pause_secs=wait_pause_secs):
        """
        fastforward: check motion is forwarded
        :return:
                * Make video play with test_youtube_play()
                * use trick_mode with press= forward of video class (see how to use video)
        """
        try:
            self.play(key_pause=key_pause,
                      match_parameters=match_parameters,wait_pause_secs=wait_pause_secs)
        except:
            assert False, ("TEST PLAY FAIL BEFORE FORWARD")
        assert video.trick_mode(self.path_mask_motion,
                                self.consecutive_frames,
                                self.noise_threshold,
                                press=key_forward,
                                occurence=occurence_forward,
                                wait_pause_secs=wait_pause_secs,
                                key_pause=key_pause,
                                pause_frame=self.pause_frame,
                                match_parameters=match_parameters), ("FORWARD VIDEO NOT DONE")
        sc_stbt.press('KEY_PLAY')



    def unit_fastforward(self, occurence_forward=occurence_forward,
                    key_pause=key_pause,
                    key_forward=key_forward,
                    match_parameters=match_parameters,
                    wait_pause_secs=wait_pause_secs):
        """
        fastforward: check motion is forwarded
        :return:
                * use trick_mode with press= forward of video class (see how to use video)
        """
        assert video.trick_mode(self.path_mask_motion,
                                self.consecutive_frames,
                                self.noise_threshold,
                                press=key_forward,
                                occurence=occurence_forward,
                                wait_pause_secs=wait_pause_secs,
                                key_pause=key_pause,
                                pause_frame=self.pause_frame,
                                match_parameters=match_parameters), ("FORWARD VIDEO NOT DONE")
        sc_stbt.press('KEY_PLAY')



    def rewind(self, occurence_rewind=occurence_rewind,
               key_pause=key_pause,
               match_parameters=match_parameters,
               wait_pause_secs=wait_pause_secs):
        """
        rewind: check motion is rewinded
        :return: * Make video play with test_youtube_play()
                 * use trick_mode with press= rewind of video class (see how to use video)
        """
        try:
            self.play(key_pause=key_pause,
                      match_parameters=match_parameters,wait_pause_secs=wait_pause_secs)
        except:
            assert False, ("TEST PLAY FAIL BEFORE REWIND")
        assert video.trick_mode(self.path_mask_motion,
                                self.consecutive_frames,
                                self.noise_threshold,
                                press="KEY_REWIND",
                                occurence=occurence_rewind,
                                wait_pause_secs=wait_pause_secs,
                                key_pause=key_pause,
                                pause_frame=self.pause_frame,
                                match_parameters=match_parameters), ("REWIND VIDEO NOT DONE")
        sc_stbt.press('KEY_PLAY')



    def unit_rewind(self, occurence_rewind=occurence_rewind,
               key_pause=key_pause,
               match_parameters=match_parameters,
               wait_pause_secs=wait_pause_secs):
        """
        rewind: check motion is rewinded
        :return:
                 * use trick_mode with press= rewind of video class (see how to use video)
        """
        assert video.trick_mode(self.path_mask_motion,
                                self.consecutive_frames,
                                self.noise_threshold,
                                press="KEY_REWIND",
                                occurence=occurence_rewind,
                                wait_pause_secs=wait_pause_secs,
                                key_pause=key_pause,
                                pause_frame=self.pause_frame,
                                match_parameters=match_parameters), ("REWIND VIDEO NOT DONE")
        sc_stbt.press('KEY_PLAY')


    def next_video(self, key_pause=key_pause):
        """
        next_video: go to next video and detect blackscreen
        :return: * Make video play with test_youtube_play()
                    * use change_video with press = next_video of video class (see how to use video)

                    return False when:
                    1) blackscreen not detected
        """
        try:
            self.play(key_pause=key_pause,
                      match_parameters=match_parameters)
        except:
            assert False, ("TEST PLAY FAIL BEFORE NEXT VIDEO")
        assert video.change_video(self.path_mask_blackscreen,
                                  self.threshold,
                                  press="KEY_VIDEO_NEXT"), ("NEXT VIDEO NOT DISPLAYED")


    def previous_video(self, key_pause=key_pause):
        """
        previous_video: go to next video and detect blackscreen
        :return: * Make video play with test_youtube_play()
                    * use change_video with press = next_video of video class (see how to use video)

                    retunr False when:
                    1) blackscreen not detected
        """
        try:
            self.play(key_pause=key_pause,
                      match_parameters=match_parameters)
        except:
            assert False, ("TEST PLAY FAIL BEFORE PREVIOUS VIDEO")
        assert video.change_video(self.path_mask_blackscreen,
                                  self.threshold,
                                  press="KEY_VIDEO_PREV"), ("PREVIOUS VIDEO NOT DISPLAYED ")

    def open(self, path_mask_blackscreen=path_mask_blackscreen):
        """
        open() : open video and detect blackscreen
        :return:
        """
        assert video.open(path_mask_blackscreen,
                          self.threshold, self.timeout_black_screen), ("VIDEO NOT OPEND")



polling_secs_audio = stbt.get_config("audio", "polling_secs_audio", type_=int)
test_secs_audio= stbt.get_config("audio", "test_secs_audio", type_=int)
interval_audio_secs = stbt.get_config("audio", "interval_audio_secs", type_=int)

import  time
class audio_tests(object):

    def __init__(self,
                 polling_secs_audio=polling_secs_audio,
                 test_secs_audio=test_secs_audio):
        self.polling_secs_audio = polling_secs_audio
        self.test_secs_audio=test_secs_audio

    def is_audio(self, polling_secs_audio=polling_secs_audio):
        """

        :param polling_secs_audio:
        check_audio_for_polling_secs
        :return:
        """
        if not audio:
            assert False,"AUDIO DISABLED"
        sc_stbt.debug("LOOKING FOR AUDIO IN", str(polling_secs_audio)+" sec")
        start_time = time.time()
        while time.time() - start_time < polling_secs_audio:
              if stbt.isaudio_present():
                sc_stbt.debug("AUDIO DETECTED")
                return True
        assert False , "ERROR NO AUDIO"

    def is_audio_absent(self, polling_secs_audio=polling_secs_audio, duration_audio_absence = None):
        """
        check if audio is absent
        :return:
        """
        if duration_audio_absence == None:
            duration_audio_absence = stbt.get_config("audio", "duration_audio_absence")
        if not audio:
            assert False, "AUDIO DISABLED"
        sc_stbt.debug("LOOKING FOR AUDIO IN", str(polling_secs_audio)+" sec")
        start_time = time.time()
        while time.time() - start_time < polling_secs_audio:
            if stbt.isaudio_absent():
                time_audio_start_absent = time.time()
                while stbt.isaudio_absent():
                    sc_stbt.debug("audio is suspended", str(time.time() - time_audio_start_absent))
                    if time.time() - time_audio_start_absent  > duration_audio_absence:
                        assert False, "NO AUDIO during "+ str(duration_audio_absence)
        return True


    def is_mute(self,  polling_secs_audio=polling_secs_audio):
        """

               :param polling_secs_audio:
               check_mute_for_polling_secs
               :return:
               """
        if not audio:
            assert False,"AUDIO DISABLED"
        sc_stbt.debug("LOOKING FOR AUDIO IN", str(polling_secs_audio)+" sec")
        start_time = time.time()
        while time.time() - start_time < polling_secs_audio:
              if stbt.isaudio_absent():
                sc_stbt.debug("NO AUDIO DETECTED")
                return True
        assert False , "ERROR AUDIO  "

    def test_audio(self, polling_secs_audio=polling_secs_audio,
                    test_secs_audio=test_secs_audio):
        """

               :param polling_secs_audio:
               wait_until_having_audio
               :return:
               """
        if stbt.wait_until(lambda: not self.is_audio(polling_secs_audio=polling_secs_audio),
                           timeout_secs=test_secs_audio):
            sc_stbt.debug("ERROR AUDIO NOT DETECTED")
            return False
        else:
            sc_stbt.debug("AUDIO DETECTED")

    def test_mute(self, polling_secs_audio=polling_secs_audio,
                   test_secs_audio=test_secs_audio):
        """

               :param polling_secs_audio:
               check_mute_for_polling_secs
               :return:
               """
        if stbt.wait_until(lambda: not self.is_mute(polling_secs_audio=polling_secs_audio),
                           timeout_secs=test_secs_audio):
            sc_stbt.debug("ERROR AUDIO DETECTED")
            return False
        else:
            sc_stbt.debug("NO AUDIO DETECTED")

