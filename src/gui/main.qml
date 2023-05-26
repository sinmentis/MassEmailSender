import QtQuick 2.14
import Qt.labs.qmlmodels 1.0
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window 2.1

Window {
    id: mainWindow

    width: 800
    height: 600
    maximumHeight: height
    maximumWidth: width
    minimumHeight: height
    minimumWidth: width

    color: "#3c3d22"
    visible: true

    title: "Massive Email Sender"


    property bool debug: false
    property int loaderRowHeight: 40

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        width: parent.width

        Loader {
            id: itemSenderRow
            Layout.minimumWidth: 800
            height: mainWindow.loaderRowHeight
            source: "ItemSenderRow.qml"
            Rectangle {
                anchors.fill: parent
                border.width: 1
                border.color: "white"
                color: "Transparent"
                visible: debug
            }
        }

//        Loader {
//            Layout.minimumWidth: 800
//            height: mainWindow.loaderRowHeight
//            source: "test.qml"
//            Rectangle {
//                anchors.fill: parent
//                border.width: 1
//                border.color: "white"
//                color: "Transparent"
//                visible: debug
//            }
//        }

        Loader {
            id: itemEmailParser
            Layout.minimumWidth: 800
            height: mainWindow.loaderRowHeight
            source: "ItemEmailParser.qml"
            Rectangle {
                anchors.fill: parent
                border.width: 1
                border.color: "white"
                color: "Transparent"
                visible: debug
            }
        }

        Loader {
            id: itemEmailStatus
            Layout.minimumWidth: 800
            height: 300
            source: "ItemEmailStatus.qml"
            Rectangle {
                anchors.fill: parent
                border.width: 1
                border.color: "white"
                color: "Transparent"
                visible: debug
            }
        }

        Loader {
            id: itemEmailLoader
            Layout.minimumWidth: 800
            height: mainWindow.loaderRowHeight
            source: "ItemEmailLoader.qml"
            Rectangle {
                anchors.fill: parent
                border.width: 1
                border.color: "white"
                color: "Transparent"
                visible: debug
            }
        }

        Loader {
            id: itemEmailSender
            Layout.minimumWidth: 800
            Layout.minimumHeight: mainWindow.loaderRowHeight * 2
            source: "ItemEmailWorker.qml"
            Rectangle {
                anchors.fill: parent
                border.width: 1
                border.color: "white"
                color: "Transparent"
                visible: debug
            }
        }
    }

    Rectangle {
        anchors.fill: columnLayout
        border.width: 1
        border.color: "white"
        color: "Transparent"
        visible: debug
    }
}

