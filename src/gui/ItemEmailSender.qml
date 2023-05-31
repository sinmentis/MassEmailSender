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
                            color: "white"
                            text: model["username"]
                        }
                    }
                }
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
    }
}
