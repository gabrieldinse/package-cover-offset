# Author: Gabriel Dinse
# File: ProductInfo
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
import datetime

# Third party modules

# Local application imports


class ProductInfo:
    def __init__(self, offset, has_cover):
        self.datetime_produced = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.offset = offset
        self.has_cover = has_cover

class ProducInfoQueue:
    def __init__(self, application, max_workers=0):
        self.sentinel = object()
        self.applcation = application
        self.queue = Queue(maxsize=max_workers)

    def add_product(self, product_info):
        self.queue.put(product_info)

    def finish_works(self):
        self.queue.put(self.sentinel)

    def run(self):
        while True:
            try:
                # Bloqueia ate ter item na fila para dar 'get()'
                item = self.queue.get()
                if item is self.sentinel:
                    return
                self.application.new_product_callback(item)
            finally:
                # Importante para o caso de multithreading para quando der
                # join na fila
                self.queue.task_done()