from utils.util import randomize
from utils.structures import State, Transition, Event
from sys import maxsize

current_running_process = None
start = maxsize
end = -maxsize - 1
processes_in_io = 0
total_io_time = 0


def ready(event):
    global current_running_process, start, end, processes_in_io, total_io_time
    if event.current_state == State.RUNNING:
        event.process.cpu_time_left -= event.process.timeout
        event.process.current_cb -= event.process.timeout
        current_running_process = None
    elif event.current_state == State.BLOCKED:
        event.process.io_time += event.process.current_ib
        processes_in_io -= 1
        if processes_in_io == 0:
            total_io_time += end - start
            start = maxsize
            end = -maxsize - 1


def running(event):
    global current_running_process
    current_running_process = event.process
    if event.process.current_cb <= 0:
        event.process.current_cb = randomize(event.process.cpu_burst)
    actual_burst = min(event.process.current_cb, event.process.timeout)
    if event.process.cpu_time_left - actual_burst <= 0:
        event.process.finishing_time = event.process.entry_time + event.process.cpu_time_left
        new_event = Event(event.process.finishing_time, event.process, State.RUNNING, Transition.DONE)
    elif event.process.current_cb == actual_burst:
        event.process.entry_time += actual_burst
        new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.BLOCK)
    else:
        event.process.entry_time += actual_burst
        new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.READY)
    return new_event


def block(event, current_time):
    global current_running_process, start, end, processes_in_io
    current_running_process = None
    event.process.cpu_time_left -= event.process.current_cb
    event.process.current_cb = 0
    event.process.current_ib = randomize(event.process.io_burst)
    event.process.entry_time += event.process.current_ib
    event.process.dynamic_priority = event.process.static_priority - 1
    processes_in_io += 1
    if start > current_time:
        start = current_time
    if end < event.process.entry_time:
        end = event.process.entry_time
    return Event(event.process.entry_time, event.process, State.BLOCKED, Transition.READY)


def simulation(event_manager, scheduler):
    global current_running_process, start, end, processes_in_io, total_io_time
    while event_manager.event_list:
        event = event_manager.get_event()
        current_time = event.timestamp
        call_scheduler = False

        if event.transition == Transition.READY:
            ready(event)
            scheduler.add_process(event.process)
            call_scheduler = True
        elif event.transition == Transition.RUN:
            new_event = running(event)
            event.process.dynamic_priority -= 1
            event_manager.put_event(new_event)
        elif event.transition == Transition.BLOCK:
            new_event = block(event, current_time)
            event_manager.put_event(new_event)
            call_scheduler = True
        elif event.transition == Transition.DONE:
            event.process.turnaround_time = event.process.finishing_time - event.process.arrival_time
            call_scheduler = True
            current_running_process = None

        if not call_scheduler or event_manager.get_next_event_time() == current_time:
            continue

        if current_running_process is not None:
            continue

        current_running_process = scheduler.get_next_process()
        if current_running_process is None:
            continue

        current_running_process.cpu_waiting_time += current_time - current_running_process.entry_time
        current_running_process.entry_time = current_time
        new_event = Event(current_time, current_running_process, State.READY, Transition.RUN)
        event_manager.put_event(new_event)
        current_running_process = None
    return total_io_time




