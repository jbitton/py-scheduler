import argparse

from simulation.des import DES
from simulation.simulation import simulation

from schedulers.fcfs import FCFS
from schedulers.lcfs import LCFS
from schedulers.prio import PRIO
from schedulers.rr import RR
from schedulers.sjf import SJF

from utils.util import populate_randvals, create_processes, print_processes

parser = argparse.ArgumentParser(description='CPU Scheduler Algorithms')
parser.add_argument('-s', nargs=1, default='F', help='used to specify the scheduler to use')
parser.add_argument('input', type=str, help='the inputfile to be used with the scheduler')
parser.add_argument('rand', type=str, help='the randfile to be used with the simulation')

args = vars(parser.parse_args())

event_manager = DES()
process_list = []
populate_randvals(args['rand'])
create_processes(event_manager, process_list, args['input'])

if 'L' in args['s']:
    scheduler = LCFS()
    print('LCFS')
elif 'S' in args['s']:
    scheduler = SJF()
    print('SJF')
elif 'R' in args['s'][0]:
    time_quantum = int(args['s'][0][1:])
    scheduler = RR(time_quantum)
    print('RR', time_quantum)
elif 'P' in args['s'][0]:
    time_quantum = int(args['s'][0][1:])
    scheduler = PRIO(time_quantum)
    print('PRIO', time_quantum)
else:
    scheduler = FCFS()
    print('FCFS')

total_io = simulation(event_manager, scheduler)
print_processes(process_list, total_io)
