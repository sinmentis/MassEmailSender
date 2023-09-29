#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import sys
import datetime
import json
from enum import Enum
from multiprocessing import freeze_support

from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, Qt, QModelIndex, QByteArray, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import PyHunter
from MassEmailSender import MassEmailSender as MES

from EmailAll import emailall
import logging
from Frisbee import Frisbee
from PyHunter import pyhunter


class SystemState(Enum):
    ERROR = 0
    IDLE = 1
    DONE = 1
    PARSING_EMAIL = 2
    PARSING_EMAIL_FINISHED = 3
    READY = 4
    SENDING = 5


class SenderEmailQT(QAbstractListModel, MES.jsonParser.sender_email_account):
    HOST_ROLE = Qt.UserRole + 1
    PORT_ROLE = Qt.UserRole + 2
    USERNAME_ROLE = Qt.UserRole + 3
    PASSWORD_ROLE = Qt.UserRole + 4
    DESCRIPTION_ROLE = Qt.UserRole + 5
    DAILY_SEND_LIMIT_ROLE = Qt.UserRole + 6

    def __init__(self, filename, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.filename = filename
        data = MES.parse_sender_data(self.filename)
        self.sender_list = [self.sender_email_qt_to_dict(sender) for sender in data]

    def export_to_local(self):
        json_data = json.dumps({"email_sender_list": self.sender_list}, indent=4)
        with open(self.filename, "w") as file:
            file.writelines(json_data)

    # Python -> QML
    senderListChanged = Signal()

    # Functions - QML -> Python
    createSender = Signal()
    deleteSender = Signal(int)
    editSenderWithIndex = Signal(int, str)

    @Slot()
    def createSender(self):
        self.sender_list.append(
            self.sender_email_qt_to_dict(
                MES.jsonParser.sender_email_account(
                    host="example.host",
                    port=0,
                    username="example@example.com",
                    password="",
                    description="",
                    daily_send_limit=500
                )))
        self.senderListChanged.emit()
        self.export_to_local()

    @Slot(int)
    def deleteSender(self, index):
        del self.sender_list[index]
        self.senderListChanged.emit()
        self.export_to_local()

    @Slot(int, str)
    def editSenderWithIndex(self, index: int, json_string: str):
        self.sender_list[index] = self.sender_email_qt_to_dict(
            MES.jsonParser.sender_email_account(json_string=json_string))
        self.export_to_local()

    def sender_email_qt_to_dict(self, sender_email_qt: MES.jsonParser.sender_email_account) -> dict:
        data = {
            "host": sender_email_qt.host,
            "port": sender_email_qt.port,
            "username": sender_email_qt.username,
            "password": sender_email_qt.password,
            "description": sender_email_qt.description,
            "daily_send_limit": sender_email_qt.daily_send_limit,
            "daily_send_number": sender_email_qt.daily_send_number
        }
        return data

    def __getitem__(self, i):
        return self.sender_list[i]

    def __len__(self):
        return len(self.sender_list)

    @Slot(int, result="QVariant")
    def get_dict_from_index(self, index):
        if -len(self.sender_list) <= index <= len(self.sender_list):
            return self.sender_list[index]
        return {}

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.sender_list)):
            return None
        sender = self.sender_list[index.row()]
        if role == SenderEmailQT.HOST_ROLE:
            return sender["host"]
        elif role == SenderEmailQT.PORT_ROLE:
            return sender["port"]
        elif role == SenderEmailQT.USERNAME_ROLE:
            return sender["username"]
        elif role == SenderEmailQT.PASSWORD_ROLE:
            return sender["password"]
        elif role == SenderEmailQT.DESCRIPTION_ROLE:
            return sender["description"]
        elif role == SenderEmailQT.DAILY_SEND_LIMIT_ROLE:
            return sender["daily_send_limit"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.sender_list)

    def roleNames(self):
        return {
            SenderEmailQT.HOST_ROLE: QByteArray(b'host'),
            SenderEmailQT.PORT_ROLE: QByteArray(b'port'),
            SenderEmailQT.USERNAME_ROLE: QByteArray(b'username'),
            SenderEmailQT.PASSWORD_ROLE: QByteArray(b'password'),
            SenderEmailQT.DESCRIPTION_ROLE: QByteArray(b'description'),
            SenderEmailQT.DAILY_SEND_LIMIT_ROLE: QByteArray(b'daily_send_limit')
        }

    senderLength = Property(int, rowCount, notify=senderListChanged)


