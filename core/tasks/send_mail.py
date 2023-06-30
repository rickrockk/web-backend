import smtplib
from email.mime.text import MIMEText


def send_mail(text: str, subject: str, me: str, to: str):
    msg = MIMEText(text)

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to

    with smtplib.SMTP('127.0.0.1:1025') as s:
        s.sendmail(me, [to], msg.as_string())
    return 'Сообщение отправлено!'
