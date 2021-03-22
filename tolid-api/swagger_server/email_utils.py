import email.utils
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailUtils:
    @staticmethod
    def get_requests_pending():
        requests_pending_html = MailUtils.__get_html_from_template('email_requests_pending')
        url = f"{os.environ['TOLID_URL']}"
        requests_pending_html = requests_pending_html.format(url=url)
        subject = "ToLID requests pending"
        return requests_pending_html, subject

    @staticmethod
    def __get_html_from_template(file_name):
        base_dir = os.path.dirname(__file__)
        path_template = os.path.abspath(os.path.join(base_dir, f'templates/{file_name}.html'))
        f = open(path_template, 'r')
        html = f.read()
        f.close()
        return html

    @staticmethod
    def send(body_html, subject, to, images=[]):
        sender = os.environ['MAIL_SENDER']
        sender_name = os.environ['MAIL_SENDER_NAME']
        user_name = os.environ['MAIL_USERNAME_SMTP']
        password = os.environ['MAIL_PASSWORD_SMTP']
        host = os.environ['MAIL_HOST']
        port = int(os.environ['MAIL_PORT'])

        msg_root = MIMEMultipart('related')

        msg_alternative = MIMEMultipart('alternative')
        msg_root['Subject'] = subject
        msg_root['From'] = email.utils.formataddr((sender_name, sender))
        msg_root['To'] = to
        msg_root.preamble = 'Multi-part message in MIME format.'
        msg_root.attach(msg_alternative)

        msg_text = MIMEText('Alternative plain text message.')
        msg_alternative.attach(msg_text)

        msg_text = MIMEText(body_html, 'html')
        msg_alternative.attach(msg_text)

        base_dir = os.path.dirname(__file__)
        path_image = os.path.abspath(os.path.join(base_dir, 'templates/mail_header.png'))
        fp = open(path_image, 'rb')  # Read image
        msg_image = MIMEImage(fp.read())
        fp.close()

        msg_image.add_header('Content-ID', '<image1>')
        msg_root.attach(msg_image)

        for image in images:
            path_image = os.path.abspath(os.path.join(base_dir, 'templates/' + image))
            fp = open(path_image, 'rb')
            msg_image = MIMEImage(fp.read())
            fp.close()
            msg_image.add_header('Content-ID', f"<{image}>")
            msg_root.attach(msg_image)

        if host:
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            if user_name and password:
                server.login(user_name, password)
            server.sendmail(sender, to, msg_root.as_string())
            server.quit()
