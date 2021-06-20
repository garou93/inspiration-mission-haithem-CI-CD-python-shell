#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import os
import sys
import re
import shutil
import datetime

from lxml import etree

# ----------------------------------------------------------------------
def html_header_footer(html_handle, header_footer):
    """ Print header and footer """
    if header_footer == "header":
        msg = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>STBTESTER-RESULT</title>
    <img src=\"header.png\" alt=\"\">
</head>\n
"""
    elif header_footer == "footer":
        msg = """
<footer>
</footer>\n
</html>
"""
    html_handle.write(msg)


# ----------------------------------------------------------------------
def html_css_style(html_handle):
    """ Add css informations """
    msg = """
<style>
    body { padding: 0; line-height: 1.5em; font-family: Arial, Georgia, "Times New Roman", Times, serif; font-size: 14px; background: #ffffff; }
    footer { height:40px; }
    h1 { padding-bottom:10px; }
    h2 { font-size:1.2em; font-style:italic; padding-top:30px; margin-bottom:-10px;}

    table                 { border-collapse:collapse; }
    .tab_env              { border:1px solid grey; margin-bottom:20px; }
    .tab_env td           { padding-right:30px; }
    .tab_main             { border-bottom:1px solid grey; }
    .tab_main th          { background-color:#B40404; color:white; font-size:1.1em; font-weight:normal; border-right:1px solid white; }
    .tab_main td          { vertical-align:top; padding-top:8px; }
    .tab_main .col1       { border-right:1px solid grey; padding-right:30px; }
    .tab_main .col2       { border-left:1px solid grey; padding-left:30px; }
    .tab_percent td       { padding-right:30px; }
    .tab_percent .percent { font-weight:bold; }
    .tab_details          { margin: -10px 0 0 20px; }
    .tab_details td       { padding-right:30px; }
    .test_description     { font-style:italic; color:blue; }
</style>\n
"""
    html_handle.write(msg)


# ----------------------------------------------------------------------
def create_html_report_file(info_svn, results, description, project_name, date, radar_file):
    """ Create a HTML report to display
        - the test results
        - the radar.png
        - some additional informations about tests
    """
    current_dir = os.path.abspath(os.path.split(__file__)[0])
    html_result_dir = os.path.join(current_dir, 'report')
    if os.path.isdir(html_result_dir):
        shutil.rmtree(html_result_dir)
    os.makedirs(html_result_dir)
    shutil.copy(os.path.join(current_dir,'header.png'), html_result_dir)
    shutil.copy(radar_file, html_result_dir)

    # init html_file and open a handle on it
    html_filename = 'report.html'
    html_file = os.path.join(html_result_dir, html_filename)
    html_handle = open(html_file, "w")
    body_node = etree.Element("body")

    # print header / title
    html_header_footer(html_handle, 'header')
    html_css_style(html_handle)
    day, hour = re.split('_',date)
    hour = hour.replace('-',':')
    title = 'STB-TESTER {} : {} ({})'.format(project_name, day, hour)
    h1_node = etree.SubElement(body_node, "h1").text = title

    # get svn revisions
    now = re.split("\.",str(datetime.datetime.now()))[0]
    now = now.replace(" "," (")+')'
    table_node = etree.SubElement(body_node, "table")
    table_node.set("class", "tab_env")
    tr_node = etree.SubElement(table_node, "tr")
    td_node = etree.SubElement(tr_node, "td").text = '<b>Report date : </b>'
    td_node = etree.SubElement(tr_node, "td").text = now
    tr_node = etree.SubElement(table_node, "tr")
    td_node = etree.SubElement(tr_node, "td").text = '<b>Environment : </b>'
    td_node = etree.SubElement(tr_node, "td").text = info_svn.env_branch
    td_node = etree.SubElement(tr_node, "td").text = 'svn_'+info_svn.env_rev
    tr_node = etree.SubElement(table_node, "tr")
    td_node = etree.SubElement(tr_node, "td").text = '<b>Trunk : </b>'
    td_node = etree.SubElement(tr_node, "td").text = info_svn.trunk_branch
    td_node = etree.SubElement(tr_node, "td").text = 'svn_'+info_svn.trunk_rev
    tr_node = etree.SubElement(table_node, "tr")
    td_node = etree.SubElement(tr_node, "td").text = '<b>Project : </b>'
    td_node = etree.SubElement(tr_node, "td").text = info_svn.project_branch
    td_node = etree.SubElement(tr_node, "td").text = 'svn_'+info_svn.project_rev

    # create the main table :
    # - col1 : tests results in percent
    # - col2 : radar.png
    table_main = etree.SubElement(body_node, "table")
    table_main.set("class", "tab_main")
    tr_node_main = etree.SubElement(table_main, "tr")
    th_node = etree.SubElement(tr_node_main, "th").text = 'tests'
    th_node = etree.SubElement(tr_node_main, "th").text = 'radar'
    tr_node_main = etree.SubElement(table_main, "tr")
    
    # col1 : tests results in percent
    td_node1 = etree.SubElement(tr_node_main, "td")
    td_node1.set("class", "col1")
    table_node = etree.SubElement(td_node1, "table")
    table_node.set("class", "tab_percent")
    for test_name in sorted(results):
        result_list = results[test_name]
        nb_try = len(result_list)
        ok_percent = nb_ko = nb_ok = 0
        for test in result_list:
            if test['result'] != '0':
                nb_ko += 1
        if nb_try>0:
            nb_ok = int(nb_try-nb_ko)
            ok_percent = (float(nb_ok)/float(nb_try))*100
            ok_percent = round(ok_percent,2)

        tr_node = etree.SubElement(table_node, "tr")
        td_node = etree.SubElement(tr_node, "td").text = test_name
        td_node = etree.SubElement(tr_node, "td").text = '{}/{}'.format(nb_ok, nb_try)
        td_node = etree.SubElement(tr_node, "td")
        td_node.set("class", "percent")
        td_node.text = '{} %'.format(ok_percent)

    # col2 : radar.png
    td_node2 = etree.SubElement(tr_node_main, "td")
    td_node2.set("class", "col2")
    img_node = etree.SubElement(td_node2, "img")
    img_node.set("src", os.path.basename(radar_file))
    img_node.set("style", "width:600px;height:600px;")

    # test details
    div_node = etree.SubElement(body_node, "table")
    for test_name, info in results.items():
        test_info_dict = description[test_name]
        h2_node = etree.SubElement(div_node, "h2").text = test_name
        p_node = etree.SubElement(div_node, "p")
        p_node.set("class", "test_description")
        p_node.text = 'RIGHT_ARROW desc : {}'.format(test_info_dict['desc'])
        table_node = etree.SubElement(div_node, "table")
        table_node.set("class", "tab_details")
        for test in info:
            tr_node = etree.SubElement(table_node, "tr")
            td_node = etree.SubElement(tr_node, "td").text = test['date']
            td_node = etree.SubElement(tr_node, "td").text = test['result']
            td_node = etree.SubElement(tr_node, "td").text = test['msg']

    # cleaning and print in file
    string = etree.tostring(body_node, pretty_print=True)
    string = string.replace("/>",">")
    string = string.replace("&lt;","<")
    string = string.replace("&gt;",">")
    string = string.replace("amp;","")
    string = string.replace("RIGHT_ARROW","&rarr;")
    html_handle.write(string)

    # print footer
    html_header_footer(html_handle, 'footer')

    # close html_file
    html_handle.close()

    print "{:<30} : {}\n".format('The HTML report file is ready', html_file)
