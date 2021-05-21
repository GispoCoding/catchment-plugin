import pytest
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialogButtonBox
from qgis.core import QgsProject

from EdPlanning.plugin import Plugin
from EdPlanning.qgis_plugin_tools.tools.settings import get_setting

from .conftest import MOCK_URL, QGIS_APP


def test_plugin(new_plugin, mock_fetch, qtbot):
    def click_button():
        dialog = new_plugin.dlg
        buttonbox = dialog.buttonbox_main
        for button in buttonbox.buttons():
            if buttonbox.buttonRole(button) == QDialogButtonBox.AcceptRole:
                qtbot.mouseClick(button, Qt.LeftButton)

    mock_fetch(MOCK_URL + "/isochrone")
    # set timer to click after plugin is run
    QTimer.singleShot(100, click_button)
    # start plugin event loop
    new_plugin.run()
    action = QGIS_APP.taskManager().activeTasks()[0]
    blocker = qtbot.waitSignal(action.taskCompleted, timeout=10000)
    blocker.wait()
    # check result layer
    for layer in QgsProject.instance().mapLayers().values():
        assert layer.featureCount() == 1
