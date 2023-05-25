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
            anchors.fill: parent
            id: tableView
            rowSpacing: 3

            model: TableModel {
                TableModelColumn { display: "emailAddress" }
                TableModelColumn { display: "checked" }
                TableModelColumn { display: "remove" }

                // Model data row representing here one type of fruit that can be ordered
                rows: [
                    // Each property is one cell/column.
                    {
                        checked: false,
                        emailAddress: "test@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    },
                    {
                        checked: true,
                        emailAddress: "test2@gmail.com",
                        remove: "remove"
                    }
                ]
            }

            delegate: DelegateChooser {

                DelegateChoice {
                    column: 0
                    delegate: TextField {
                        implicitWidth: 650
                        implicitHeight: 30
                        font.capitalization: Font.AllUppercase
                        text: model.display
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
                        checked: model.display
                    }
                }

                DelegateChoice {
                    column: 2
                    delegate: Button {
                        width: 10
                        text: model.display
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
