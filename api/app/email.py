from django.core.mail import send_mail
from django.template.loader import get_template


# verify email
class SendMail:
    def __init__(self, first_name, last_name, to_mail):
        self.first_name = first_name
        self.last_name = last_name
        self.to_mail = to_mail

    @staticmethod
    def get_send_mail():
        return 'send@gmail.com'

    def send_verify_mail(self, subject):
        context = {
            'first': self.first_name,
            'last_name': self.last_name,
        }
        template = get_template('verify_email.html').render(context)

        send_mail(
            subject,
            None,
            self.get_send_mail(),
            [self.to_mail],
            fail_silently=False,
            html_message=template
        )
