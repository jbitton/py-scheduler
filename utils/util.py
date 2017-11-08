from os.path import exists
from utils.structures import Process, Event, State, Transition

ofs = 0
max_length = 0
randvals = []


def populate_randvals(filename):
    if not exists(filename):
        print(f"Not a valid randfile <({filename})>")
        exit(1)

    tokens = open(filename, 'r').read().split()

    if len(tokens) <= 0:
        randvals.append(0)
        return

    global max_length
    max_length = int(tokens[0])

    for i in range(1, max_length+1):
        if not tokens[i].isdigit():
            print("format error in random file")
            exit(1)
        randvals.append(int(tokens[i]))


def randomize(burst):
    global ofs, max_length
    rand = 1 + (randvals[ofs] % burst)
    if ofs >= max_length - 1:
        ofs = 0
    else:
        ofs += 1
    return rand


def create_processes(event_manager, process_list, filename):
    if not exists(filename):
        print(f"Not a valid inputfile <({filename})>")
        exit(1)

    tokens = open(filename, 'r').read().split()

    if len(tokens) <= 0:
        print("Error input file format line 0")
        exit(1)

    count, process_number = 0, 0
    attr = [0] * 4

    for token in tokens:
        if not token.isdigit():
            print(f"Error input file format line {process_number}")
            exit(1)

        attr[count] = int(token)
        count += 1

        if count == 4:
            new_process = Process(attr[0], attr[1], attr[2], attr[3], randomize(4), process_number)
            process_list.append(new_process)
            event = Event(new_process.entry_time, new_process, State.STATE_CREATED, Transition.TRANS_TO_READY)
            event_manager.put_event(event)
            count = 0
            process_number += 1


def print_processes(process_list, total_io):
    total_cpu_time = 0
    num_processes = 0
    total_turnaround_time = 0
    total_cpu_waiting_time = 0
    finish_time = 0

    for p in process_list:
        print(f"{p.pid}: {p.arrival_time} {p.total_cpu_time} {p.cpu_burst} {p.io_burst} ", end=" ")
        print(f"{p.static_priority} | {p.finishing_time} {p.turnaround_time} {p.io_time} {p.cpu_waiting_time}")

        total_cpu_time += p.total_cpu_time
        total_turnaround_time += p.turnaround_time
        total_cpu_waiting_time += p.cpu_waiting_time
        num_processes += 1

        if p.finishing_time > finish_time:
            finish_time = p.finishing_time

    # print_totals(finish_time, total_cpu_time, total_io, num_processes, total_turnaround_time, total_cpu_waiting_time)


def print_totals(finish_time, total_cpu, total_io, num_processes, total_turnaround, total_cpu_waiting):
    cpu_utilization = (total_cpu / float(finish_time)) * 100.0
    io_utilization = (total_io / float(finish_time)) * 100.0
    avg_turnaround = (total_turnaround / float(num_processes))
    avg_cpu_waiting = (total_cpu_waiting / float(num_processes))
    throughput = (num_processes / float(finish_time)) * 100.0

    print(f"SUM: {finish_time} {cpu_utilization} {io_utilization} {avg_turnaround} {avg_cpu_waiting} {throughput}")
