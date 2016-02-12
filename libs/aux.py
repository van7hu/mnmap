import os, time
from time import sleep
import state, scan
from datetime import datetime
import argparse
import subprocess
import re

# this should not be too big, if not, nmap will GIVE UP, I haven't had code to handle this case
MAX_NET_ERROR = 10

def mnmap_msg(msg):
    base = 'At ['+ str(datetime.now()) + '] script, '
    print base + str(msg)

def test_network(threads, ips, running_ips, next_ips, init_file):
    if (test_network_aux()==False):
        scan.scan.start_flag = False

        if test_network.counter == 0:
            mnmap_msg('you may have Internet problem!')
            test_network.counter = test_network.counter + 1
        elif test_network.counter < MAX_NET_ERROR:
            mnmap_msg(str(test_network.counter) + '. Internet problem still persisted.')
            sleep(5)
            test_network.counter = test_network.counter + 1
        elif test_network.counter == MAX_NET_ERROR:
            mnmap_msg(str(test_network.counter) + '. too much network errors, will save the state')
            state.save_state(threads, ips, running_ips, next_ips, init_file)
            test_network.counter = test_network.counter + 1
        else:
            mnmap_msg(str(test_network.counter) + '. Internet problem still persisted, state has been saved.')
            sleep(1)
            test_network.counter = test_network.counter + 1
    
    else:
        if(test_network.counter >= MAX_NET_ERROR):
            mnmap_msg(str(test_network.counter) + '. Internet problem has been solved')
            next_ips = state.load_state(threads, ips, running_ips, init_file)
            test_network.counter = 0
            # return next_ips # This line will not needed, when checking with network, we have done nothing with next_ips
        elif test_network.counter > 0:
            mnmap_msg(str(test_network.counter) + '. Internet problem has been solved')
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

def read_init_file(init_file, write_processed):
    lines = open(init_file, 'r').readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    try:
        lines.remove('')
    except:
        pass
    
    out = processing_init_ips(lines)
    if write_processed == True:
        processed_file = init_file + '.processed'
        with open(processed_file, 'w') as f:
            for line in out:
                f.write(line+'\n')

        mnmap_msg("'" + processed_file + "' was written for reference")

    return out

def processing_init_ips(ips):
    r = []
    for i in ips:
        r.append(i.split('/'))

    for k in reversed(r):
        for i in reversed(r):
            if ((len(k) == 2 and len(i) == 2)) and k[0] == i[0]:
                if int(k[1]) < int(i[1]):
                    r.remove(i)
    out = []
    for i in r:
        if len(i) == 1:
            out.append(i[0])
        if len(i) == 2:
            out.append(i[0] + '/' + i[1])
    return out


def print_status(next_ips, ips):
    sleep(1)
    if print_status.output_counter % 600 == 0:
        mnmap_msg('STATUS: up to ' + str(next_ips) + ' of ' + str(len(ips)))

    print_status.output_counter = print_status.output_counter + 1

def init_argparser(parser):
    parser.add_argument('-a, --action', required=True, help='take 1 of 2 values (start or resume), start or resume scanning', dest='action', type=str)

    parser.add_argument('-t, --threads', required=False, help='number of maximum thread for doing scanning (each thread will handle one line in the input file)', dest='threads', type=int)

    parser.add_argument('-i, --input', required=False, help='input file for scanning, line seperated ip, ip range or hostname', dest='input', type=str)

def remove_thread(threads, running_ips):
    for k in list(threads):
        if k.is_alive()==False:
            # remove the thread from running_ips dict
            del running_ips[k.name]

            mnmap_msg('remove the thread "' + str(k) + '"')
            threads.remove(k)
            mnmap_msg('running threads after removed: ' + str(threads))
            mnmap_msg('running_ips after removed: ' + str(running_ips))

def kill_process_using_port(ports):
    popen = subprocess.Popen(['netstat', '-lpn'],
                             shell=False,
                             stdout=subprocess.PIPE)
    (data, err) = popen.communicate()

    pattern = "^tcp.*((?:{0})).* (?P<pid>[0-9]*)/.*$"
    pattern = pattern.format(')|(?:'.join(ports))
    prog = re.compile(pattern)
    for line in data.split('\n'):
        match = re.match(prog, line)
        if match:
            pid = match.group('pid')
            subprocess.Popen(['kill', '-9', pid])
