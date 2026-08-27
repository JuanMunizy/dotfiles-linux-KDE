import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QtControls
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    id: root

    property alias cfg_command: commandField.text
    property alias cfg_updateInterval: intervalSpin.value
    property alias cfg_showIcon: showIconCheck.checked
    property alias cfg_iconName: iconNameField.text

    property string cfg_commandDefault: "echo -e \"Seconds:\\n$(date +%S)\""
    property int cfg_updateIntervalDefault: 1
    property bool cfg_showIconDefault: true
    property string cfg_iconNameDefault: "utilities-terminal-symbolic"

    property bool cfg_expanding: false
    property int cfg_length: 0
    property var cfg_expandingDefault: false
    property var cfg_lengthDefault: 0

    Kirigami.FormLayout {
        QtControls.TextField {
            id: commandField
            Kirigami.FormData.label: i18n("Command:")
            Layout.fillWidth: true
            placeholderText: i18n("Example: echo -e \"Seconds:\\n$(date +%S)\"")
        }

        QtControls.SpinBox {
            id: intervalSpin
            Kirigami.FormData.label: i18n("Update interval (sec):")
            from: 1
            to: 3600
            stepSize: 1
            editable: true
        }

        QtControls.CheckBox {
            id: showIconCheck
            Kirigami.FormData.label: i18n("Icon:")
            text: i18n("Show system icon")
        }

        QtControls.TextField {
            id: iconNameField
            Kirigami.FormData.label: i18n("Icon name:")
            Layout.fillWidth: true
            placeholderText: i18n("Example: utilities-terminal-symbolic")
            enabled: showIconCheck.checked
        }
    }
}
