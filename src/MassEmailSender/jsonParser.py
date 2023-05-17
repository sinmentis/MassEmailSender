import typing


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