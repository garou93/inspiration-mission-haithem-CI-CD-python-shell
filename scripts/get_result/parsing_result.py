#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import os
import re
import sys
import shutil
from html_report.create_html import create_html_report_file
from testlink.Testlink import build_testlink_xml

import numpy as np
import pylab as plt


# ----------------------------------------------------------------------
class Radar(object):
    """https://openclassrooms.com/forum/sujet/radar-chart"""
    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            rect = [0.10, 0.10, 0.80, 0.80]

        self.nb_test = len(titles)
        self.angles = [a if a <=360.0 else a - 360.0 for a in np.arange(90, 90+360, 360.0/self.nb_test)]
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) for i in range(self.nb_test)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=12)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, 12), angle=angle, labels=label, fontsize=8)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 10)

    def plot(self, values, *args, **kw):
            angle  = np.deg2rad(np.r_[self.angles, self.angles[0]])
            values = np.r_[values, values[0]]
            self.ax.plot(angle, values, *args, **kw)


# ----------------------------------------------------------------------
class Info_svn():
    """Class Env_rev to store the svn informations about the 
        stb-tester environment
    """
    def __init__(self, env_branch=None, env_rev=None, trunk_branch=None, trunk_rev=None, project_branch=None, project_rev=None):
        """Class Env_rev constructor with attributes
        """
        self.env_branch     = env_branch
        self.env_rev        = env_rev
        self.trunk_branch   = trunk_branch
        self.trunk_rev      = trunk_rev
        self.project_branch = project_branch
        self.project_rev    = project_rev


# ----------------------------------------------------------------------
def get_param():
    """
        get the result_dir, project_name, date
        from the given parameter (~/Desktop/Results)
    """
    try:
        result_dir = os.path.abspath(sys.argv[1])
        if not os.path.isdir(result_dir):
            print "ERROR ! This result_dir doesn't exist : {}".format(result_dir)
            exit(1)
    except IndexError:
        print "ERROR ! Missing param : result_dir"
        print "Usage : parsing_result.py <result_dir>"
        exit(1)

    if not 'index.html' in os.listdir(result_dir):
        print "ERROR ! The result_dir in wrong : {}".format(result_dir)
        print "Please set result_dir=<MAIN_DIR>/{project}/{runtime}"
        exit(1)

    date = re.split('/',result_dir)[-1]
    project_name = re.split('/',result_dir)[-2]

    return result_dir, project_name, date


# ----------------------------------------------------------------------
def get_test_description(full_test_name):
    """
        read the .py file to get the test description
    """
    # init
    test_desc = None

    # specific case for the 'trunk' tests
    if '::' in full_test_name:
        full_test_name = re.split('::',full_test_name)[0]
    
    filepath = os.path.join(project_dir, 'tests', full_test_name)
    if not os.path.isfile(filepath):
        filepath = os.path.join(project_dir, '../trunk', full_test_name)

    if os.path.isfile(filepath):
        with open(filepath, "r") as fich:
            for line in fich:
                if line.startswith('#'):
                    test_desc=line.replace('#','')
                    test_desc=test_desc.replace('\n','')
                    test_desc.strip()
                    break
    else:
        print 'Warning ! The following file is not found ! {}'.format(filepath)

    if test_desc is None:
        test_desc='[ not found in {} !!! ]'.format('projects'+re.split('projects',filepath)[1])
    
    return test_desc


