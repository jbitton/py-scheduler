from simulation.des import DES
from utils.util import populate_randvals, create_processes, print_processes

event_manager = DES()
process_list = []
populate_randvals('tests/inputs/rfile')
create_processes(event_manager, process_list, 'tests/inputs/input0')
print_processes(process_list, 100)
