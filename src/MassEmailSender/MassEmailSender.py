import os.path
import typing
from . import jsonParser
import json
from smtplib import SMTP
import email
from email.message import EmailMessage
from email.header import Header

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


class EmailWorker:
    def __init__(self, destination_list: typing.List[jsonParser.target] | None = None,
                 sender_list: typing.List[jsonParser.sender_email_account] | None = None,
                 email_content: jsonParser.email | None = None,
                 debug_only=False):
        self.destination_list = destination_list if destination_list else []
        self.sender_list = sender_list
        self.email_content = email_content
        self.debug_only = debug_only

        self.current_sender = None if sender_list is None else sender_list[0]
        self.destination_already_sent_list = []

    def set_destination_list(self, destination_list):
        self.destination_list = destination_list

    def remove_destination_list(self, index):
        if 0 <= index < len(self.destination_list):
            del self.destination_list[index]

    def add_sender_list(self, sender_list):
        self.sender_list = sender_list

    def set_email_from_eml(self, eml_file):
        if os.path.exists(eml_file):
            with open(eml_file, 'rb') as file:
                self.email_content = email.message_from_binary_file(file)
                return True
        print(f"{eml_file} doesn't exist")
        return False

    def select_sender(self, index):
        if len(self.sender_list) == 0:
            return

        if self.sender_list and index < len(self.sender_list):
            self.current_sender = self.sender_list[index]
            print(f"User {self.current_sender['username']} been selected")
        else:
            raise Exception(f"Err: currently only {len(self.sender_list)} sender exist, asking for {index}")

    def _construct_mime_message(self):
        email_message = EmailMessage()
        subject_encoded = self.email_content['Subject']
        subject_decoded = email.header.decode_header(subject_encoded)[0][0]
        subject_decoded = subject_decoded.decode("utf-8")

        # Remove the second part
        if len(self.email_content.get_payload()) > 1:
            del self.email_content.get_payload()[1:]

        email_message.set_content(self.email_content)
        email_message['Subject'] = subject_decoded
        email_message['From'] = Header(self.current_sender.username, 'utf-8')
        return email_message

    def start_sending(self):
        mime_message = self._construct_mime_message()

        with SMTP(self.current_sender.host, self.current_sender.port) as server:
            # server.set_debuglevel(2)

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

            self.destination_already_sent_list = []
            for index, destination in enumerate(self.destination_list):
                if mime_message.get("To"):
                    mime_message.replace_header('To', Header(destination.email_address, 'utf-8'))
                else:
                    mime_message["To"] = Header(destination.email_address, 'utf-8')

                result = ""
                if not self.debug_only:
                    result = server.send_message(mime_message)
                    self.destination_already_sent_list.append(index)
                print(
                    f"({index + 1}/{len(self.destination_list):<5})\t{mime_message['From']:<10} -> "
                    f"{mime_message['To']:<20}\t{result}")
