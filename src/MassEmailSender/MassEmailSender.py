import os.path
import typing
from . import jsonParser
import json
from smtplib import SMTP
from email.mime.text import MIMEText

"""
TODO:
0. import argparse
1. Check Daily limit - save to local or better yet - remotely.
2. Spam Checker.
3. Add history to email that's already sent out. In Email Json or different location
"""


def parser_decorator(func):
    """
    :param func: has to take arguments (filename: str, json_file: json = None)
    :return: filled json_file with result of json.load()
    """

    def wrapper(*args, **kwargs):
        if os.path.isfile(args[0]):
            with open(args[0]) as file:
                kwargs["json_file"] = json.load(file)
            return func(*args, **kwargs)
        else:
            raise Exception(f"{args[0]} doesn't exist, exit...")

    return wrapper


@parser_decorator
def parse_sender_data(filename: str, json_file: json = None) -> typing.List[jsonParser.sender_email_account]:
    """
    :param json_file: Placeholder for decorator
    :param filename: sender list file
    :return: sender list of email_account
    """

    sender_list = []
    try:
        for email_sender in json_file["email_sender_list"]:
            host = email_sender["host"]
            port = int(email_sender["port"])
            username = email_sender["username"]
            password = email_sender["password"]
            description = email_sender["description"]
            daily_send_limit = int(email_sender["daily_send_limit"])
            email_account = jsonParser.sender_email_account(host, port, username, password, description,
                                                            daily_send_limit)
            sender_list.append(email_account)
    except KeyError as e:
        raise Exception(f"Parsing error: Missing input from {filename} - {e}")

    return sender_list


@parser_decorator
def parse_email_to_send(filename: str, json_file: json = None) -> jsonParser.email:
    """
    :param json_file: Placeholder for decorator
    :param filename: Email with subject and message
    :return: sender list of email_account
    """
    try:
        subject = json_file["subject"]
        message = json_file["message"]
        email = jsonParser.email(subject, message)
    except KeyError as e:
        raise Exception(f"Parsing error: Missing input from {filename} - {e}")

    return email


@parser_decorator
def parse_destination_list(filename: str, json_file: json = None):
    """
    :param json_file: Placeholder for decorator
    :param filename: target list file
    :return: sender list of email_account
    """
    destination_list = []
    try:
        for data in json_file["email_list"]:
            email_address = data["email_address"]
            name = data["name"]
            source = data["source"]
            phone = data["phone"]
            destination = jsonParser.target(email_address, name, source, phone)
            for email in data.get("already_sent", []):
                email_hash_md5 = email['email_hash_md5']
                email_times = email['email_times']
                destination.add_sent_email(email_hash_md5, email_times)
            destination_list.append(destination)
    except KeyError as e:
        raise Exception(f"Parsing error: Missing input from {filename} - {e}")

    return destination_list


class email_worker:
    def __init__(self, destination_list: typing.List[jsonParser.target],
                 sender_list: typing.List[jsonParser.sender_email_account],
                 email_content: jsonParser.email, debug_only=False):
        self.destination_list = destination_list
        self.sender_list = sender_list
        self.email_content = email_content
        self.debug_only = debug_only

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
                if not self.debug_only:
                    result = server.send_message(mime_message)
                print(
                    f"({index + 1}/{len(self.destination_list):<5})\t{mime_message['From']:<10} -> "
                    f"{mime_message['To']:<20}\t{result}")
