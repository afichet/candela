import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

import AppConfig 1.0
import BridgeAccess 1.0

Page {
    id: root

    property AppConfig config
    property string ip
    property BridgeAccess bridge_access: BridgeAccess{ip: ip}

    anchors.fill: parent
    header: ToolBar{
        ToolButton {
            text: qsTr("Back")
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            onClicked: root.StackView.view.pop()
        }

        Label {
            text: qsTr("Pairing a new bridge")
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
            icon.source: "icons/times-solid.svg"
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        Label {
            text: qsTr("Push the button on the bridge to connect")
        }

        BusyIndicator {
            id: busyIndicator
            Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
            transformOrigin: Item.Center
        }
    }

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            bridge_access.ip = ip
            bridge_access.init_connection()
        }
    }

    // Signal argument names are not propagated from Python to QML, so we need to re-emit the signal
    signal connectionEstablished(string user)
    Component.onCompleted: bridge_access.connection_established.connect(root.connectionEstablished)

    Connections {
        target: root
        function onConnectionEstablished(user) {
            print(user)
            config.add_bridge(ip, user)
            root.StackView.view.pop()
        }
    }
}
