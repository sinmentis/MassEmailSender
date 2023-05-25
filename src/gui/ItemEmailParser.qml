import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1

GroupBox{
    title: "Step 2: Getting Email List"
    Row {
        anchors{
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        height: parent.height
        spacing: 40

        Text {
            text: "Domain to search: (i.e. gmail.com)"
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        TextField {
            text: ""
            width: 200
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Start Searching"
            onClicked: function() {}
        }

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Load Email from local"
            onClicked: function() {}
        }
    }
}
