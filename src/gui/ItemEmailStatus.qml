import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1

import Qt.labs.qmlmodels 1.0


Item {
    width: 800
    height: 200
    Flickable {
        id: flickable
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        boundsMovement: Flickable.StopAtBounds
        boundsBehavior: Flickable.StopAtBounds

        TableView {
            id: tableView
            anchors.fill: parent
            rowSpacing: 3

            model: TableModel {
                id: tableModel

                TableModelColumn { display: "emailAddress" }
                TableModelColumn { display: "checked" }
                TableModelColumn { display: "remove" }

                rows: []
            }

            delegate: DelegateChooser {
                DelegateChoice {
                    column: 0
                    delegate: TextField {
                        implicitWidth: 650
                        implicitHeight: 30
                        font.capitalization: Font.AllUppercase
                        text: tableModel.rows[index]? tableModel.rows[index].emailAddress: ""
                        readOnly: true
                        verticalAlignment: TextInput.AlignVCenter // Align vertically centered
                        horizontalAlignment: TextInput.AlignHCenter // Align horizontally centered
                    }
                }

                DelegateChoice {
                    column: 1
                    delegate: CheckBox {
                        enabled: false
                        width: 50
                        checked: false
                    }
                }

                DelegateChoice {
                    column: 2
                    delegate: Button {
                        width: 10
                        text: "remove"
                        onClicked: function() {
                            // FIXME: Why 10? Why the index of first value is 10
                            backend.removeEmailIndex(index-10)
                        }
                    }
                }
            }

            Connections {
                target: backend
                function onDestinationEmailListChanged() {
                    tableModel.clear()
                    for (var i = 0; i < backend.emailDestinationList.length; i++) {

                        var rowData = {
                            emailAddress: backend.emailDestinationList[i],
                            checked: "",
                            remove: ""
                        };
                        tableModel.appendRow(rowData)
                    }
                }
            }
        }

        ScrollBar.vertical: ScrollBar {
            id: scrollBar
            parent: flickable.parent
            anchors.top: flickable.top
            anchors.left: flickable.right
            anchors.bottom: flickable.bottom
            policy: ScrollBar.AsNeeded
            size: flickable.contentHeight/ flickable.height - 1
            stepSize: 1
            snapMode: ScrollBar.SnapOnRelease
            contentItem: Rectangle {
                implicitWidth: 6
                color: "red"
            }
        }
    }
}
