# Author: Gabriel Dinse
# File: ProductInfo
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime

# Third party modules
import pydispatch

# Local application imports


class ProductInfo:
    def __init__(self, offset, has_cover):
        self.datetime_produced = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.offset = offset
        self.has_cover = has_cover

class WorkerQueue:
    def __init__(self, callback, max_workers=0):
        self.sentinel = object()
        self.callback = callback
        self.queue = Queue(maxsize=max_workers)

    def put(self, *args, **kwargs):
        self.queue.put((args, kwargs))

    def finish_works(self):
        self.queue.put(self.sentinel)

    def run(self):
        while True:
            try:
                item = self.queue.get()
                if item is self.sentinel:
                    return
                args, kwargs = item
                self.callback(*args, **kwargs)
            finally:
                # Importante para o caso de multithreading para quando der
                # join na fila
                self.queue.task_done()

def circular_kernel(size):
    """ Cria um uma janela circular para aplicacao de convolucao. """

    kernel = np.ones((size, size), dtype=np.uint8)
    center = floor(size / 2)
    for i in range(size):
        for j in range(size):
            if hypot(i - center, j - center) > center:
                kernel[i, j] = 0
    return kernel


class VideoInfoEvents(pydispatch.Dispatcher):
    _events_ =  ['new_product', 'new_frame']