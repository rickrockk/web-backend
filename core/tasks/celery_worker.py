from celery import Celery
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv('.env')

celery = Celery(__name__)
celery.conf.broker_url=os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend=os.environ.get("CELERY_RESULT_BACKEND")

@celery.task(name="send_mail")
def send_mail(me: str, to: str, text: str, subject: str):
    msg = MIMEText(text)

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to

    with smtplib.SMTP('mail:1025') as s:
        s.sendmail(me, [to], msg.as_string())
    return 'Сообщение отправлено!'

    