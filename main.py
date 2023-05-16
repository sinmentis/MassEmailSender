#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import typing
import Common
import json

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
def parse_sender_data(filename: str, json_file: json = None) -> typing.List[Common.sender_email_account]:
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
            email_account = Common.sender_email_account(host, port, username, password, description, daily_send_limit)
            sender_list.append(email_account)
    except KeyError as e:
        raise Exception(f"Parsing error: Missing input from {filename} - {e}")

    return sender_list


@parser_decorator
def parse_email_to_send(filename: str, json_file: json = None) -> Common.email:
    """
    :param json_file: Placeholder for decorator
    :param filename: Email with subject and message
    :return: sender list of email_account
    """
    try:
        subject = json_file["subject"]
        message = json_file["message"]
        email = Common.email(subject, message)
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
            destination = Common.target(email_address, name, source, phone)
            for email in data.get("already_sent", []):
                email_hash_md5 = email['email_hash_md5']
                email_times = email['email_times']
                destination.add_sent_email(email_hash_md5, email_times)
            destination_list.append(destination)
    except KeyError as e:
        raise Exception(f"Parsing error: Missing input from {filename} - {e}")

    return destination_list


def main():
    sender_list = parse_sender_data("sender.json")
    email = parse_email_to_send("email_to_send.json")
    destination_list = parse_destination_list("destination_list.json")
    email_sender = Common.email_sender(destination_list, sender_list, email)
    email_sender.start_sending()


if __name__ == "__main__":
    main()
