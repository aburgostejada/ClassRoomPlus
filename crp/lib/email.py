import os
from urllib import urlencode
import httplib2
import webapp2


class Email:
    def __init__(self):
        self.MAILGUN_DOMAIN_NAME = os.environ['MAILGUN_DOMAIN_NAME']
        self.MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']

    def send_confirmation_message(self, to):
        http = httplib2.Http()
        http.add_credentials('api', self.MAILGUN_API_KEY)

        url = 'https://api.mailgun.net/v3/{}/messages'.format(self.MAILGUN_DOMAIN_NAME)
        data = {
            'from': 'Example Sender <mailgun@{}>'.format(self.MAILGUN_DOMAIN_NAME),
            'to': to,
            'subject': 'This is an example email from Mailgun',
            'text': 'Test message from Mailgun',
            'html': '<html>HTML <strong>version</strong> of the body</html>'
        }
        resp, content = http.request(url, 'POST', urlencode(data))

        if resp.status != 200:
            raise RuntimeError(
                'Mailgun API error: {} {}'.format(resp.status, content))

