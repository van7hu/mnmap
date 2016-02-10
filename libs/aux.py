import os, time
from time import sleep
import state, scan
from datetime import datetime
import argparse

# this should not be too big, if not, nmap will GIVE UP, I haven't had code to handle this case
MAX_NET_ERROR = 10

def test_network(threads, ips, running_ips, next_ips, init_file):
    if (test_network_aux()==False):
        scan.scan.start_flag = False

        if test_network.counter == 0:
            print 'At ['+ str(datetime.now()) + '] script, you may have Internet problem!'
            test_network.counter = test_network.counter + 1
        elif test_network.counter < MAX_NET_ERROR:
            print 'At ['+ str(datetime.now()) + '] script, '+ str(test_network.counter) + '. Internet problem still persisted!'
            sleep(5)
            test_network.counter = test_network.counter + 1
        elif test_network.counter == MAX_NET_ERROR:
            print 'At ['+ str(datetime.now()) + '] script, '+ str(test_network.counter) + '. too much network errors, will save the state'
            state.save_state(threads, ips, running_ips, next_ips, init_file)
            test_network.counter = test_network.counter + 1
        else:
            print 'At ['+ str(datetime.now()) + '] script, '+ str(test_network.counter) + '. Internet problem still persisted, state has been saved!'
            sleep(0.25)
            test_network.counter = test_network.counter + 1
    
    else:
        if(test_network.counter >= MAX_NET_ERROR):
            print 'At ['+ str(datetime.now()) + '] script, Internet problem has been solved'
            next_ips, init_file = state.load_state(threads, ips, running_ips) # here should contain problems X must be solved by Y
            test_network.counter = 0
            return next_ips # will be greater than 0, Y
        elif test_network.counter > 0:
            print 'At ['+ str(datetime.now()) + '] script, ' + str(test_network.counter) + ' .Internet problem has been solved'
            test_network.counter = 0

        scan.scan.start_flag = True

def test_network_aux():
    hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname + ' >/dev/null 2>/dev/null')

    #and then check the response...
    if response == 0:
        return True
    else:
        return False

def read_init_file(init_file):
    lines = open(init_file, 'r').readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    try:
        lines.remove('')
    except:
        pass
    
    return lines

def print_status(next_ips, ips):
    sleep(1)
    if print_status.output_counter % 600 == 0:
        print 'At ['+ str(datetime.now()) + '] script, STATUS: we up to ' + str(next_ips) + ' of ' + str(len(ips))

    print_status.output_counter = print_status.output_counter + 1

def init_argparser(parser):
    parser.add_argument('-a, --action', required=True, help='take 1 of 2 values (start or resume), start or resume scanning', dest='action', type=str)

    parser.add_argument('-t, --threads', required=False, help='number of maximum thread for doing scanning (each thread will handle one line in the input file)', dest='threads', type=int)

    parser.add_argument('-i, --input', required=False, help='input file for scanning, line seperated ip, ip range or hostname', dest='input', type=str)

    
