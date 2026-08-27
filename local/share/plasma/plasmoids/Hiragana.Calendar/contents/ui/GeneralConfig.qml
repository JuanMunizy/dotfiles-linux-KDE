/*
 *  SPDX-FileCopyrightText: zayronxio
 *  SPDX-License-Identifier: GPL-3.0-or-later
 */
import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.kquickcontrols as KQControls

Item {
    id: configRoot

    property alias cfg_widgetColor: generalColor.color

    Kirigami.FormLayout {
        width: configRoot.width

        KQControls.ColorButton {
            id: generalColor
            Kirigami.FormData.label: i18n(' Color:')
            showAlphaChannel: true
        }
    }

}
