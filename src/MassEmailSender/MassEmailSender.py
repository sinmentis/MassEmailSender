import os.path
import os
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


def convert_to_windows_path(path):
    windows_path = path.replace('/', '\\')
    return windows_path


def parser_decorator(func):
    """
    :param func: has to take arguments (filename: str, json_file: json = None)
    :return: filled json_file with result of json.load()
    """

    def wrapper(*args, **kwargs):
        filepath = os.path.normpath(args[0])

        if os.name == 'nt' and filepath[0] in ("/", "\\"):
            filepath = os.path.abspath(filepath[1:])

        if os.path.exists(filepath):
            with open(filepath) as file:
                kwargs["json_file"] = json.load(file)
            return func(*args, **kwargs)
        else:
            raise Exception(f"{filepath} doesn't exist, exit...")

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


def parse_destination_list_from_txt(filename: str) -> list[jsonParser.target]:
    """
    :param filename: target txt file
    :return: sender list of email_account
    """
    filepath = os.path.normpath(filename)

    if os.name == 'nt' and filepath[0] in ("/", "\\"):
        filepath = os.path.abspath(filepath[1:])

    if os.path.exists(filepath):
        with open(filepath) as file:
            data = file.readlines()
    else:
        return []

    try:
        destination_list = [jsonParser.target(line.strip(), "", "", "") for line in data]
    except Exception as e:
        raise Exception(f"Parsing error: Missing input from {filepath} - {e}")
    return destination_list


@parser_decorator
def parse_destination_list_from_json(filename: str, json_file: json = None) -> list[jsonParser.target]:
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
                 email_content: EmailMessage | None = None,
                 debug_only=False):
        self.num_email_sent = 0
        self.destination_list = destination_list if destination_list else []
        self.sender_list = sender_list
        self.email_content = email_content
        self.debug_only = debug_only

        self.current_sender = None if sender_list is None else sender_list[0]

    def export_destination(self, filename):
        num_destinations = len(self.destination_list)
        max_per_file = 500
        num_files = (num_destinations + max_per_file - 1) // max_per_file

        for i in range(num_files):
            start_index = i * max_per_file
            end_index = min((i + 1) * max_per_file, num_destinations)
            destinations_subset = self.destination_list[start_index:end_index]

            data = {"email_list": [destination.to_dict() for destination in destinations_subset]}
            filename_with_index = f"{filename} - {i + 1}_{num_files}.json"
            with open(filename_with_index, "w") as file:
                json.dump(data, file, indent=4)

    def set_destination_list(self, destination_list):
        self.destination_list = destination_list

    def remove_destination_list(self, index):
        if 0 <= index < len(self.destination_list):
            del self.destination_list[index]

    def add_sender_list(self, sender_list):
        self.sender_list = sender_list

    def set_email_from_eml(self, eml_file):
        filepath = os.path.normpath(eml_file)
        if os.name == 'nt' and filepath[0] in ("/", "\\"):
            filepath = os.path.abspath(filepath[1:])

        with open(filepath) as file:
            json_file = file.read()
        self.email_content = email.message_from_string(json_file)
        return True

    def select_sender(self, index):
        if len(self.sender_list) == 0:
            return

        if self.sender_list and index < len(self.sender_list):
            self.current_sender = self.sender_list[index]
            print(f"User {self.current_sender['username']} been selected")
        else:
            raise Exception(f"Err: currently only {len(self.sender_list)} sender exist, asking for {index}")

    def _switch_next_available_sender(self):
        new_sender_index = self.sender_list.sender_list.index(self.current_sender) + 1
        if new_sender_index >= len(self.sender_list):
            print("No more available sender, exit")
            return False
        else:
            print("Next select: ", new_sender_index)
            self.select_sender(new_sender_index)
        return True

    def _check_sender_daily_limit(self):
        return self.current_sender["daily_send_limit"] - self.current_sender["daily_send_number"]

    def _start_sending(self, server, email_list, callback):
        for index, destination in enumerate(email_list):
            if 'From' in self.email_content.keys():
                self.email_content.replace_header('From', Header(self.current_sender["username"], 'utf-8'))
            else:
                self.email_content['From'] = Header(self.current_sender["username"], 'utf-8')
            if 'To' in self.email_content.keys():
                self.email_content.replace_header('To', Header(destination.email_address, 'utf-8'))
            else:
                self.email_content['To'] = Header(destination.email_address, 'utf-8')

            if self.debug_only:
                print(f"DEBUG_ONLY: Email Sent from {self.current_sender['username']} to {destination['email_address']}")
            else:
                try:
                    server.send_message(self.email_content)
                    self.current_sender["daily_send_number"] += 1
                    print(
                        f"({index + 1}/{len(self.destination_list):<5})\t{str(self.email_content['From']):<10} -> "
                        f"{str(self.email_content['To']):<20}")
                    self.num_email_sent += 1
                    callback(self.num_email_sent)
                except:
                    break

    def start_sending(self, callback=None):
        email_left = self.destination_list[:]
        self.num_email_sent = 0

        while len(email_left) != 0:
            num_email_available = self._check_sender_daily_limit()
            if num_email_available > 0:
                try:
                    with SMTP(self.current_sender["host"], self.current_sender["port"], timeout=5) as server:
                        # server.set_debuglevel(2)
                        # Put the SMTP connection in TLS (Transport Layer Security) mode.
                        # All SMTP commands that follow will be encrypted
                        server.ehlo()  # Identify yourself to an ESMTP server using EHLO
                        if server.has_extn('STARTTLS'):
                            # print("STARTTLS extension is supported.")
                            server.starttls()
                        else:
                            print("STARTTLS extension is not supported.")
                        server.ehlo()  # re-identify ourselves as an encrypted connection

                        login_status = server.login(self.current_sender["username"], self.current_sender["password"])
                        # print(f"login_status: {login_status}" )
                        self._start_sending(server, email_left[:num_email_available], callback)
                        email_left = email_left[num_email_available:]
                except Exception as e:
                    print(f"error: {e}")
                    if not self._switch_next_available_sender():
                        return
            else:
                if not self._switch_next_available_sender():
                    return False
        return True