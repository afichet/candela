import QtQuick 2.0
import QtQuick.Controls 2.15
import AppConfig 1.0

Page {
    id: root
    property AppConfig config: app_config
    anchors.fill: parent
    header: ToolBar {
        Label {
            text: qsTr("Hue bridges")
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

    ListView {
        id: bridgeListView
        anchors.fill: parent
        topMargin: 20
        leftMargin: 48
        bottomMargin: 20
        rightMargin: 48
        spacing: 20
        model: bridge_model
        delegate: ItemDelegate {
            text: ip
            width: bridgeListView.width - bridgeListView.leftMargin - bridgeListView.rightMargin
            height: bridgeIcon.height
            leftPadding: bridgeIcon.width + 32
            onClicked: {
                if (!configured) {
                    root.StackView.view.push("PairBridge.qml", {config: config, ip: ip});
                } else {
                    root.StackView.view.push("LightControl.qml", {
                                                 config: config,
                                                 ip: ip,
                                                 user: user});
                }
            }

            Image {
                id: bridgeIcon
                source: "icons/network-wired-solid.svg"
                width:50
                height:50
                fillMode: Image.PreserveAspectFit
            }
        }
    }
}