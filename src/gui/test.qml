import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: textFieldWithLabel
    property string labelText: ""
    property string placeholderText: ""

    Row {
        spacing: 10

        Label {
            text: labelText
            width: 100
            verticalAlignment: Text.AlignVCenter
        }

        TextField {
            id: inputField
            width: 200
            placeholderText: placeholderText
        }
    }

    // Proxy property to access the text input value
    property alias text: inputField.text
}
