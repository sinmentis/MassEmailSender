#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from MassEmailSender import MassEmailSender as MES

class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._sender_list = []

    senderListChanged = Signal()

    def getSenderList(self):
        return self._sender_list

    def setSenderList(self, sender_list):
        if self._sender_list != sender_list:
            self._sender_list = sender_list
            self.senderListChanged.emit()
    senderList = Property(list, getSenderList, setSenderList, notify=senderListChanged)

    @Slot(str)
    def update_sender_list(self, sender_list):
        self.setSenderList(sender_list)


def main():
    email = MES.parse_email_to_send("./config_json/email_to_send.json")
    destination_list = MES.parse_destination_list("./config_json/destination_list.json")


def prepare_QT():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    context = engine.rootContext()
    context.setContextProperty("backend", backend)

    sender_list = MES.parse_sender_data("./config_json/sender.json")
    backend.update_sender_list([str(sender) for sender in sender_list])

    engine.load("./gui/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    prepare_QT()
