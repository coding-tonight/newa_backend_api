import secrets
import smtplib

from email.message import EmailMessage


def send_mail(sender_email, sender_password, receiver_email, subject):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender_email,
                     sender_password)

        msg = EmailMessage()  # createing email dict or objects

        otp = secrets.token_hex(2)  # generating otp
        msg.set_content(f'''Hi {receiver_email} your otp is {otp}.
                            for one time use only.
                        ''')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        # send otp in the mail
        server.send_message(msg)  # alternative sendmail()
        server.close()

        return otp

    except Exception as exe:
        raise Exception(exe)
