import smtplib
import mimetypes
import os
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, subject, text, attachments):
    addr_from = os.getenv('FROM')
    password = os.getenv('PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = email
    msg['Subject'] = subject

    process_attachments(msg, attachments)

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(os.getenv('HOST'), int(os.getenv('PORT')))
    server.login(addr_from, password)

    server.send_message(msg)
    server.quit()

    return True


def process_attachments(msg, attachments):
    for elem in attachments:
        if os.path.isfile(elem):
            attach_file(msg, elem)
        elif os.path.exists(elem):
            dir = os.listdir(elem)
            for file in dir:
                attach_file(msg, elem + '/' + file)


def attach_file(msg, file):
    attach_types = {
        'text': MIMEText,
        'image': MIMEImage,
        'audio': MIMEAudio
    }

    filename = os.path.basename(file)
    ctype, encoding = mimetypes.guess_type(file)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)
    with open(file, mode='rb' if maintype != 'text' else 'r') as infile:
        if maintype in attach_types:
            file = attach_types[maintype](infile.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(infile.read())
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)