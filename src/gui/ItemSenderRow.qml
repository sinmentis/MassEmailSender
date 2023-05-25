import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1

GroupBox{
    title: "Step 1: select valid sender"
    Row {
        height: parent.height
        spacing: 20

        Text {
            text: "Current Sender"
            width: 400
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        Item {
            height: parent.height
            width: 200
            anchors.verticalCenter: parent.verticalCenter

            ComboBox {
                width: parent.width
                anchors.centerIn: parent
                model: backend.senderList
                onCurrentIndexChanged: {
                    backend.handleSelectionChange(currentIndex)
                }
            }
        }

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Sender management"
            onClicked: function() {
                console.log("backend.senderList: ", backend.senderList)
            }
        }
    }
}
