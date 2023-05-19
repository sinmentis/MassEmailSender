#!/usr/bin/python3
# -*- coding: utf-8 -*-

from MassEmailSender import MassEmailSender as MES

def main():
    sender_list = MES.parse_sender_data("./config_json/sender.json")
    email = MES.parse_email_to_send("./config_json/email_to_send.json")
    destination_list = MES.parse_destination_list("./config_json/destination_list.json")
    email_sender = MES.email_worker(destination_list, sender_list, email, debug_only=True)
    email_sender.start_sending()


if __name__ == "__main__":
    main()
