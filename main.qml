import QtQuick 2.13
import QtQuick.Window 2.13
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.0



ApplicationWindow {
    id: window
    title: qsTr("Candela")
    width: 640
    height: 480
    opacity: 0.9
    visible: true
    flags: Qt.FramelessWindowHint |Qt.WindowMinimizeButtonHint | Qt.Window
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem:BridgeView{}
    }
}
