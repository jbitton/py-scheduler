from schedulers.base import BaseScheduler
from schedulers.rr import RR


class PRIO(BaseScheduler):
    def __init__(self, time_quantum):
        super().__init__()
        self.time_quantum = time_quantum
        self.priority_levels = 4
        self.priority_queue = [RR(time_quantum), RR(time_quantum), RR(time_quantum), RR(time_quantum)]
        self.expired_queue = [RR(time_quantum), RR(time_quantum), RR(time_quantum), RR(time_quantum)]
        self.priority_arrays = [self.priority_queue, self.expired_queue]

    def add_process(self, new_process):
        queue = 0
        if new_process.dynamic_priority == -1:
            queue = 1
            new_process.dynamic_priority = new_process.static_priority - 1
        self.priority_arrays[queue][new_process.dynamic_priority].add_process(new_process)

    def find_process(self):
        for i in reversed(range(self.priority_levels)):
            returned_process = self.priority_arrays[0][i].get_next_process()
            if returned_process is not None:
                return returned_process
        return None

    def get_next_process(self):
        next_process = self.find_process()

        if next_process is not None:
            return next_process

        self.priority_arrays[0], self.priority_arrays[1] = self.priority_arrays[1], self.priority_arrays[0]

        return self.find_process()
