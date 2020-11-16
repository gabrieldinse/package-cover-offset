# Author: Gabriel Dinse
# File: Events
# Date: 11/15/2020
# Made with PyCharm

# Standard Library

# Third party modules
import pydispatch

# Local application imports


class VideoInfoEvents(pydispatch.Dispatcher):
    _events_ =  ['new_product', 'new_frame']

class MainWindowEvents(pydispatch.Dispatcher):
    _events_ = ['vision_system_start', 'vision_system_stop',
                'new_product_type', 'product_type_edited',
                'close',
                'turn_on_camera', 'turn_off_camera']