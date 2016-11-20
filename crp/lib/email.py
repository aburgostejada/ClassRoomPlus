from urllib import urlencode
import os
import httplib2
from flask import render_template

from crp.lib.security import Security


class Email:
    def __init__(self):
        self.MAILGUN_DOMAIN_NAME = os.environ['MAILGUN_DOMAIN_NAME']
        self.MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']

    def send_confirmation_message(self, to):
        http = httplib2.Http()
        http.add_credentials('api', self.MAILGUN_API_KEY)

        token = Security.generate_confirmation_token(to)

        url = 'https://api.mailgun.net/v3/{}/messages'.format(self.MAILGUN_DOMAIN_NAME)
        data = {
            'from': 'ClassRoom+ <noreply@{}>'.format(self.MAILGUN_DOMAIN_NAME),
            'to': to,
            'subject': 'Required: Please verify your email address for your ClassRoom+ account',
            'text': 'Test message from Mailgun',
            'html':  render_template("confirmation_email.html", url="http://crplus.net/confirm/"+token)
        }
        resp, content = http.request(url, 'POST', urlencode(data))

        if resp.status != 200:
            raise RuntimeError(
                'Mailgun API error: {} {}'.format(resp.status, content))