# ----------------------------------------------------------------------
def get_results(result_dir, project_dir, report_file_h):
    """
        Build the RESULTS dictionnary parsing the STBT result files
        Build the DESCRIPTIONS dictionnary (each test is associated with its description)
    """
    RESULTS = {}         # main 'RESULTS' dictionnary = { test_name ; test_results }
    DESCRIPTIONS = {}    # main 'DESCRIPTIONS' dictionnary = { test_name ; test_description }

    # loop on each test result
    for test_date in [x for x in sorted(os.listdir(result_dir))]:

        # build the test_dir : Results/alticeus/<main_date>/<date>
        test_dir = os.path.join(result_dir, test_date)

        regexp = r"(^\d{4}-\d{2}-\d{2})"
        if os.path.isdir(test_dir) and re.match(regexp, test_date):
            # TEST_NAME : read the test-name file
            #   Results/alticeus/<main_date>/<date>/test-name
            filepath = os.path.join(test_dir, 'test-name')
            with open(filepath, "r") as fich:
                full_test_name = fich.readlines()[0].replace('\n','')
                test_name = os.path.basename(full_test_name).replace('.py','')
                test_name = re.split('::',test_name)[-1]

            # TEST_RESULT : read the exit-status file
            #   Results/alticeus/<main_date>/<date>/exit-status
            filepath = os.path.join(test_dir, 'exit-status')
            with open(filepath, "r") as fich:
                test_result = fich.readlines()[0].replace('\n','')

            # TEST_MSG : read the failure-reason file
            #   Results/alticeus/<main_date>/<date>/failure-reason
            filepath = os.path.join(test_dir, 'failure-reason')
            with open(filepath, "r") as fich:
                test_msg = fich.readlines()[0].replace('\n','')

            # TEST_DESCRIPTION : read the .py file to get the test description
            test_desc = get_test_description(full_test_name)

            # build a dictionnary for the current test with date / result / msg
            test_dict = {
                'name':test_name,
                'date':test_date,
                'result':test_result,
                'msg':test_msg
            }

            # build a dictionnary for the current test with full_test_name / test_description
            test_info_dict = {
                'full_test_name':full_test_name,
                'desc':test_desc
            }

            # re-format test_name to create the disp_test_name
            disp_test_name = test_name.replace('test_','')
            if '_youtube' in disp_test_name:
                disp_test_name = 'youtube_'+disp_test_name.replace('_youtube','')

            # add the test_dict in the main 'RESULTS' dictionnary, with 'test_name' as key
            if RESULTS.has_key(disp_test_name):
                current_list = RESULTS[disp_test_name]
                current_list.append(test_dict)
                RESULTS[disp_test_name] = current_list
            else:
                RESULTS[disp_test_name] = [test_dict]
            
            if not DESCRIPTIONS.has_key(disp_test_name):
                DESCRIPTIONS[disp_test_name] = test_info_dict

            report_file_h.write('{} | {:<40} | {} | {}\n'.format(test_date, test_name, test_result, test_msg))

    return RESULTS, DESCRIPTIONS


# ----------------------------------------------------------------------
def build_radar(RESULTS, report_file_h, report_dir):
    """
        Build the radar from the tests resuls in percent
    """
    # init
    test_list  = []
    label_list = []
    value_list = []
    label_flag = 0

    # print details
    tmp_tab = []
    report_file_h.write("\n\n"+"="*40+' DETAILS '+"="*40)
    for test_name in sorted(RESULTS, reverse=True):
        result_list = RESULTS[test_name]
        for test in result_list:
            tmp_tab.append('  * {} : {:<2} ({})\n'.format(test['date'], test['result'], test['msg']))
        tmp_tab.append('\n'+test_name+'\n')
    for line in reversed(tmp_tab):
        report_file_h.write(line)

    # build radar
    fig = plt.figure(figsize=(9,9))
    tmp_tab = []
    report_file_h.write("\n\n"+"="*40+' RADAR '+"="*40+'\n')
    for test_name in sorted(RESULTS, reverse=True):
        result_list = RESULTS[test_name]
        nb_try = len(result_list)
        ok_percent = nb_ko = 0
        for test in result_list:
            if test['result'] != '0':
                nb_ko += 1

        if nb_try>0:
            ok_percent = float(nb_try-nb_ko)/float(nb_try)
        tmp_tab.append('{:<40} \t ok={}/{} \t {}%\n'.format(test_name, (nb_try-nb_ko), nb_try, ok_percent*100))

        test_list.append(test_name)
        value_list.append(ok_percent*10)

        if label_flag == 0:
            label_list.append(["10%","20%","30%","40%","50%","60%","70%", "80%", "90%", "100%"])
            label_flag = 1
        else:
            label_list.append(["", "", "", "", "", "", "", "", "", ""])

    for line in reversed(tmp_tab):
        report_file_h.write(line)

    radar = Radar(fig, test_list, label_list)
    radar.plot(value_list, lw=2, color="b", alpha=0.4, label="version1")

    radar_filename = 'radar-chart.png'
    radar_file = os.path.join(report_dir, radar_filename)
    plt.savefig(radar_file, facecolor='white')
    #~ plt.show()
    report_file_h.write("\n\n{:<30} : {}\n".format('The radar is ready', os.path.join(report_dir, radar_file)))

    return radar_file


