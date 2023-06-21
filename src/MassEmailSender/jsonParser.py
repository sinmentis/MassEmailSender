import json


class sender_email_account:
    def __init__(self, host: str = None, port: int = None, username: str = None, password: str = None,
                 description: str = None, daily_send_limit: int = None, json_string: str = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.description = description
        self.daily_send_limit = daily_send_limit
        if json_string:
            self.from_json(json_string)

    def from_json(self, json_string: str):
        data = json.loads(json_string)
        self.host = data.get('host')
        self.port = data.get('port')
        self.username = data.get('username')
        self.password = data.get('password')
        self.description = data.get('description')
        self.daily_send_limit = data.get('daily_send_limit')

    def __str__(self):
        return self.username


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

    def __str__(self):
        data = {
            "email_address": self.email_address,
            "name": self.name,
            "source": self.source,
            "phone": self.phone,
            "already_sent": self.already_sent
        }
        return json.dumps(data, indent=4)

    def to_dict(self):
        data = {
            "email_address": self.email_address,
            "name": self.name,
            "source": self.source,
            "phone": self.phone,
            "already_sent": self.already_sent
        }
        return data
