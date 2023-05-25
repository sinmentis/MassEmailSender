import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1


GroupBox {
    title: "Step 5 - Send Email "

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
            onClicked: function() {}
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
            text: "Empty"
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }
    }
}
