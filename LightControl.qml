import QtQuick 2.4
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import Qt.labs.platform 1.0

import LightModel 1.0

Page {
    id: root

    property var config
    property string ip
    property string user
    property LightModel light: LightModel{ip: root.ip; user: root.user}

    anchors.fill: parent
    header: ToolBar{
        ToolButton {
            text: qsTr("Back")
            anchors.left: parent.left
            onClicked: root.StackView.view.pop()
            icon.source: "icons/arrow-left-solid.svg"
        }

        Label {
            text: qsTr("All lights")
            padding: 10
            font.pixelSize: 20
            anchors.centerIn: parent
            MouseArea {
                anchors.fill: parent
                property point lastMousePos: Qt.point(0, 0)
                onPressed: { lastMousePos = Qt.point(mouseX, mouseY); }
                onMouseXChanged: window.x += (mouseX - lastMousePos.x)
                onMouseYChanged: window.y += (mouseY - lastMousePos.y)
            }
        }

        ToolButton {
            anchors.right: exitButton.left
            onClicked: showMinimized()
            icon.source: "icons/minus-solid.svg"
        }

        ToolButton {
            id: exitButton
            anchors.right: parent.right
            onClicked: Qt.callLater(Qt.quit)
            width: height
            icon.source: "icons/times-solid.svg"
        }
    }

    ListView {
        id: lightListView
        anchors.fill: parent
        topMargin: 20
        leftMargin: 48
        bottomMargin: 20
        rightMargin: 48
        spacing: 20
        model: light
        delegate: RowLayout {
            width: lightListView.width - lightListView.leftMargin - lightListView.rightMargin
            spacing: 50
            Button {
                id: button
                onPressed: colorDialog.open()
                Layout.alignment: Qt.AlignLeft
                background: Rectangle {
                    implicitHeight: 40
                    implicitWidth: 40
                    color: colour
                    border.color: "#222222"
                }
            }
            Label {
                id: label
                text: name
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                Layout.alignment: Qt.AlignLeft
            }

            Switch {
                checked: on
                Layout.alignment: Qt.AlignRight
                onToggled: root.light.change_state(id, checked)
            }

            Dial {
                implicitWidth: 40
                implicitHeight: 40
                value: brightness
                onMoved: root.light.set_brightness(id, value)
            }

            ColorDialog {
                id: colorDialog
                onColorChanged: root.light.change_color(id, currentColor)
                onAccepted: root.light.change_color(id, color)
                Timer {
                    interval: 200
                    running: parent.visible
                    repeat: true
                    onTriggered: root.light.change_color(id, parent.currentColor);
                }

            }
        }
    }
}