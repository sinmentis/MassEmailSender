import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1

GroupBox{
    title: "Step 2: Getting Email List"
    width: 800


    function checkSearchButtonState() {
        var emailPattern = /[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
        var isEmailValid = emailPattern.test(targetDomin.text)
        if (isEmailValid) {
            searchButton.enabled = true && backend.emailWorkerState !== 2
        } else {
            searchButton.enabled = false
        }
    }

    Row {
        anchors{
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        height: parent.height
        spacing: 40

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Load Local"
            enabled: backend.emailWorkerState !== 2
            onClicked: function() {
                fileDialog.open()
            }
        }

        Text {
            text: "Domain to search:"
            width: 70
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        TextField {
            id: targetDomin
            text: ""
            width: 100
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            onTextChanged: checkSearchButtonState()
        }

        Text {
            text: "times: "
            width: 15
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }

        TextField {
            id: searchTimes
            text: "1"
            width: 30
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Button {
            id: searchButton
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Start Searching"
            onClicked: function() {
                backend.startSearchingEmail(targetDomin.text, parseInt(searchTimes.text))
                checkSearchButtonState()
            }
            enabled: false
        }

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Export to local"
            onClicked: backend.exportEmailListToLocal()
        }
    }

    FileDialog {
        id: fileDialog
        title: "Load Email Address File"
        nameFilters: ["json or text files (*.json *.txt)", "All (*.*)"]
        fileMode: FileDialog.OpenFiles
        options: FileDialog.ReadOnly
        onAccepted: {
            var fileList = []
            for (var i = 0; i < selectedFiles.length; i++) {
                var file = selectedFiles[i].toString().replace("file://", "")
                fileList.push(file)
            }
            backend.loadDestinationFromFiles(fileList)
        }
    }
}
