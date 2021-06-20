import smtplib
import os
import sys
import codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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


    header = '<h1 align="center"><font color="blue">Automatic Tests Final Report</font></h1>' \
                     '<a href=http://'+str(sys.argv[3])+'/'+str(sys.argv[4])+'/>Visit our NEW STB-TESTER REPORTING TOOLS</a> ' \

    part2 = MIMEText(header.encode('UTF-8'), 'html', _charset=('UTF-8'))
    msg.attach(part2)
    file = codecs.open('index.html','r','utf-8')
    body = file.read()
    #print body
    part2 = MIMEText(body.encode('UTF-8'), 'html', _charset=('UTF-8'))
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
        print mailing_list
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
