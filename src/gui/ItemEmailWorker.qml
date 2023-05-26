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
            onClicked: function() {
                backend.startSending()
            }

            function getSendingButtonState() {
                var ifEmailLoaded = backend.emlLoadState
                var ifDestinationLoaded = (backend.emailDestinationList.length > 0)
                var ifSenderReady = backend.senderList.length > 0

                return ifEmailLoaded && ifDestinationLoaded && ifSenderReady
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
            text: getWorkerStateText()
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"

            function getWorkerStateText() {
                var already_sent_out = backend.emailWorkerState.length
                var total = backend.emailDestinationList.length

                return already_sent_out + " / " + total
            }
        }
    }
}