# ----------------------------------------------------------------------
def get_svn_info(folder):
    """Get svn revision for a given local folder"""

    cmd = 'svn info {}'.format(folder)
    svn_info = re.split('\n',os.popen(cmd, "r").read())
    for line in svn_info:
        if line.startswith('URL'):
            branch = re.split(' ',line)[-1]
        elif line.startswith('Last Changed Rev'):
            version = re.split(' ',line)[-1]
    return branch, version


# ----------------------------------------------------------------------
def get_platform_name(project_name):
    """ convert project_name to the associated platform_name"""
    convert_table = {
        'alticeus'  : 'm384us'
    }

    if not convert_table.has_key(project_name):
        print "ERROR ! It's not possible to convert the following project_name to the associated platform_name !"
        print "--> {}".format(project_name)
        print "please check the table in get_platform_name function !"
        exit(0)

    return convert_table[project_name]



# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    """
        MAIN FUNCTION
        - build the RESULTS and DESCRIPTIONS dictionnaries
        - build the radar.png file
        - build the report.log file
        - call the 'create_html_report_file' function to create the report.html
    """
    # get { result_dir, project_name, date } from the given param
    result_dir, project_name, date = get_param()

    # create report_file
    report_dir = os.path.abspath(os.path.split(__file__)[0])
    report_filename = 'report.log'
    report_file_h = open(os.path.join(report_dir, report_filename), "w")
    root_dir = re.split('projects', report_dir)[0]
    trunk_dir = os.path.join(root_dir, 'projects', 'trunk')
    project_dir = os.path.join(root_dir, 'projects', project_name)

    # build the 'ENV' dictionnary (svn_rev for root_dir and project_dir)
    branch_e, version_e = get_svn_info(root_dir)
    branch_t, version_t = get_svn_info(trunk_dir)
    branch_p, version_p = get_svn_info(project_dir)

    report_file_h.write('-'*120+'\n')
    report_file_h.write('project_name : {}\n'.format(project_name))
    report_file_h.write('date         : {}\n'.format(date))
    report_file_h.write('environment  : {} --> svn_{}\n'.format(branch_e, version_e))
    report_file_h.write('project      : {} --> svn_{}\n'.format(branch_p, version_p))
    report_file_h.write('-'*120+'\n')

    # build the 'RESULTS' main dictionnary 
    RESULTS, DESCRIPTIONS = get_results(result_dir, project_dir, report_file_h)

    INFO_SVN = Info_svn(
        env_branch     = branch_e,
        env_rev        = version_e,
        trunk_branch   = branch_t,
        trunk_rev      = version_t,
        project_branch = branch_p,
        project_rev    = version_p
    )
    
    # build the radar
    radar_file = build_radar(RESULTS, report_file_h, report_dir)

    # build the testlink_xml file
    platform_name = get_platform_name(project_name)
    build_testlink_xml(RESULTS, report_file_h, report_dir, platform_name)

    # close report_file
    report_file_h.write("{:<30} : {}\n".format('The report.log file is ready', os.path.join(report_dir, report_filename)))
    report_file_h.close()
    os.system('cat {}'.format(os.path.join(report_dir, report_filename)))

    # create html file
    create_html_report_file(INFO_SVN, RESULTS, DESCRIPTIONS, project_name, date, radar_file)

    # move the report.log in html_report/report/
    shutil.copy(os.path.join(report_dir, report_filename), os.path.join(report_dir, 'html_report', 'report', report_filename))
