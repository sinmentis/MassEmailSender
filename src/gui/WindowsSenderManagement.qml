import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

ApplicationWindow {
    width: 300
    height: 400
    visible: true
    title: "Sender Management"
    maximumHeight: height
    maximumWidth: width
    minimumHeight: height
    minimumWidth: width

    property bool isValidEmail: false

    function validateEmail(email) {
        // Regular expression for email validation
        var emailRegExp = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
        return emailRegExp.test(email);
    }

    function restoretext() {
        hostInput.text = ""  // Clear user input text
        hostInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["host"]? senderList.get_dict_from_index(comboBox.currentIndex)["host"]: ""

        portInput.text = ""  // Clear user input text
        portInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["port"]? senderList.get_dict_from_index(comboBox.currentIndex)["port"]: ""

        usernameInput.text = ""  // Clear user input text
        usernameInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["username"]? senderList.get_dict_from_index(comboBox.currentIndex)["username"]: ""

        passwordInput.text = ""  // Clear user input text
        passwordInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["password"]? senderList.get_dict_from_index(comboBox.currentIndex)["password"]: ""

        descriptionInput.text = ""  // Clear user input text
        descriptionInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["description"]? senderList.get_dict_from_index(comboBox.currentIndex)["description"]: ""

        dailyLimitInput.text = ""  // Clear user input text
        dailyLimitInput.text = senderList.get_dict_from_index(comboBox.currentIndex)["daily_send_limit"]? senderList.get_dict_from_index(comboBox.currentIndex)["daily_send_limit"]: ""
    }

    Item {
        id: senderSelect
        height: 30
        width: 300

        Row {
            Label {
                text: "Sender:"
                width: 50
            }
            ComboBox {
                id: comboBox

                // Function to update the dropdown list
                function updateDropdownList() {
                    comboBox.model.modelReset()
                }

                width: 200
                model: senderList
                currentIndex: -1
                displayText: usernameInput.text
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
                            text: model["username"]? model["username"]: ""
                        }
                    }
                }
                onCurrentIndexChanged: {
                    comboBox.currentIndex = currentIndex
                    restoretext()
                }
            }

            Button {
                id: addNewSender
                width: 20
                text: "+"
                onClicked: {
                    senderList.createSender()
                    comboBox.updateDropdownList()
                    comboBox.currentIndex = -1
                }
            }

            Button {
                id: deleteSender
                width: 20
                text: "-"
                onClicked: {
                    senderList.deleteSender(comboBox.currentIndex)
                    comboBox.updateDropdownList()
                    comboBox.currentIndex = -1
                    restoretext()
                }
                enabled: senderList.senderLength > 0
            }
        }
    }


    GroupBox {
        title: "Sender Management"
        anchors.top: senderSelect.bottom
        width: 300
        visible: senderList.senderLength > 0
        Column {
            spacing: 10

            Row {
                Label {
                    text: "Host"
                    width: 100
                }
                TextField {
                    id: hostInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["host"]? senderList.get_dict_from_index(comboBox.currentIndex)["host"]: ""
                }
            }

            Row {
                Label {
                    text: "Port"
                    width: 100
                }
                TextField {
                    id: portInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["port"]? senderList.get_dict_from_index(comboBox.currentIndex)["port"] : ""
                    inputMethodHints: Qt.ImhDigitsOnly
                }
            }

            Row {
                Label {
                    text: "Username (Email)"
                    width: 100
                }
                TextField {
                    id: usernameInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["username"]? senderList.get_dict_from_index(comboBox.currentIndex)["username"] : ""
                    onTextChanged: {
                        if (validateEmail(text)) {
                            isValidEmail = true
                        } else {
                            isValidEmail = false
                        }
                    }
                }
            }

            Row {
                Label {
                    text: "Password"
                    width: 100
                }
                TextField {
                    id: passwordInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["password"]? senderList.get_dict_from_index(comboBox.currentIndex)["password"]: ""
                    echoMode: TextInput.Password
                }
            }

            Row {
                Label {
                    text: "Description"
                    width: 100
                }
                TextField {
                    id: descriptionInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["description"]? senderList.get_dict_from_index(comboBox.currentIndex)["description"]:""
                }
            }

            Row {
                Label {
                    text: "Daily Sent Limit"
                    width: 100
                }
                TextField {
                    id: dailyLimitInput
                    width: 200
                    text: senderList.get_dict_from_index(comboBox.currentIndex)["daily_send_limit"]? senderList.get_dict_from_index(comboBox.currentIndex)["daily_send_limit"]: ""
                }
            }

            Button {
                text: "Confirm"
                onClicked: {
                    var data = {
                        "host": hostInput.text,
                        "port": portInput.text,
                        "username": usernameInput.text,
                        "password": passwordInput.text,
                        "description": descriptionInput.text,
                        "daily_send_limit": parseInt(dailyLimitInput.text)
                    }
                    senderList.editSenderWithIndex(comboBox.currentIndex, JSON.stringify(data))
                }
                enabled: hostInput.text.length > 0 && portInput.text.length > 0 && usernameInput.text.length > 0 &&
                         passwordInput.text.length > 0 && descriptionInput.text.length > 0 && dailyLimitInput.text.length > 0
            }
        }
    }
}
