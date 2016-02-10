import os, time
from time import sleep
import state, scan
from datetime import datetime

# this should not be too big, if not, nmap will GIVE UP, I haven't had code to handle this case
MAX_NET_ERROR = 10

def test_network(threads, ips, running_ips, next_ips):
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
            state.save_state(threads, ips, running_ips, next_ips)
            test_network.counter = test_network.counter + 1
        else:
            print 'At ['+ str(datetime.now()) + '] script, '+ str(test_network.counter) + '. Internet problem still persisted, state has been saved!'
            sleep(0.25)
            test_network.counter = test_network.counter + 1
    
    else:
        if(test_network.counter >= MAX_NET_ERROR):
            print 'At ['+ str(datetime.now()) + '] script, Internet problem has been solved'
            next_ips = state.load_state(threads, ips, running_ips)
            test_network.counter = 0
            return next_ips # will be greater than 0
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
