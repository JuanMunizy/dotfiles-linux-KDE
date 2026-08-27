import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.components as PlasmaComponents
import org.kde.plasma.plasma5support as Plasma5Support
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root

    readonly property string p_command: plasmoid.configuration.command || ""
    readonly property int p_updateInterval: plasmoid.configuration.updateInterval || 2
    readonly property bool p_showIcon: plasmoid.configuration.showIcon
    readonly property string p_iconName: plasmoid.configuration.iconName || "utilities-terminal-symbolic"

    property string stdoutOutput: ""

    implicitWidth: mainLayout.implicitWidth
    Layout.preferredWidth: implicitWidth
    onImplicitWidthChanged: plasmoid.preferredRepresentationWidth = implicitWidth

    Plasma5Support.DataSource {
        id: cmdSource
        engine: "executable"
        connectedSources: []
        onNewData: (sourceName, data) => {
            stdoutOutput = data.stdout ? data.stdout.trim() : "";
            disconnectSource(sourceName);
        }
    }

    Timer {
        interval: root.p_updateInterval * 1000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            if (root.p_command) {
                cmdSource.connectSource("bash -c '" + root.p_command + "'");
            }
        }
    }

    RowLayout {
        id: mainLayout
        anchors.fill: parent
        spacing: Kirigami.Units.smallSpacing

        Kirigami.Icon {
            id: iconItem
            source: root.p_iconName
            visible: root.p_showIcon
            Layout.preferredWidth: root.height * 0.8
            Layout.preferredHeight: root.height * 0.8
            Layout.alignment: Qt.AlignVCenter
        }

        PlasmaComponents.Label {
            id: textLabel
            text: root.stdoutOutput

            font.pixelSize: root.height * 0.45
            lineHeight: 0.85

            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

            wrapMode: Text.NoWrap

            Layout.preferredWidth: contentWidth
            Layout.alignment: Qt.AlignVCenter
            elide: Text.ElideNone
        }
    }
}
