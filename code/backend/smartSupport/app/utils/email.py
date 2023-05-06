import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from flask import current_app as app


def send_email(subject, message, recipient, content_type='text', attachments=None):
    msg = MIMEMultipart()
    msg['From'] = app.config['SENDER_ADDRESS']
    msg['To'] = recipient
    msg['Subject'] = subject

    if content_type == 'html':
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment}')
            msg.attach(part)

    s = smtplib.SMTP(host= app.config['SMTP_SERVER_HOST'], port=app.config['SMTP_SERVER_PORT'])
    s.login(app.config['SENDER_ADDRESS'], app.config['SENDER_PASSWORD'])
    s.send_message(msg)
    s.quit()

    return True