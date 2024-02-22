from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from .models import User, OneTimePassword

import random
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class SendMail:
    @staticmethod
    def send_otp(email):
        otp = random.randint(100000, 999999)

        user = User.objects.get(email=email)
        print(user)
        OneTimePassword.objects.create(user=user, code=otp)
        message = EmailMessage(
            subject="verification otp",
            body=f"Hi {user}!, Your one time password is {otp}",
            to=[email],
        )
        message.content_subtype = "html"
        EmailThread(message).start()
