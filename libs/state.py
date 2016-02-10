import os, pickle
from multiprocessing import Process
from threads import nmap_start_runner, nmap_resume_runner
import scan
from datetime import datetime
import copy

def check_for_save(threads, ips, running_ips, next_ips, init_file):
    if os.path.exists('save'):
        save_state_exit(threads, ips, running_ips, next_ips, init_file)

class state:
    def __init__(self, ips, running_ips, next_ips, init_file):
        self.ips = ips # list of ip(s) to scan.
        self.running_ips = running_ips # list of ip(s), which is being scanned.
        self.next_ips = next_ips # next index in list of ip(s), which is going to be scanned.
	self.init_file = init_file
    
def save_state_exit(threads, ips, running_ips, next_ips, init_file):
    save_state(threads, ips, running_ips, next_ips, init_fukw)
    print 'At ['+ str(datetime.now()) + '] script, self-killing for exit. Good bye!'
    os.system('kill $PPID')

def save_state(threads, ips, running_ips, next_ips, init_file):

    # dont allow start new thread of scan

    print 'At ['+ str(datetime.now()) + '] script, saving state'
    print 'At ['+ str(datetime.now()) + '] script, killing all child-processes'

    print 'At ['+ str(datetime.now()) + '] script, threads before mass-kill: ' + str(threads)
    for t in threads:
        try:
            t.terminate()
        except:
            'At ['+ str(datetime.now()) + '] script, do not even try to kill a ZOMBIES'

    sstate = state(ips, running_ips, next_ips, init_file)

    with open('state.pickle', 'wb') as f:
        pickle.dump(sstate, f)

def load_state(threads, ips, running_ips):
    print 'At ['+ str(datetime.now()) + '] script, load the saved state'
    with open('state.pickle', 'rb') as f:
        sstate = pickle.load(f) 
   
    for i in reversed(ips):
        ips.remove(i)
    for i in sstate.ips:
        ips.append(i)

    for i in list(running_ips):
        del running_ips[i]
    tmp_running_ips = {}
    for i in sstate.running_ips:
        tmp_running_ips[i] = sstate.running_ips[i]

    for i in threads:
        threads.remove(i)

    dir = sstate.init_file + '.init'

    for v in tmp_running_ips.values():
        # check the number of line of output file, if it's less than, equal 1, treat as new scan
        vout = v.replace('/', '..') + '.out'
        with open(vout, 'r') as f:
            vlines = f.readlines()
           
        if len(vlines) <=1:
            t = Process(target = nmap_start_runner, args = (v, dir))
            t.daemon = True           
            t.start()
        else:
            t = Process(target = nmap_resume_runner, args = (v, dir)) 
            t.daemon = True       
            t.start()
        threads.append(t) 

        running_ips[t.name] = v

    print 'At ['+ str(datetime.now()) + '] script, threads after resumed: ' + str(threads)
    return sstate.next_ips, sstate.init_file
