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

import stbt
import sc_stbt

Frame = "video_pause"
class video(object):

    def is_motion(self,
                  path,
                  consecutive_frames,
                  noise_threshold,
                  time_out_detect_motion=None):
        """
        is_motion: detect motion
        :param path: path to the reference template of mask to detect motion
        :param consecutive_frames:considers the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion:timeout for detecting motion
        :return: True when motion detected
                 False when motion not detected
        """
        if time_out_detect_motion is None:
            time_out_detect_motion = stbt.get_config("video", "time_out_detect_motion", type_=int)

        result = False
        sc_stbt.debug("LOOKING FOR MOTION WITHIN", str(time_out_detect_motion)+" sec")
        try:
            stbt.wait_for_motion(timeout_secs=time_out_detect_motion,
                                 consecutive_frames=consecutive_frames,
                                 noise_threshold=noise_threshold,
                                 mask=path)
            result = True
            sc_stbt.debug("MOTION DETECTED", consecutive_frames)
        except:
            sc_stbt.debug("NO MOTION", consecutive_frames)
            pass
        return result


    def test_motion(self,
                  path,
                  consecutive_frames,
                  noise_threshold,
                  time_out_detect_motion,
                  test_secs,
                  interval_secs):
        """
        test_motion: detect motion for test_secs time
        :param path: path to the reference template of mask to detect motion
        :param consecutive_frames:considers the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion:timeout for detecting mmotion
        :param test_secs: Duration of test_motion
        :return: True when motion detected
                 False when motion not detected
        """
        if stbt.wait_until(lambda: not self.is_motion(path,
                                                consecutive_frames,
                                                noise_threshold,
                                                time_out_detect_motion),
                            timeout_secs=test_secs,
                            interval_secs=interval_secs):
            sc_stbt.debug("MOTION NOT DETECTED")
            return False
        else:
            sc_stbt.debug("MOTION DETECTED")
            return True



    def trick_mode_ott(self,
                   path_mask_motion_trickmode,
                   consecutive_frames,
                   noise_threshold,
                   press,
                   index_frame):

        """
        trick_mode: checck if video has forwarded or rewinded
        path_mask_motion_trickmode: mask for detecting motion
        consecutive_frames:Considers the video stream to have motion if there
                                were differences between the specified number of
                                 consecutive frames
        noise_threshold:The amount of noise to ignore.
        press: KEY_FASTFORWARD / KEY_REWIND
        index_frame: indice of frame saved
        True for youtub and netflix
        value return: True or Flase

        """
        sc_stbt.press(press)
        sc_stbt.wait(2)
        if self.is_motion(path_mask_motion_trickmode,
                                consecutive_frames,
                                noise_threshold) == False:
            stbt.save_frame(stbt.get_frame(), str(press) + index_frame + ".png")
            return True
        else:
            sc_stbt.debug("Motion detected")
            return False


    def test_trick_mode_ott(self,
                   path_mask_motion_trickmode,
                   consecutive_frames,
                   noise_threshold,
                   press,
                   occurence=None):
        """
        test_trick_mode: checck if video has forwarded or rewinded
        path_mask_motion_trickmode: mask for detecting motion
        consecutive_frames:Considers the video stream to have motion if there
                                were differences between the specified number of
                                 consecutive frames
        noise_threshold:The amount of noise to ignore.
        press: KEY_FASTFORWARD / KEY_REWIND
        True for youtub and netflix
        value return: True or Flase

        """
        if occurence is None:
            occurence=stbt.get_config("video", "occurence", type_=int)

        assert stbt.wait_until(lambda: self.trick_mode_ott(path_mask_motion_trickmode,
                                                                   consecutive_frames,
                                                                   noise_threshold,
                                                                   press,
                                                                   index_frame="1"),
                                    timeout_secs=8), ("%s1 Has Not Done" % str(press))
        sc_stbt.wait(4)
        if occurence > 1:
            sc_stbt.repeat(lambda: sc_stbt.press(press),
                            occurence=occurence-1)
        assert stbt.wait_until(lambda: self.trick_mode_ott(path_mask_motion_trickmode,
                                                                   consecutive_frames,
                                                                   noise_threshold,
                                                                   press,
                                                                   index_frame="2"),
                                    timeout_secs=8), ("%s2 Has Not Done" % str(press))

        if stbt.match(str(press) + "1.png", stbt.load_image(str(press) +"2.png")):
            sc_stbt.debug(str(press), " HAS Not DONE ")
            return False
        else:
            sc_stbt.debug(str(press), " DONE ")
            return True


    def trick_mode(self,
                   path_mask_motion,
                   consecutive_frames,
                   noise_threshold,
                   press,
                   occurence=None,
                   wait_pause_secs=None,
                   key_pause=None,
                   pause_frame=None,
                   time_out_detect_motion=None,
                   match_parameters=None):
        """
        trick_mode: video check motion is forwarded or rewinded
        scenario: 0) test_pause() : use t test parameters of test_pause() for the pause delay
                     variation:
                  1)press occurence trick_mode-1
                  1) check trickmode is done or not
        :param path_mask_motion:path to the reference template of mask to detect motion
        :param consecutive_frames:onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames.
        :param noise_threshold: The maximum allowed difference between any given templates
        :param press: key press rewind or fastforward (forward)
        :param occurence: number of press key rewin or fastforward
        :param wait_pause_secs:delay pause after press key pause
        :param key_pause:press key pause,for some projects the key pause is the same key play
        :param pause_frame: frame saved after video is paused
        :return:True when trickmode is done
                False when trickmode not done
        """
        if occurence is None:
            occurence=stbt.get_config("video", "occurence", type_=int)
        if wait_pause_secs is None:
            wait_pause_secs=stbt.get_config("video", "wait_pause_secs", type_=int)
        if key_pause is None:
            key_pause=stbt.get_config("video", "key_pause")
        if pause_frame is None:
            pause_frame=eval(stbt.get_config("video", "pause_frame"))

        result = False

        if self.test_pause(path_mask_motion,
                            consecutive_frames,
                            noise_threshold,
                            time_out_detect_motion=20,
                            delay_pause=5,
                            timeout_motion=5,
                            interval_sec_motion=5,
                            wait_pause_secs=wait_pause_secs,
                            key_pause=key_pause,
                            pause_frame=pause_frame,
                            match_parameters=match_parameters):
            sc_stbt.repeat(lambda: sc_stbt.press(press, delay_sec=5),
                           occurence=occurence)
            sc_stbt.wait(5)
            if not stbt.match(Frame+".png"):
                sc_stbt.debug(str(press), " DONE ")
                result = True
        else:
            result = False

        return result


    def retry_press_in_noblackscreen(self,
                                     mask,
                                     press,
                                     threshold=None):
        """
        retry_press_in_noblackscreen: detect black screen else press key
        :param mask:to the reference template of mask to blackscreen
        :param press: press_key
        :param threshold:The maximum allowed difference between any given templates
        :return:true wwhen blackscreen is detected
                 false when blackscrenn is not detected
        """
        if stbt.wait_until(lambda: stbt.is_screen_black(mask=mask,
                                                        threshold=threshold),
                           timeout_secs=20,
                           interval_secs=0):
            return True
        else:
            sc_stbt.press(press)
            return False


    def change_video(self,
                     path,
                     threshold,
                     press):
        """
        change_video: go to next or previous video and detect blackscreen
        :param path:to the reference template of mask to blackscreen
        :param threshold: The maximum allowed difference between any given templates
        :param press:press key: KEY_VIDEO_NEXT or KEY_VIDEO_PREV
        :return:True when video changed and blackscreen detected
                 False when video not changed and blackscreen not detected
        """
        sc_stbt.press(press)
        if stbt.wait_until(lambda: self.retry_press_in_noblackscreen(path,
                                                                     press,
                                                                     threshold),
                           timeout_secs=10,
                           interval_secs=0):
            sc_stbt.debug("BLACK_SCREEN DETECTED AND VIDEO CHANGED")
            return True
        else:
            sc_stbt.debug("VIDEO NOT CHANGED")
            return False


    def open(self,
             path,
             threshold,
             timeout_black_screen=None):
        """
        open : open video and detect black screen
        :param path: to the reference template of mask to blackscreen
        :param threshold:The maximum allowed difference between any given templates
        :return: true when black screen detected
                false when black screen not detected
        """
        if timeout_black_screen is None:
            timeout_black_screen = stbt.get_config("video", "timeout_black_screen", type_=int)
        press = "KEY_OK"
        sc_stbt.press(press)
        if stbt.wait_until(lambda: self.retry_press_in_noblackscreen(path,
                                                                         press,
                                                                         threshold),
                               timeout_secs=timeout_black_screen,
                               interval_secs=2):
            sc_stbt.debug("BLACK_SCREEN DETECTED AND VIDEO OPENED")
            return True
        else:
            sc_stbt.debug("VIDEO NOT OPENED")
            return False


    def play(self,
             mask,
             consecutive_frames,
             noise_threshold,
             time_out_detect_motion,
             timeout_motion,
             interval_sec_motion):
        """
        play: video: check motion is played
        :param mask: path to the reference template of mask to detect motion
        :param consecutive_frames: onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames.
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion: timeout for detecting mmotion
        :param timeout_motion: it is the waiting time for a video in play mode
        :param interval_sec_motion:the time interval for detection if the video is in play mode or not
        :return:True when video played
                  False whend video not played
        """
        sc_stbt.press("KEY_PLAY")
        sc_stbt.debug ("VIDEO PLAY FOR",str(timeout_motion)+" sec")
        sc_stbt.wait(5)
        if stbt.wait_until(lambda: not self.is_motion(mask,
                                                consecutive_frames,
                                                noise_threshold,
                                                time_out_detect_motion),
                            timeout_secs=timeout_motion,
                            interval_secs=interval_sec_motion):


            sc_stbt.debug("VIDEO NOT PLAYED")
            return False
        else:
            sc_stbt.debug("VIDEO PLAYED")
            return True


    def pause(self,
              mask,
              noise_threshold,
              time_out_detect_motion,
              delay_pause,
              interval_sec_motion,
              wait_pause_secs,
              key_pause=None,
              pause_frame=None,
              match_parameters=None):
        """

        :param mask:path to the reference template of mask to detect motion
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion: onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames.
        :param delay_pause: it is the waiting time for a video in pause mode
        :param interval_sec_motion:the time interval for detection if the video is in play mode or not
        :param wait_pause_secs: delay pause after press key_pause
        :param key_pause: press key pause,for some projects the key pause is the same key play
        :param pause_frame:frame saved after video is paused
        :return:when video paused
                 False when video not paused
        """
        if key_pause is None:
            key_pause=stbt.get_config("video", "key_pause")
        if pause_frame is None:
            pause_frame=eval(stbt.get_config("video", "pause_frame"))
        noise_threshold = 0.5
        sc_stbt.press(key_pause)
        sc_stbt.debug("VIDEO PAUSE FOR", str(delay_pause)+" sec")
        sc_stbt.wait(wait_pause_secs)
        sc_stbt.debug ("WAITED AFTER PRESS KEY PAUSE",str(wait_pause_secs)+" sec")
        if stbt.wait_until(lambda: not self.is_pause(mask,
                                                     noise_threshold,
                                                     time_out_detect_motion,
                                                     pause_frame,
                                                     match_parameters=match_parameters),
                                    timeout_secs=delay_pause,
                                    interval_secs=interval_sec_motion):
            sc_stbt.debug("VIDEO NOT PAUSED")
            return False
        else:
            sc_stbt.debug("VIDEO PAUSED")
            #ave a cropped frame to avoid popup appearing "opera Device SDK" in top of frame
            sc_stbt.crop(stbt.get_frame(),
                            region=pause_frame,
                            file_name=Frame)
            return True


    def is_pause(self,
                 mask,
                 noise_threshold,
                 time_out_detect_motion=None,
                 pause_frame=None,
                 match_parameters=None):
        """
        unti function of test_pause
        :param mask: path to the reference template of mask to detect motion
        :param noise_threshold: The maximum allowed difference between any given templates
        :param consecutive_frames: onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames.
        :param checking_secs:timeout for detecting mmotion
        :param frame:frame saved after video is paused
        :return: True when video is paused
                 False when video is not paused
        """
        # detect pause -> consecutive_frames='1/30'
        # True: motion detected unless '1/30'.
        # False: no motion -> '0/30'
        # frame: save screenshot.
        if time_out_detect_motion is None:
            time_out_detect_motion=stbt.get_config("video", "time_out_detect_motion", type_=int)
        if pause_frame is None:
            pause_frame=eval(stbt.get_config("video", "pause_frame"))

        noise_threshold = noise_threshold

        # get frame and save it to be used with frames comparison if not is_motion() fail
        pause_image = stbt.get_frame()
        stbt.save_frame(pause_image, 'pause_image.png')

        if not self.is_motion(mask,
                              consecutive_frames='1/30',
                              noise_threshold=noise_threshold,
                              time_out_detect_motion=time_out_detect_motion):
            return True
        else:
            sc_stbt.wait(1)
            number = 1
            regions = sc_stbt.convert_mask_to_regions(path_mask=mask)
            if regions is None:
                sc_stbt.debug("MASK IS BLACK SCREEN: NO REGIONS")
                return False
            else:
                for region in regions:
                    sc_stbt.crop(pause_image,
                                 region=region,
                                 file_name="cropped_pause_image_" + str(number))
                    cropped_pause_image = stbt.load_image("cropped_pause_image_" + str(number) + ".png")
                    number += 1

                    if not stbt.match(image=cropped_pause_image,
                                      frame=None,
                                      match_parameters=match_parameters,
                                      region=region):
                        sc_stbt.debug("FRAMES COMPARISON: PAUSE NOT DONE")
                        return False
                sc_stbt.debug("FRAMES COMPARISON: PAUSE DONE")
                return True


    def test_play(self,
                   path_mask_motion,
                   consecutive_frames,
                   noise_threshold,
                   time_out_detect_motion=None,
                   delay_pause=None,
                   timeout_motion=None,
                   interval_sec_motion=None,
                   wait_pause_secs=None,
                   key_pause=None,
                   pause_frame=None,
                   match_parameters=None):
        """
        test_play: check moition is played
        scenario: -if moition is detected => video pause ==> video play
                  -else:=> video play
        :param path_mask_motion: path to the reference template of mask to detect motion
        :param consecutive_frames:onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion:timeout for detecting motion
        :param delay_pause:it is the waiting time for a video in pause mode
        :param timeout_motion:it is the waiting time for a video in play mode
        :param interval_sec_motion:the time interval for detection if the video is in play mode or not
        :param wait_pause_secs:delay pause after press key pause
        :param key_pause:press key pause,for some projects the key pause is the same key play
        :param pause_frame:frame saved after video is paused
        :return:True  when video played
                 False when video paused
        """
        if time_out_detect_motion is None:
            time_out_detect_motion=stbt.get_config("video", "time_out_detect_motion", type_=int)
        if delay_pause is None:
            delay_pause=stbt.get_config("video", "delay_pause", type_=int)
        if timeout_motion is None:
            timeout_motion=stbt.get_config("video", "timeout_motion", type_=int)
        if interval_sec_motion is None:
            interval_sec_motion=stbt.get_config("video", "interval_sec_motion", type_=int)
        if wait_pause_secs is None:
            wait_pause_secs=stbt.get_config("video", "wait_pause_secs", type_=int)
        if key_pause is None:
            key_pause=stbt.get_config("video", "key_pause")
        if pause_frame is None:
            pause_frame=eval(stbt.get_config("video", "pause_frame"))

        #time_out_detect_motion or interval_sec_motion must not be greater than timeout_motion
        if interval_sec_motion > timeout_motion:
            interval_sec_motion = time_out_detect_motion
        result = False
        if self.is_motion(path_mask_motion,
                          consecutive_frames,
                          noise_threshold,
                          time_out_detect_motion):
            if self.pause(path_mask_motion,
                            noise_threshold,
                            time_out_detect_motion,
                            delay_pause,
                            interval_sec_motion,
                            wait_pause_secs,
                            key_pause,
                            pause_frame,
                            match_parameters=match_parameters):
                if self.play(path_mask_motion,
                                consecutive_frames,
                                noise_threshold,
                                time_out_detect_motion,
                                timeout_motion,
                                interval_sec_motion):
                    result = True
        else:
            if self.play(path_mask_motion,
                                consecutive_frames,
                                noise_threshold,
                                time_out_detect_motion,
                                timeout_motion,
                                interval_sec_motion):
                result = True
        return result


    def test_pause(self,
                   path_mask_motion,
                   consecutive_frames,
                   noise_threshold,
                   time_out_detect_motion=None,
                   delay_pause=None,
                   timeout_motion=None,
                   interval_sec_motion=None,
                   wait_pause_secs=None,
                   key_pause=None,
                   pause_frame=None,
                   match_parameters=None):
        """
        test_pause: check moition is paused
        scenario: -if moition is not detected => video play ==> video pause
                  -else:=> video pause
        :param path_mask_motion:path to the reference template of mask to detect motion
        :param consecutive_frames:consecutive_frames:onsiders the video stream to have motion if there were
                differences between the specified number of consecutive frames
                This can be:
                a positive integer value, or
                a string in the formx/y, where x is the number of frames with motion detected
                out of a sliding window of y frames.
        :param noise_threshold:The maximum allowed difference between any given templates
        :param time_out_detect_motion:timeout for detecting motion
        :param delay_pause:it is the waiting time for a video in pause mode
        :param timeout_motion: it is the waiting time for a video in play mode
        :param interval_sec_motion: the time interval for detection if the video is in play mode or not
        :param wait_pause_secs:delay pause after press key pause
        :param key_pause:press key pause,for some projects the key pause is the same key play
        :param pause_frame:frame saved after video is paused
        :return:True  when video paused
                 False when video played
        """
        if time_out_detect_motion is None:
            time_out_detect_motion=stbt.get_config("video", "time_out_detect_motion", type_=int)
        if delay_pause is None:
            delay_pause=stbt.get_config("video", "delay_pause", type_=int)
        if timeout_motion is None:
            timeout_motion=stbt.get_config("video", "timeout_motion", type_=int)
        if interval_sec_motion is None:
            interval_sec_motion=stbt.get_config("video", "interval_sec_motion", type_=int)
        if wait_pause_secs is None:
            wait_pause_secs=stbt.get_config("video", "wait_pause_secs", type_=int)
        if key_pause is None:
            key_pause=stbt.get_config("video", "key_pause")
        if pause_frame is None:
            pause_frame=eval(stbt.get_config("video", "pause_frame"))
        #time_out_detect_motion or interval_sec_motion must not be greater than delay_pause
        if time_out_detect_motion > delay_pause:
            time_out_detect_motion = delay_pause
        if interval_sec_motion > delay_pause:
            interval_sec_motion = delay_pause
        result = False
        if self.is_pause(path_mask_motion,
                         noise_threshold,
                         time_out_detect_motion,
                         pause_frame,
                         match_parameters=match_parameters):
            if self.play(path_mask_motion,
                            consecutive_frames,
                            noise_threshold,
                            time_out_detect_motion,
                            timeout_motion,
                            interval_sec_motion):
                if self.pause(path_mask_motion,
                                    noise_threshold,
                                    time_out_detect_motion,
                                    delay_pause,
                                    interval_sec_motion,
                                    wait_pause_secs,
                                    key_pause,
                                    pause_frame,
                                    match_parameters=match_parameters):
                    result = True
        else:
            if self.pause(path_mask_motion,
                                noise_threshold,
                                time_out_detect_motion,
                                delay_pause,
                                interval_sec_motion,
                                wait_pause_secs,
                                key_pause,
                                pause_frame,
                                match_parameters=match_parameters):
                 result = True
        return result


