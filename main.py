import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
from getpass import getpass

send_from = 'emilialechart@wp.pl'
send_to = ['marek.baranski@interia.pl']
text = 'Hello world'
subject = 'test'
password = getpass("password: ")


def send_mail(send_from, send_to, subject, text, password, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(files) == list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    server.starttls()
    server.login(send_from, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()


send_mail(send_from, send_to, subject, text, password, files=[], server=smtplib.SMTP('smtp.wp.pl', 587))
