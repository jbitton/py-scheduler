from simulation.des import DES
from schedulers.fcfs import FCFS
from utils.util import populate_randvals, create_processes, print_processes
from simulation.simulation import simulation

event_manager = DES()
scheduler = FCFS()
process_list = []
populate_randvals('tests/inputs/rfile')

create_processes(event_manager, process_list, 'tests/inputs/input6')
total_io = simulation(event_manager, scheduler)
print_processes(process_list, total_io)
