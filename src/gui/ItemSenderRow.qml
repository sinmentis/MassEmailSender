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

        Item {
            height: parent.height
            width: 400
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
                // TODO: Pop sender management window, can add more if needed, and save to local
                console.log("backend.senderList: ", backend.senderList)
            }
        }
    }
}
