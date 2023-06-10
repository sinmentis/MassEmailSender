import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1


GroupBox {
    title: "Step 4 - Load Email "
    Row {
        anchors{
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        height: parent.height
        spacing: 10

        Text {
            text: "Email to send"
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        Button {
            height: parent.height / 2
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Load Email from local"
            onClicked: fileDialog.open()
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
            text: backend.emlLoadState ? "Ready" : "Empty"
            width: 200
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: backend.emlLoadState ? "green" : "red"
            font.bold: backend.emlLoadState
        }
    }

    FileDialog {
        id: fileDialog
        title: "Load EML File"
        nameFilters: ["EML files (*.eml)"]
        onAccepted: {
            if (selectedFile !== "") {
                var file = selectedFile.toString().replace("file://", "")
                backend.loadEMLFromFile(file)
            }
        }
    }
}
