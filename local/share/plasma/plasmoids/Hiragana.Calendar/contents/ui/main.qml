import QtQuick
import Qt5Compat.GraphicalEffects
import org.kde.plasma.plasmoid

PlasmoidItem {
    id: root

    Plasmoid.backgroundHints: "NoBackground"

    property string hiraganaDay
    property color textColor1: Plasmoid.configuration.widgetColor

    property int intDay: Qt.formatDateTime(new Date(), "d")
    property string mountText: (new Date()).toLocaleString(Qt.locale(), "MMMM");
    property int year: Qt.formatDateTime(new Date(), "yyyy")

    property var days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    property var daysOfWeekHiragana: ["げつようび", "かようび", "すいようび", "もくようび", "きんようび", "どようび", "にちようび"]

    FontLoader {
        id: shiba
        source: "../fonts/Seibi Shiba Medium.otf"
    }

    FontLoader {
        id: antonio
        source: "../fonts/Antonio-Bold.ttf"
    }

    function assignStringHiragana() {
        var day = Qt.formatDateTime(new Date(), "dddd")
        for (var u = 0; u < days.length; u++){
            if (day === days[u]) {
                console.log(days[u])
                hiraganaDay = daysOfWeekHiragana[u]
            }
        }
    }
    Item {
        id:  wrapper
        width: hiraganaTextDay.implicitWidth
        height: hiraganaTextDay.implicitHeight
        Rectangle {
            id: mask
            anchors.fill: parent
            visible:  false
            gradient: Gradient {
                GradientStop { position: 0.0; color: "black" }
                GradientStop { position: 1.3; color: "transparent" }
            }
        }
        Text {
            id: hiraganaTextDay
            width: root.width < root.height*5 ? root.height*5 : root.width
            text: hiraganaDay
            color: textColor1
            font.bold: true
            font.pointSize: root.width < root.height*5 ? root.width/6 : root.height/6
            font.family: shiba.name
            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: mask
            }
        }
    }

    Text {
       text: intDay + " " + mountText
       anchors.bottom: wrapper.bottom
       anchors.right: wrapper.right
       font.pointSize: wrapper.height/4
       font.family: antonio.name
       color: textColor1
    }
    Text {
        text: year
        anchors.top: wrapper.bottom
        anchors.topMargin: - wrapper.height/8
        anchors.right: wrapper.right
        font.pointSize: wrapper.height/4
        font.family: antonio.name
        color: textColor1
    }
    Timer {
        interval: 6000
        running: true
        repeat: true
        onTriggered: {
            assignStringHiragana()
            intDay = Qt.formatDateTime(new Date(), "d")
            mountText =  (new Date()).toLocaleString(Qt.locale(), "MMMM");
            year = Qt.formatDateTime(new Date(), "yyyy")
        }
    }
    Component.onCompleted: {
        assignStringHiragana()
    }
}
