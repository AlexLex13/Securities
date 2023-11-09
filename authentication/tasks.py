import socket

import dramatiq
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .utils import account_activation_token


@dramatiq.actor
def sent_activate_mail(user, domain):
    email_body = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }

    link = reverse('activate', kwargs={
        'uidb64': email_body['uid'], 'token': email_body['token']})

    email_subject = 'Activate your account'

    activate_url = 'http://' + domain + link

    sent_mail_count = 0
    while sent_mail_count != 1:
        try:
            sent_mail_count = send_mail(
                email_subject,
                'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                'noreply@semycolon.com',
                [user.email],
                fail_silently=False,
            )
        except socket.gaierror:
            pass
