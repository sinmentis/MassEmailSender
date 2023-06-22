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
                id: comboBox
                width: parent.width
                anchors.centerIn: parent
                model: senderList
                displayText: senderList.get_dict_from_index(currentIndex)? senderList.get_dict_from_index(currentIndex)["username"] : ""
                currentIndex: 0
                enabled: backend.emailWorkerState !== 2
                delegate: Item {
                    width: comboBox.width
                    height: 30

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "transparent"
                        border.width: 1
                        border.color: "gray"

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                comboBox.currentIndex = index
                                comboBox.popup.close()
                            }
                        }
                        Text {
                            anchors.centerIn: parent
                            text: model["username"]
                        }
                    }
                }

                onCurrentIndexChanged: function() {
                    if (currentIndex >= 0) {
                        backend.handleSelectionChange(currentIndex)
                        comboBox.displayText = senderList.get_dict_from_index(comboBox.currentIndex)? senderList.get_dict_from_index(comboBox.currentIndex)["username"] : ""
                    }
                }
            }
        }

        Button {
            height: parent.height
            Layout.fillWidth: true
            anchors.verticalCenter: parent.verticalCenter
            text: "Sender management"
            enabled: backend.emailWorkerState !== 2
            onClicked: function() {
                popupLoader.active = false
                popupLoader.active = true
                popup.open()
            }
        }
    }

    Popup {
        id: popup
        contentItem: Loader {
            id: popupLoader
            anchors.fill: parent
            source: "WindowsSenderManagement.qml"
        }
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        focus: true
        visible: false
        onClosed: function () {
            comboBox.model.modelReset()
            comboBox.displayText = senderList.get_dict_from_index(comboBox.currentIndex)? senderList.get_dict_from_index(comboBox.currentIndex)["username"] : ""
            backend.handleSelectionChange(comboBox.currentIndex)
        }
    }
}
