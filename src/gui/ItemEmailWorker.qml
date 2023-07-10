import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1


GroupBox {
    title: "Step 5 - Send Email"

    Row {
        anchors{
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        height: parent.height
        spacing: 10

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Send"
            enabled: getSendingButtonState()
                onClicked: {
                    popup.open();
                    emailSenderTimer.start();
                }

                Timer {
                    id: emailSenderTimer
                    interval: 1
                    repeat: false
                    onTriggered: {
                        backend.startSending();
                    }
                }

            function getSendingButtonState() {
                var ifEmailIsNotSending = backend.emailWorkerState == 3 || backend.emailWorkerState == 4  // ALL_READY = 3
                var ifEmailLoaded = backend.emlLoadState
                var ifDestinationLoaded = (backend.emailDestinationList.length > 0)
                var ifSenderReady = senderList? senderList.senderLength > 0: false
                return ifEmailLoaded && ifDestinationLoaded && ifSenderReady && ifEmailIsNotSending
            }
        }

        Text {
            text: "Status: "
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        Text {
            id: workerstateText
            text: backend.emailWorkerStateStr
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: getColor()
            font.pointSize: 20
            function getColor() {
                if (backend.emailWorkerState == 0) {
                    return "red"
                } else if (backend.emailWorkerState == 1 || backend.emailWorkerState == 3 || backend.emailWorkerState == 4) {
                    return "green"
                } else if (backend.emailWorkerState == 2 || backend.emailWorkerState == 5) {
                    return "white"
                } else {
                    return "white"
                }
            }
        }
    }

    Popup {
        id: popup
        modal: true
        width: 200
        height: 200
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        BusyIndicator {
            running: image.status === Image.Loading
        }
    }

    Connections {
        target: backend
        function onEmailWorkerStateChanged() {
            if (backend.emailWorkerState == 1 && popup.opened) {
                popup.close()
            }
            workerstateText.text = backend.emailWorkerStateStr
        }

        function onEmailSendFinished(result) {
            workerstateText.text = result + "/" + result
        }
    }
}

