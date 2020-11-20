@echo off
call python -m PyQt5.uic.pyuic -x %~dp0\main_window.ui -o %~dp0\MainWindowUi.py
call python -m PyQt5.uic.pyuic -x %~dp0\segmentation_settings_dialog.ui -o %~dp0\SegmentationSettingsUi.py
call python -m PyQt5.uic.pyuic -x %~dp0\template_dialog.ui -o %~dp0\TemplatePickingUi.py
echo Generation done!
