#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from MassEmailSender import MassEmailSender as MES

class Backend(QObject):
    def __init__(self, email_worker: MES.EmailWorker):
        super().__init__()

        self.email_worker = email_worker
        sender_list = MES.parse_sender_data("./config_json/sender.json")
        self.email_worker.add_sender_list(sender_list)
        self.senderListChanged.emit()

    # Python -> QML
    senderListChanged = Signal()
    destinationEmailListChanged = Signal()
    emlLoadStateChanged = Signal()
    emailWorkerStateChanged = Signal()

    # State Changed - QML -> Python
    selectionIndexChanged = Signal(int)

    # Functions - QML -> Python
    startSearchingEmail = Signal(str)
    exportEmailListToLocal = Signal()
    loadEMLFromFile = Signal(str)
    loadEmailListFromFile = Signal(str)
    removeEmailIndex = Signal(int)
    startSending = Signal()

    def getSenderList(self):
        return [str(sender) for sender in self.email_worker.sender_list]

    def getEmailDestinationList(self):
        # TODO: Might need to change data structure of email_worker.destination_list into simple list, so that it can
        #  be removed
        return [sender.email_address for sender in self.email_worker.destination_list]

    def getEmlLoadStateReady(self):
        return self.email_worker.email_content is not None

    def getEmailWorkerState(self):
        return self.email_worker.destination_already_sent_list

    def setEmailDestinationList(self):
        pass

    # QML Model
    senderList = Property(list, getSenderList, notify=senderListChanged)
    emailDestinationList = Property("QVariantList", getEmailDestinationList, notify=destinationEmailListChanged)
    emlLoadState = Property("bool", getEmlLoadStateReady, notify=emlLoadStateChanged)
    emailWorkerState = Property(list, getEmailWorkerState, notify=emailWorkerStateChanged)

    @Slot(str)
    def startSearchingEmail(self, target_domin):
        # TODO: pass it to seracher target_domin
        print(f"TOOD: Start seraching {target_domin}")


    @Slot()
    def exportEmailListToLocal(self):
        # TODO: exportEmailListToLocal
        print("TOOD: exportEmailListToLocal")


    @Slot(str)
    def loadEmailListFromFile(self, file_path):
        destination_list = MES.parse_destination_list(file_path)
        self.email_worker.set_destination_list(destination_list)
        self.destinationEmailListChanged.emit()

    @Slot(str)
    def loadEMLFromFile(self, file_path):
        if self.email_worker.set_email_from_eml(file_path):
            self.emlLoadStateChanged.emit()

    @Slot(str)
    def removeEmailIndex(self, index):
        print(f"TOOD: removeEmailIndex: {index}")
        self.email_worker.remove_destination_list(index)
        self.destinationEmailListChanged.emit()

    @Slot()
    def startSending(self):
        self.email_worker.start_sending()

    @Slot(int)
    def handleSelectionChange(self, currnet_index):
        self.email_worker.select_sender(currnet_index)


def main():
    email_worker = MES.EmailWorker()

    # Prepare QT
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend(email_worker)
    context = engine.rootContext()
    context.setContextProperty("backend", backend)
    engine.load("./gui/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
