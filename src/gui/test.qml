import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    width: 400
    height: 300
    visible: true
    title: "Table View Example"

    TableView {
        id: tableView
        anchors.fill: parent
        model: myModel

        RowLayout {
            anchors.fill: parent

            ColumnLayout {
                Layout.fillWidth: true

                CheckBox {
                    text: "Checked"
                    checked: myModel.data(index, Qt.CheckStateRole) === Qt.Checked
                    onCheckedChanged: {
                        if (checked)
                            myModel.setData(index, Qt.Checked, Qt.CheckStateRole)
                        else
                            myModel.setData(index, Qt.Unchecked, Qt.CheckStateRole)
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true

                Text {
                    text: myModel.data(index, Qt.DisplayRole)
                }
            }

            ColumnLayout {
                Layout.fillWidth: true

                Button {
                    text: myModel.data(index, Qt.DisplayRole)
                    onClicked: {
                        // Handle remove button click here
                    }
                }
            }
        }
    }
}
