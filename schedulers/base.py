from collections import deque
from abc import abstractclassmethod


class BaseScheduler(object):
    def __init__(self):
        self.run_queue = deque([])

    @abstractclassmethod
    def add_process(self, process):
        raise NotImplementedError

    @abstractclassmethod
    def get_next_process(self):
        raise NotImplementedError