class MyApp(QObject):
    def __init__(self):
        super().__init__()
        self.app = QGuiApplication([])
        self.engine = QQmlApplicationEngine()
        self.backend = Backend(self.engine)
        self.setup()

        # Connect the aboutToQuit signal to the cleanup function
        self.app.aboutToQuit.connect(self.cleanup)

    def setup(self):
        context = self.engine.rootContext()
        context.setContextProperty("backend", self.backend)
        self.engine.load("./gui/main.qml")
        if not self.engine.rootObjects():
            sys.exit(-1)

    def run(self):
        sys.exit(self.app.exec())

    def cleanup(self):
        # Quit the search thread if it's running
        if self.backend.search_thread and self.backend.search_thread.isRunning():
            self.backend.search_thread.quit()
            self.backend.search_thread.wait()


class Backend(QObject):
    def __init__(self, engine):
        super().__init__()
        self.email_parser_emailAll = emailall.EmailAll(debug_only=False)
        self.email_parser_frisbee = Frisbee.Frisbee(log_level=logging.DEBUG, save=False)
        self.email_parser_pyhunter = PyHunter.PyHunter(pyhunter_API_getter())

        self.domain_name_to_search = "fromLocal"
        self.state = SystemState.IDLE

        self.sender_list = SenderEmailQT("./config_json/sender.json")
        self.engine = engine
        self.engine.rootContext().setContextProperty("senderList", self.sender_list)

        # For Sending engine
        self.total_sent = 0
        self.email_worker = MES.EmailWorker(debug_only=False)
        self.email_worker.add_sender_list(self.sender_list)
        self.email_worker.select_sender(0)

        # For Searching engine
        self.search_thread = QThread()
        self.target_search_times = 0
        self.search_worker = None

    def update_destination_list(self, new_parser_results):
        result_emails = [MES.jsonParser.target(email_address=email, name="", source="", phone="") for email in
                         new_parser_results]
        result_emails += self.email_worker.destination_list

        self.email_worker.set_destination_list(list(set(result_emails)))

    def set_system_state(self, new_state: SystemState):
        if self.state == SystemState.PARSING_EMAIL:
            if new_state.name != SystemState.PARSING_EMAIL_FINISHED.name:
                return
        self.state = new_state
        self.emailWorkerStateChanged.emit()

    # Python -> QML
    currentEmailSenderChanged = Signal()
    destinationEmailListChanged = Signal()
    emlLoadStateChanged = Signal()
    emailWorkerStateChanged = Signal()
    emailSendFinished = Signal(int, int)

    # Functions - QML -> Python
    startSearchingEmail = Signal(str, int)
    exportEmailListToLocal = Signal()
    loadEMLFromFile = Signal(str)
    loadDestinationFromFiles = Signal(list)
    removeEmailIndex = Signal(int)
    startSending = Signal()

    def getCurrentEmailSenderIndex(self):
        return self.sender_list[self.email_worker.current_sender]

    def getEmailDestinationList(self):
        return [sender.to_dict() for sender in self.email_worker.destination_list]

    def getEmlLoadStateReady(self):
        return self.email_worker.email_content is not None

    def getEmailWorkerState(self):
        return self.state.value

    def getEmailWorkerStateStr(self):
        return self.state.name

    # QML Model
    currentEmailSenderIndex = Property(int, getCurrentEmailSenderIndex, notify=currentEmailSenderChanged)
    emailDestinationList = Property(list, getEmailDestinationList, notify=destinationEmailListChanged)
    emlLoadState = Property("bool", getEmlLoadStateReady, notify=emlLoadStateChanged)
    emailWorkerState = Property(int, getEmailWorkerState, notify=emailWorkerStateChanged)
    emailWorkerStateStr = Property(str, getEmailWorkerStateStr, notify=emailWorkerStateChanged)

    @Slot(str, int)
    def startSearchingEmail(self, target_domain, search_times=1):
        self.domain_name_to_search = target_domain
        self.target_search_times = search_times
        self.set_system_state(SystemState.PARSING_EMAIL)

        # Check if a previous search thread is running
        if self.search_thread and self.search_thread.isRunning():
            # Emit a signal to stop the previous thread
            del self.search_worker
            self.search_thread.quit()
            self.search_thread.wait()

        # Create a worker thread for the task
        self.search_thread = QThread()
        self.search_worker = EmailSearchWorker(self.domain_name_to_search, self.email_parser_emailAll,
                                               self.email_parser_frisbee, self.email_parser_pyhunter)
        self.search_worker.moveToThread(self.search_thread)

        # Connect signals and slots
        self.search_worker.searchCompleted.connect(self.onSearchCompleted)
        self.search_thread.started.connect(self.search_worker.start)
        self.search_thread.finished.connect(self.search_thread.deleteLater)
        self.search_thread.start()

    @Slot(list)
    def onSearchCompleted(self, search_results):
        self.update_destination_list(search_results)
        self.destinationEmailListChanged.emit()

        if self.target_search_times > 1:
            self.startSearchingEmail(self.domain_name_to_search, self.target_search_times - 1)
        else:
            self.set_system_state(SystemState.PARSING_EMAIL_FINISHED)

    @Slot()
    def exportEmailListToLocal(self):
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")  # Format the timestamp as desired
        if not os.path.exists("./export_destination"):
            os.mkdir("./export_destination")
        self.email_worker.export_destination(f"./export_destination/{timestamp} - {self.domain_name_to_search}")

    @Slot(list)
    def loadDestinationFromFiles(self, file_path):
        destination_list = []
        for file in file_path:
            try:
                if file.endswith(".txt") or file.endswith(".TXT"):
                    destination_list += MES.parse_destination_list_from_txt(file)
                else:
                    destination_list += MES.parse_destination_list_from_json(file)
            except:
                pass
        self.domain_name_to_search = "fromLocal"
        self.email_worker.destination_already_sent_list = []
        self.set_system_state(SystemState.READY)  # FIXME: not really, depends on UI to block it :(
        self.email_worker.set_destination_list(destination_list)
        self.destinationEmailListChanged.emit()

    @Slot(str)
    def loadEMLFromFile(self, file_path):
        self.email_worker.destination_already_sent_list = []
        self.set_system_state(SystemState.READY)  # FIXME: not really, depends on UI to block it :(
        if self.email_worker.set_email_from_eml(file_path):
            self.emlLoadStateChanged.emit()

    @Slot(int)
    def removeEmailIndex(self, index):
        self.email_worker.remove_destination_list(index)
        self.destinationEmailListChanged.emit()

    def email_status_callback(self, destination_index: int, result: bool):
        self.total_sent = destination_index + 1

    @Slot()
    def startSending(self):
        self.set_system_state(SystemState.SENDING)
        if not self.email_worker.start_sending(callback=self.email_status_callback):  # (callback=self.email_status_callback):
            self.set_system_state(SystemState.ERROR)
        self.set_system_state(SystemState.DONE)
        self.emailSendFinished.emit(self.total_sent, len(self.email_worker.destination_list))

    @Slot(int)
    def handleSelectionChange(self, current_index):
        self.email_worker.select_sender(current_index)
        self.currentEmailSenderChanged.emit()


