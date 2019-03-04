import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
from getpass import getpass

send_from = 'emilialechart@wp.pl'
send_to = ['maro.baranski@gmail.com']
send_cc = ['marek.baranski@capgemini.com']
send_bcc = ['marek.baranski@interia.pl']
subject = 'test'
files = []
password = getpass("password: ")


def send_mail(send_from, send_to, send_cc, send_bcc, subject, password, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(send_cc) == list
    assert type(send_bcc) == list
    assert type(files) == list

    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] = COMMASPACE.join(send_cc)
    msg['Bcc'] = COMMASPACE.join(send_bcc)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    with open("template.html", "r", encoding='utf-8') as f:
        html = f.read()
    msg.attach(MIMEText(html, 'html'))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    server.starttls()
    server.login(send_from, password)
    server.sendmail(send_from, send_to + send_cc + send_bcc, msg.as_string())
    server.close()


send_mail(send_from, send_to, send_cc, send_bcc, subject, password, files, server=smtplib.SMTP('smtp.wp.pl', 587))
