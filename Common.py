import typing
from smtplib import SMTP
from email.mime.text import MIMEText


class sender_email_account:
    def __init__(self, host: str, port: int, username: str, password: str, description: str, daily_send_limit: int):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.description = description
        self.daily_send_limit = daily_send_limit


class email:
    def __init__(self, subject: str, message: str):
        self.subject = subject
        self.message = message


class target:
    def __init__(self, email_address: str, name: str, source: str, phone: str):
        self.email_address = email_address
        self.name = name
        self.source = source
        self.phone = phone
        self.already_sent = []

    def add_sent_email(self, email_hash_md5, email_times):
        sent_email = {
            "email_hash_md5": email_hash_md5,
            "email_times": email_times
        }
        self.already_sent.append(sent_email)


class email_sender:
    def __init__(self, destination_list: typing.List[target], sender_list: typing.List[sender_email_account],
                 email_content: email):
        self.destination_list = destination_list
        self.sender_list = sender_list
        self.email_content = email_content

        self.current_sender = sender_list[0]

    def _construct_mime_message(self):
        mime_message = MIMEText(self.email_content.message)
        mime_message["Subject"] = self.email_content.subject
        mime_message["From"] = self.current_sender.username
        return mime_message

    def start_sending(self):
        with SMTP(self.current_sender.host, self.current_sender.port) as server:
            server.set_debuglevel(2)

            # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be
            # encrypted
            server.ehlo()  # Identify yourself to an ESMTP server using EHLO
            if server.has_extn('STARTTLS'):
                print("STARTTLS extension is supported.")
                server.starttls()
            else:
                print("STARTTLS extension is not supported.")
            server.ehlo()  # re-identify ourselves as an encrypted connection

            try:
                server.login(self.current_sender.username, self.current_sender.password)
            except Exception as e:
                raise Exception(f"Login error: {e}")

            mime_message = self._construct_mime_message()
            for index, destination in enumerate(self.destination_list):
                mime_message["To"] = destination.email_address
                result = []
                # result = server.send_message(mime_message)
                print(f"({index+1}/{len(self.destination_list):<5})\t{mime_message['From']:<10} -> {mime_message['To']:<20}\t{result}")