class EmailSearchWorker(QObject):
    searchCompleted = Signal(list)

    def __init__(self, domain_name, email_parser_emailAll, email_parser_frisbee, email_parser_pyhunter):
        super().__init__()
        self.domain_name = domain_name
        self.email_parser_emailAll = email_parser_emailAll
        self.email_parser_frisbee = email_parser_frisbee
        self.email_parser_pyhunter = email_parser_pyhunter

    @Slot()
    def start(self):
        email_parser_results = []

        # Start EmailAll engine
        email_parser_results_emailAll = []
        emailAll_results = self.email_parser_emailAll.run(self.domain_name)
        for source in emailAll_results.keys():
            if emailAll_results[source] is not None:
                email_parser_results_emailAll += emailAll_results[source]

        # Start Frisbee engine
        email_parser_results_frisbee = []
        jobs = [{'engine': "bing", 'modifier': None,
                 'domain': self.domain_name, 'limit': 500,
                 'greedy': False, 'fuzzy': False}]
        self.email_parser_frisbee.search(jobs)
        frisbee_results = self.email_parser_frisbee.get_results()
        for job in frisbee_results:
            if len(job['results']['emails']):
                email_parser_results_frisbee += job['results']['emails']

        # Start Pyhunter engine
        try:
            email_parser_results_pyhunter = self.email_parser_pyhunter.domain_search(self.domain_name, email_only=True)
        except:
            email_parser_results_pyhunter = []

        # Combine into one big list
        email_parser_results += email_parser_results_emailAll
        email_parser_results += email_parser_results_frisbee
        email_parser_results += email_parser_results_pyhunter

        # Remove invalid email, only ends with @domain_name
        email_parser_results = [email for email in set(email_parser_results) if email.endswith(f"@{self.domain_name}")]

        self.searchCompleted.emit(email_parser_results)


def pyhunter_API_getter():
    try:
        with open(os.path.join("config_json", "pyhunter_API.txt")) as file:
            data = file.read().strip()
    except:
        print("ERR: config_json/pyhunter_API.txt not exist, skip hunter.io engine")
        data = ""
    return data


def main():
    backend = MyApp()
    backend.run()


if __name__ == "__main__":
    freeze_support()
    main()
