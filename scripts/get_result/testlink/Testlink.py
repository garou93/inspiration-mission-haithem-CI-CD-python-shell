#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime

from lxml import etree

# //////////////////////////////////////////////////////////////////////
class Testlink():
    def __init__(self, serveur_url=None, test_plan_id=None, platform_name=None, build_name=None, platform_id=None, build_id=None, testsuite_list=None):
        self.serveur_url    = serveur_url
        self.test_plan_id   = test_plan_id
        self.platform_name  = platform_name
        self.build_name     = build_name
        self.platform_id    = platform_id
        self.build_id       = build_id
        self.testsuite_list = testsuite_list


# //////////////////////////////////////////////////////////////////////
class TestSuite():
    def __init__(self, name=None, testcase_list=None):
        self.name          = name
        self.testcase_list = testcase_list


# //////////////////////////////////////////////////////////////////////
class TestCase():
    def __init__(self, name=None, internal_id=None, external_id=None, result=None, success_ratio=None):
        self.name          = name
        self.internal_id   = internal_id
        self.external_id   = external_id
        self.result        = result
        self.success_ratio = success_ratio




# ----------------------------------------------------------------------
def create_testlink_obj(template_path):
    """create a testlink object"""

    print ">> Create Testlink object"
    tree = etree.parse(template_path)

    # header
    father_node = '/document'
    serveur_url   = parse_xml(tree, father_node, 'serveur_url')
    test_plan_id  = parse_xml(tree, father_node, 'test_plan_id')
    platform_name = parse_xml(tree, father_node, 'platform_name')
    build_name    = parse_xml(tree, father_node, 'build_name')
    platform_id   = parse_xml(tree, father_node, 'platform_id')
    build_id      = parse_xml(tree, father_node, 'build_id')

    testsuite_list = []
    for testsuite in tree.xpath("/document/testsuite"):
        testsuite_name = testsuite.text.strip()
        testcase_list  = []

        for testcase in testsuite.xpath('testcase'):
            # create TestCase object
            father_node = None      #we are alreay at the 'testcase' level !
            testcase = TestCase(
                name          = parse_xml(testcase, father_node, 'name'),
                internal_id   = parse_xml(testcase, father_node, 'id'),
                external_id   = parse_xml(testcase, father_node, 'external_id'),
                result        = parse_xml(testcase, father_node, 'result'),
                success_ratio = parse_xml(testcase, father_node, 'success_ratio')
            )
            testcase_list.append(testcase)

        # create TestSuite object
        testsuite = TestSuite(
            name = testsuite_name,
            testcase_list = testcase_list
        )
        testsuite_list.append(testsuite)

    # create Manifest object
    testlink = Testlink(
        serveur_url     = serveur_url,
        test_plan_id    = test_plan_id,
        platform_name   = platform_name,
        build_name      = build_name,
        platform_id     = platform_id,
        build_id        = build_id,
        testsuite_list  = testsuite_list,
    )

    return testlink


# ----------------------------------------------------------------------
def parse_xml(tree, father_node, field):
    value = None

    # it is not necessary to jump to the father_node
    if father_node is None:
        for sample in tree:
            if sample.tag == field:
                value = sample.text

    # we have to jump to the father_node
    else:
        for node in tree.xpath(father_node):
            for sample in node:
                if sample.tag == field:
                    value = sample.text

    return value



# ----------------------------------------------------------------------
def build_testlink_xml(RESULTS, report_file_h, report_dir, platform_name):

    report_file_h.write("\n\n"+"="*40+' TESTLINK XML FILE '+"="*40+'\n')

    # create testlink_obj from the testlink_results_template.xml file
    template_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testlink_results_template.xml'))
    template = create_testlink_obj(template_file)

    testlink_file = os.path.join(report_dir, 'testlink_results.xml')

    # build_name = date ?
    build_name = re.split("\.",str(datetime.datetime.now()))[0]
    build_name = build_name.replace(' ','_')
    build_name = build_name.replace(':','-')
    build_name = build_name.replace('20','', 1)

    # create XML tree
    root_node = etree.Element("document")

    # header
    etree.SubElement(root_node, 'platform_name').text = platform_name
    etree.SubElement(root_node, 'build_name').text    = build_name
    # ------
    etree.SubElement(root_node, 'serveur_url').text   = template.serveur_url
    etree.SubElement(root_node, 'test_plan_id').text  = template.test_plan_id
    etree.SubElement(root_node, 'platform_id').text   = template.platform_id
    etree.SubElement(root_node, 'build_id').text      = template.build_id

    for testsuite in template.testsuite_list:
        testsuite_node = etree.SubElement(root_node, 'testsuite')
        testsuite_node.set("name", testsuite.name)

        for testcase in testsuite.testcase_list:
            testcase_node = etree.SubElement(testsuite_node, 'testcase')

            # get result and success_ratio from the RESULTS dict
            test_name = convert_test_name(testcase.name)

            result = 'ne'       # not executed
            success_ratio = '0' # not executed
            if RESULTS.has_key(test_name):
                result_list = RESULTS[test_name]
                nb_try = len(result_list)
                nb_ko = 0
                for test in result_list:
                    if test['result'] != '0':
                        nb_ko += 1
                success_ratio = "{}/{}".format(nb_try-nb_ko, nb_try)
                if nb_ko>0:
                    result = 'f'    # failed
                else:
                    result = 'p'    # passed
                report_file_h.write("- {}".format(test_name)+" "*(40-len(test_name))+" {} ({})\n".format(result, success_ratio))
            else:
                report_file_h.write("- {}".format(test_name)+" "*(40-len(test_name))+" ERROR ! not found in the RESULTS tab !\n")

            etree.SubElement(testcase_node, 'name').text          = testcase.name
            etree.SubElement(testcase_node, 'id').text            = testcase.internal_id
            etree.SubElement(testcase_node, 'external_id').text   = testcase.external_id
            etree.SubElement(testcase_node, 'result').text        = result
            etree.SubElement(testcase_node, 'success_ratio').text = success_ratio    

    # write xml tree in a file + reformat
    tree = etree.ElementTree(root_node)
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_string = xml_header+'\n\n'+(etree.tostring(tree, pretty_print=True))
    xml_file = open(testlink_file, "w")
    xml_file.write("%s" % xml_string)
    xml_file.close()
    
    report_file_h.write("\n\n{:<30} : {}\n".format('The testlink XML file is ready', os.path.join(testlink_file)))

    return testlink_file


