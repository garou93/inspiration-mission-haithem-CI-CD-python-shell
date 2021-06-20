import smtplib
import os
import sys
import codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import time
import bs4


def notification_mail(emailfrom,emailto, subject,body):
    emailfrom = "no-reply.stb-tester@haithem.com"
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto

    if subject is None:
        subject = "subject of test"

    msg["Subject"] = subject

    if body is None:
        body = 'this is a test message'

    current_directory = str(sys.argv[6])
    name_tag = "RO_sagem-stbt-v2_"
    if name_tag in current_directory:
        current_directory = current_directory.replace(name_tag, " ")
    else:
        current_directory = "BO: Official_Branche"
   

    header = '<h1 align="center"><font color="blue">Automatic Tests Final Report</font></h1>' \
                     '<a href=http://'+str(sys.argv[3])+'/'+str(sys.argv[4])+'/>Visit our NEW STB-TESTER REPORTING TOOLS</a> ' \
    #
    # part2 = MIMEText(header.encode('UTF-8'), 'html', _charset=('UTF-8'))
    # msg.attach(part2)

    # check if it's a duration (xx:xx:xx)
    def is_time_format(input):
        try:
            time.strptime(input, '%H:%M:%S')
            return True
        except ValueError:
            return False

    # get durations division
    with open('index_all.html') as fp:
        soup = bs4.BeautifulSoup(fp, "html.parser")
    duration = []
    for content in soup.find_all("td"):
        if is_time_format(content.text):
            duration.append(content.text)

    #calculate tests duration
    totalSecs = 0
    for tm in duration:
        timeParts = [int(s) for s in tm.split(':')]
        totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
    totalSecs, sec = divmod(totalSecs, 60)
    hr, min = divmod(totalSecs, 60)

    total_tests_duration = "%02d:%02d:%02d" % (hr, min, sec)

    file = codecs.open('index_all.html','r','utf-8')
    body2 = file.read()
    success_number = 0
    fail_number = 0
    error_number = 0
    total_number = 1

    success_number = file.read().count("Success<")
    total_tests_duration = "%02d:%02d:%02d" % (hr, min, sec)

    file = codecs.open('index_all.html','r','utf-8')
    fail_number= file.read().count("Fail<")
    total_tests_duration = "%02d:%02d:%02d" % (hr, min, sec)

    file = codecs.open('index_all.html','r','utf-8')
    error_number= file.read().count("Error<")
    total_number= success_number + fail_number + error_number
    file.close()
    file.close()
    file.close()

    file = codecs.open('index.html','r','utf-8')
    body = file.read()

    body = body.replace('success_number', str(success_number)+'/'+str(total_number))
    body = body.replace('fail_number', str(fail_number)+'/'+str(total_number))
    body = body.replace('error_number', str(error_number)+'/'+str(total_number))
    body = body.replace('success_percentage', str(round((float(success_number) / total_number)*100,2)))
    body = body.replace('fail_percentage', str(round((float(fail_number) / total_number) * 100,2)))
    body = body.replace('error_percentage', str(round((float(error_number) / total_number) * 100,2)))
    body = body.replace('To_be_replaced_with_tests_duration', total_tests_duration)
    try:
        body = body.replace('To_be_replaced_with_version', str(sys.argv[8]))
    except:
        try:
            body = body.replace('To_be_replaced_with_version', str(sys.argv[9]))
        except:
            body = body.replace('To_be_replaced_with_version', "NOT_DEFINED")

    body = body.replace('To_be_replaced_with_Tag_STB_Tester', current_directory)
    body = body.replace('To_be_replaced_with_Sanity', str(sys.argv[7]))
    body = body.replace('unknown location', str(sys.argv[5]).replace("_", " "))
    file.close()
    file = codecs.open('index.html','w','utf-8')
    file.write(body)
    file.close()
    body = body.replace('a href="', 'a href="http://' + str(sys.argv[3]) + '/' + str(sys.argv[4]) + '/')
    # Define the image's ID as referenced above

    part2 = MIMEText(body.encode('UTF-8'), 'html', _charset=('UTF-8'))

    if sys.argv[10] == "1":
        #Traitement
        file = codecs.open('index_all.html','r','utf-8')
        body2 = file.read()
        body2 = body2.replace('success_number', str(success_number)+'/'+str(total_number))
        body2 = body2.replace('fail_number', str(fail_number)+'/'+str(total_number))
        body2 = body2.replace('error_number', str(error_number)+'/'+str(total_number))
        body2 = body2.replace('success_percentage', str(round((float(success_number) / total_number)*100,2)))
        body2 = body2.replace('fail_percentage', str(round((float(fail_number) / total_number) * 100,2)))
        body2 = body2.replace('error_percentage', str(round((float(error_number) / total_number) * 100,2)))
        body2 = body2.replace('To_be_replaced_with_tests_duration', total_tests_duration)
        try:
            body2 = body2.replace('To_be_replaced_with_version', str(sys.argv[8]))
        except:
            try:
                body2 = body2.replace('To_be_replaced_with_version', str(sys.argv[9]))
            except:
                body2 = body2.replace('To_be_replaced_with_version', "NOT_DEFINED")

        body2 = body2.replace('To_be_replaced_with_Tag_STB_Tester', current_directory)
        body2 = body2.replace('To_be_replaced_with_Sanity', str(sys.argv[7]))
        body2 = body2.replace('unknown location', str(sys.argv[5]).replace("_", " "))
        file.close()
        file = codecs.open('index_all.html','w','utf-8')
        file.write(body2)
        file.close()
        body2 = body2.replace('a href="', 'a href="http://' + str(sys.argv[3]) + '/' + str(sys.argv[4]) + '/')
        # Define the image's ID as referenced above

        part2 = MIMEText(body.encode('UTF-8'), 'html', _charset=('UTF-8'))
        #Traitement

        r = requests.post("http://127.0.0.1:8080/VALID1", data={"body" : body2.split("<h1>")[1] , "idTest" : sys.argv[11]})
        print(r.status_code, r.reason , r.text)
    else:
        pass
    msg.attach(part2)

    # display the report.html in the body section
    if os.path.isfile('report/report.html'):
        part1 = MIMEText(header.encode('UTF-8'), 'html', _charset=('UTF-8'))
        msg.attach(part1)
        file = codecs.open('report/report.html','r','utf-8')
        body = file.read()
        #print body
        part2 = MIMEText(body.encode('UTF-8'), 'html', _charset=('UTF-8'))
        msg.attach(part2)

    #file_size = os.path.getsize(fileToSend)
    # Do not send attachments bigger than 1 MB
    """
    if file_size < 1048577:
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        try:
            if maintype == "text":
                fp = open(fileToSend)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(fileToSend, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(fileToSend, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()

        except:
            return False
       """

    # add an attachement : radar-chart.png
    radar_filename = "radar-chart.png"
    radar_filepath = os.path.join("report", radar_filename)
    if os.path.isfile(radar_filepath):
        attachment = open(radar_filepath, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % radar_filepath)
        msg.attach(part)

    server = smtplib.SMTP("10.66.236.14")
    try:
        mailing_list = str(sys.argv[1])
        if ";" in mailing_list:
            liste_email = mailing_list.split(";")
            for mail in liste_email:
                server.sendmail(emailfrom,mail, msg.as_string())
        else:
            server.sendmail(emailfrom, emailto, msg.as_string())
    except:
        return False
    server.quit()
    return True


notification_mail("no-reply.stb-tester@haithem.com",emailto= str(sys.argv[1]),subject = str(sys.argv[2]) , body = None)
