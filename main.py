import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
from getpass import getpass


# setting the necessary variables
send_from = 'emilialechart@wp.pl'
send_to = ['marek.baranski@interia.pl']
send_cc = ['marek.baranski@capgemini.com']
send_bcc = ['maro.baranski@gmail.com']
subject = 'test'
filesToAttach = []
password = getpass("password: ")


def send_mail(send_from, send_to, send_cc, send_bcc, subject, password, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(send_cc) == list
    assert type(send_bcc) == list
    assert type(files) == list

# server startup and logging into e-mail
    server.starttls()
    server.login(send_from, password)

# a loop to send an e-mail - only one address is shown in "To:"
    for eachMail in send_to:
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = 'To: %s\r\n' % eachMail
        msg['cc'] = 'cc: %s\r\n' % COMMASPACE.join(send_cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

# combination all of addresses needed to send an e-mail
        toaddrs = [eachMail] + [send_cc] + [send_bcc]

# attaching an HTML template for sending an e-mail#
        with open("template.html", "r", encoding='utf-8') as f:
            html = f.read()
        msg.attach(MIMEText(html, 'html'))

# attaching all of attachment from list filesToAttach
        for f in filesToAttach:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

# sending an e-mail to every address in the send_to list
        server.sendmail(send_from, toaddrs, msg.as_string())

# closing the connection with the server
    server.close()


# starting the function
send_mail(send_from, send_to, send_cc, send_bcc, subject, password, filesToAttach, server=smtplib.SMTP('smtp.wp.pl', 587))
