@echo off
call python -m PyQt5.uic.pyuic -x main_window.ui -o MainWindowUi.py
call python -m PyQt5.uic.pyuic -x segmentation_settings_dialog.ui -o SegmentationSettingsUi.py
call python -m PyQt5.uic.pyuic -x edit_segmentation_settings_dialog.ui -o EditSegmentationSettingsUi.py
call python -m PyQt5.uic.pyuic -x template_dialog.ui -o TemplatePickingUi.py
echo Generation done!
