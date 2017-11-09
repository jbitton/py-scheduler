from enum import Enum


class State(Enum):
    CREATED = 1
    READY = 2
    RUNNING = 3
    BLOCKED = 4


class Transition(Enum):
    READY = 1
    RUN = 2
    BLOCK = 3
    DONE = 4


class Process(object):
    def __init__(self, arrival_time, total_cpu_time, cpu_burst, io_burst, prio, pid, timeout=10000):
        self.arrival_time = arrival_time
        self.entry_time = arrival_time
        self.total_cpu_time = total_cpu_time
        self.cpu_time_left = total_cpu_time
        self.cpu_burst = cpu_burst
        self.io_burst = io_burst
        self.static_priority = prio
        self.dynamic_priority = prio - 1
        self.pid = pid
        self.timeout = timeout
        self.finishing_time = 0
        self.turnaround_time = 0
        self.io_time = 0
        self.cpu_waiting_time = 0
        self.current_cb = 0
        self.current_ib = 0


class Event(object):
    def __init__(self, timestamp, process, curr_state, new_state):
        self.timestamp = timestamp
        self.process = process
        self.current_state = curr_state
        self.transition = new_state
