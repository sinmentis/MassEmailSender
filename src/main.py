#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, Qt, QModelIndex, QByteArray
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from MassEmailSender import MassEmailSender as MES

"""
TODO:
1. Email Parser side
    1.1 TBD
2. Email worker side 
    2.0 Send email within daily limit, switch sender if possible
    2.1 Modify the destination list datastructure to only have email address, or wrapper around it
    2.2 Sender worker - eml format thing, not working in foxmail but works in gmail
    2.3 After Email Parser
        1. Adding export email list to local feature, with domain name as filename
"""


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
        print()

    def export_to_local(self):
        json_data = json.dumps({"email_sender_list":self.sender_list}, indent=4)
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
            self.sender_email_qt_to_dict(MES.jsonParser.sender_email_account(username="example@example.com")))
        self.senderListChanged.emit()
        self.export_to_local()

    @Slot(int)
    def deleteSender(self, index):
        del self.sender_list[index]
        self.senderListChanged.emit()
        self.export_to_local()

    @Slot(int, str)
    def editSenderWithIndex(self, index: int, json_string: str):
        self.sender_list[index] = self.sender_email_qt_to_dict(MES.jsonParser.sender_email_account(json_string=json_string))
        self.export_to_local()

    def sender_email_qt_to_dict(self, sender_email_qt: MES.jsonParser.sender_email_account) -> dict:
        data = {
            "host": sender_email_qt.host,
            "port": sender_email_qt.port,
            "username": sender_email_qt.username,
            "password": sender_email_qt.password,
            "description": sender_email_qt.description,
            "daily_send_limit": sender_email_qt.daily_send_limit
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

    def setup(self):
        context = self.engine.rootContext()
        context.setContextProperty("backend", self.backend)
        self.engine.load("./gui/main.qml")
        if not self.engine.rootObjects():
            sys.exit(-1)

    def run(self):
        sys.exit(self.app.exec())


class Backend(QObject):
    def __init__(self, engine):
        super().__init__()
        self.email_worker = MES.EmailWorker(debug_only=True)
        self.sender_list = SenderEmailQT("./config_json/sender.json")
        self.engine = engine
        self.engine.rootContext().setContextProperty("senderList", self.sender_list)

        self.email_worker.add_sender_list(self.sender_list)
        self.email_worker.select_sender(0)

    # Python -> QML
    currentEmailSenderChanged = Signal()
    destinationEmailListChanged = Signal()
    emlLoadStateChanged = Signal()
    emailWorkerStateChanged = Signal()
    emailSendingResult = Signal(int, bool)

    # Functions - QML -> Python
    startSearchingEmail = Signal(str)
    exportEmailListToLocal = Signal()
    loadEMLFromFile = Signal(str)
    loadDestinationFromFile = Signal(str)
    removeEmailIndex = Signal(int)
    startSending = Signal()

    def getCurrentEmailSenderIndex(self):
        return self.sender_list[self.email_worker.current_sender]

    def getEmailDestinationList(self):
        return [sender.to_dict() for sender in self.email_worker.destination_list]

    def getEmlLoadStateReady(self):
        return self.email_worker.email_content is not None

    def getEmailWorkerState(self):
        return len(self.email_worker.destination_already_sent_list)

    # QML Model
    currentEmailSenderIndex = Property(int, getCurrentEmailSenderIndex, notify=currentEmailSenderChanged)
    emailDestinationList = Property(list, getEmailDestinationList, notify=destinationEmailListChanged)
    emlLoadState = Property("bool", getEmlLoadStateReady, notify=emlLoadStateChanged)
    emailWorkerState = Property(int, getEmailWorkerState, notify=emailWorkerStateChanged)

    @Slot(str)
    def startSearchingEmail(self, target_domin):
        # TODO: pass it to seracher target_domin
        print(f"TOOD: Start seraching {target_domin}")

    @Slot()
    def exportEmailListToLocal(self):
        self.email_worker.export_destination()

    @Slot(str)
    def loadDestinationFromFile(self, file_path):
        destination_list = MES.parse_destination_list(file_path)
        self.email_worker.destination_already_sent_list = []
        self.emailWorkerStateChanged.emit()
        self.email_worker.set_destination_list(destination_list)
        self.destinationEmailListChanged.emit()

    @Slot(str)
    def loadEMLFromFile(self, file_path):
        self.email_worker.destination_already_sent_list = []
        self.emailWorkerStateChanged.emit()
        if self.email_worker.set_email_from_eml(file_path):
            self.emlLoadStateChanged.emit()

    @Slot(int)
    def removeEmailIndex(self, index):
        self.email_worker.remove_destination_list(index)
        self.destinationEmailListChanged.emit()

    def email_status_callback(self, destination_index: int, result: bool):
        self.emailWorkerStateChanged.emit()
        self.emailSendingResult.emit(destination_index, result)
        print(f"Sending email to {destination_index}: {self.email_worker.destination_list[destination_index].email_address}. Result: {result}")

    @Slot()
    def startSending(self):
        self.email_worker.start_sending(callback=self.email_status_callback)

    @Slot(int)
    def handleSelectionChange(self, current_index):
        self.email_worker.select_sender(current_index)
        self.currentEmailSenderChanged.emit()


def main():
    backend = MyApp()
    backend.run()


if __name__ == "__main__":
    main()