# ----------------------------------------------------------------------
def convert_test_name(testlink_testname):
    """ convert TESTLINK_testname to STB_TESTER_testname (without the 'test_' prefix !)"""
    convert_table = {
        'Boot'                                          : 'test_boot.py',
        'Standby'                                       : 'test_standby_wakeup.py',
        'Technical informations'                        : 'test_technical_information.py',
        'Portal loading'                                : 'test_portal_loading.py',
        'Launch menu'                                   : 'test_launch_menu.py',
        'Timeshift'                                     : 'test_time_shift.py',
        'Max size UHD'                                  : 'test_max_size_uhd.py',
        'Info banner'                                   : 'test_info_banner.py',
        'Live'                                          : 'test_live_motion.py',
        'PIP'                                           : 'test_pip_from_rcu.py',
        'Zapping'                                       : 'test_swap_zapping_pip.py',
        'PIP disabled on timeshift'                     : 'test_pip_mode_disabling_on_time_shift.py',
        'Tests zapping'                                 : 'test_zapping.py',
        'Tests zapping performance'                     : 'test_zapping_perf.py',
        'Endurance zapping PIP 1s'                      : 'test_endurance_zapping_pip_1s.py',
        'Endurance zapping PIP 2s'                      : 'test_endurance_zapping_pip_2s.py',
        'Endurance zapping PIP 3s'                      : 'test_endurance_zapping_pip_3s.py',
        'Endurance zapping 1s'                          : 'test_endurance_zapping_1s.py',
        'Endurance zapping 2s'                          : 'test_endurance_zapping_2s.py',
        'Endurance zapping 3s'                          : 'test_endurance_zapping_3s.py',
        'Endurance zapping 5s'                          : 'test_endurance_zapping_5s.py',
        'Endurance zapping 10s'                         : 'test_endurance_zapping_10s.py',
        'Numeric zapping 10s'                           : 'test_endurance_zapping_num10s.py',
        'Subtitles from RCU'                            : 'test_subtitles_from_rcu.py',
        'Subtitles from menu'                           : 'test_subtitles_from_menu.py',
        'Navigate in menu item'                         : 'test_guide.py',
        'Navigate through the item on system settings'  : 'test_navigate_through_the_item_on_system.py',
        'Select and validate system settings'           : 'test_select_and_validate_system.py',
        'Select and validate diagnostic settings'       : 'test_select_and_validate_diagnostics.py',
        'Select and validate TV'                        : 'test_select_and_validate_tv.py',
        'Select and validate exist guide'               : 'test_select_validate_exit_guide.py',
        'Exit TV'                                       : 'test_exit_tv.py',
        'Go to Netflix menu'                            : 'test_go_to_netflix.py',
        'Go to Youtube menu'                            : 'test_go_to_youtube.py',
        'Opens a video and detects blackscreen'         : 'youtube_video.py::test_open_video_youtube',
        'Detects motion from Youtube video'             : 'youtube_video.py::test_youtube_motion',
        'Checks video is paused'                        : 'youtube_video.py::test_youtube_pause',
        'Checks video is played'                        : 'youtube_video.py::test_youtube_play',
        'Checks motion is forwarded'                    : 'youtube_video.py::test_youtube_fastforward',
        'Checks motion is rewinded'                     : 'youtube_video.py::test_youtube_rewind',
        'Exits from Youtube'                            : 'youtube_video.py::test_exit_youtube',
        'Sets the power state of the STB standby'       : 'test_set_standby.py',
        'Sets all power ports off'                      : 'test_power_off.py'
    }

    if not convert_table.has_key(testlink_testname):
        print "ERROR ! It's not possible to convert the following TESTLINK_testname to a STB_TESTER_testname !"
        print "--> {}".format(testlink_testname)
        print "please check the table in convert_test_name function !"
        exit(0)

    stbtester_testname = convert_table[testlink_testname].replace('.py','').replace('test_','')
    if '::' in stbtester_testname:
        stbtester_testname = re.split('::',stbtester_testname)[1]

    return stbtester_testname
