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