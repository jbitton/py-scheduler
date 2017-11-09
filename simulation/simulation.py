from utils.util import randomize
from utils.structures import State, Transition, Event
from sys import maxsize


def simulation(event_manager, scheduler):
    current_running_process = None
    start = maxsize
    end = -maxsize - 1
    processes_in_io = 0
    total_io_time = 0

    while event_manager:
        event = event_manager.get_event()
        if event is None:
            break
        current_time = event.timestamp
        call_scheduler = False

        if event.transition == Transition.READY:
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
            scheduler.add_process(event.process)
            call_scheduler = True
        elif event.transition == Transition.RUN:
            current_running_process = event.process
            if event.process.current_cb > 0:
                actual_burst = min(event.process.current_cb, event.process.timeout)
                if event.process.cpu_time_left - actual_burst <= 0:
                    event.process.finishing_time = event.process.entry_time + event.process.cpu_time_left
                    new_event = Event(event.process.finishing_time, event.process, State.RUNNING, Transition.DONE)
                elif event.process.current_cb == actual_burst:
                    event.process.entry_time += actual_burst
                    new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.BLOCK)
                else:
                    event.process.entry_time += event.process.timeout
                    new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.READY)
            else:
                event.process.current_cb = randomize(event.process.cpu_burst)
                if event.process.current_cb > event.process.timeout:
                    if event.process.cpu_time_left - event.process.timeout <= 0:
                        event.process.finishing_time = event.process.entry_time + event.process.cpu_time_left
                        new_event = Event(event.process.finishing_time, event.process, State.RUNNING, Transition.DONE)
                    else:
                        event.process.entry_time += event.process.timeout
                        new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.READY)
                elif event.process.cpu_time_left - event.process.current_cb <= 0:
                    event.process.finishing_time = event.process.entry_time + event.process.cpu_time_left
                    new_event = Event(event.process.finishing_time, event.process, State.RUNNING, Transition.DONE)
                else:
                    event.process.entry_time += event.process.current_cb
                    new_event = Event(event.process.entry_time, event.process, State.RUNNING, Transition.BLOCK)
            event.process.dynamic_priority -= 1
            event_manager.put_event(new_event)
        elif event.transition == Transition.BLOCK:
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
            new_event = Event(event.process.entry_time, event.process, State.BLOCKED, Transition.READY)
            event_manager.put_event(new_event)
            call_scheduler = True
        elif event.transition == Transition.DONE:
            event.process.turnaround_time = event.process.finishing_time - event.process.arrival_time
            call_scheduler = True
            current_running_process = None

        if call_scheduler:
            if event_manager.get_next_event_time() == current_time:
                continue

            if current_running_process is None:
                current_running_process = scheduler.get_next_process()
                if current_running_process is None:
                    continue

                current_running_process.cpu_waiting_time += current_time - current_running_process.entry_time
                current_running_process.entry_time = current_time
                new_event = Event(current_time, current_running_process, State.READY, Transition.RUN)
                event_manager.put_event(new_event)
                current_running_process = None
    return total_io_time




