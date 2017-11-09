from schedulers.base import BaseScheduler


class RR(BaseScheduler):
    def __init__(self, time_quantum):
        super().__init__()
        self.time_quantum = time_quantum

    def add_process(self, new_process):
        if new_process.timeout != self.time_quantum:
            new_process.timeout = self.time_quantum

        if not self.run_queue:
            self.run_queue.appendleft(new_process)
            return

        for i, process in enumerate(self.run_queue):
            if process.entry_time > new_process.entry_time:
                self.run_queue.insert(i, new_process)
                return

        self.run_queue.append(new_process)

    def get_next_process(self):
        if not self.run_queue:
            return None
        return self.run_queue.popleft()
