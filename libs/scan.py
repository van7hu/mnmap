import sys 
from multiprocessing import Process
from time import sleep
from threads import nmap_start_runner, nmap_resume_runner
import state, aux
from datetime import datetime

def scan(max_thread):
    # if sys.argv[0] == start, new scan
    # if sys.argv[0] == resume, resume scan
    
    ips = []
    threads = []
    running_ips = {}
    next_ips = 0

    if len(sys.argv) != 2:
        print 'At ['+ str(datetime.now()) + '] script, you must provide an argument!'
        exit(1)

    if sys.argv[1] == 'start':
        ips = aux.read_init_file('init.ip')

        print 'At ['+ str(datetime.now()) + '] script, you have chosen "start"'
        for i in range(max_thread):
            t = Process(target = nmap_start_runner, args = (ips[i],))
            t.daemon = True
            t.start()
            threads.append(t) 

            running_ips[t.name] = ips[i]

        print 'At ['+ str(datetime.now()) + '] script, initial threads: ' + str(threads)
        next_ips = max_thread
    
    elif sys.argv[1] == 'resume':
        print 'At ['+ str(datetime.now()) + '] script, you have chosen "resume"'
        next_ips = state.load_state(threads, ips, running_ips)

    else:
        print sys.argv[1]
        print 'At ['+ str(datetime.now()) + '] script, please use start/resume'
        exit(1)

    while True:
        state.check_for_save(threads, ips, running_ips, next_ips)
        aux.test_network(threads, ips, running_ips, next_ips)
        aux.print_status(next_ips, ips)
        for k in list(threads):
            if k.is_alive()==False:
                print 'At ['+ str(datetime.now()) + '] script, remove the thread "' + str(k) + '"'
                threads.remove(k)
                print 'At ['+ str(datetime.now()) + '] script, list of currently running threads after killed: ' + str(threads)

        if len(threads) < max_thread:
            
            if scan.start_flag == True:
                if next_ips < len(ips):
                    print 'At ['+ str(datetime.now()) + '] script, a thread of scan has finished, starting a new one'
                    t = Process(target = nmap_start_runner, args = (ips[next_ips],))
                    t.daemon = True
                    t.start()
                    next_ips = next_ips + 1
                    threads.append(t)
                    print 'At ['+ str(datetime.now()) + '] script, threads after added new one: ' + str(threads)
                else:
                    print 'At ['+ str(datetime.now()) + '] script, we have iterate over all the init lines'
                    break
            else:
                # do nothing
                pass

    while True:
        state.check_for_save(threads, ips, running_ips, next_ips)
        aux.test_network(threads, ips, running_ips)
        aux.print_status(next_ips, ips)

        for k in list(threads):
            if k.is_alive()==False:
                print 'At ['+ str(datetime.now()) + '] script, remove the thread "' + str(k) + '"'
                threads.remove(k)
                print 'At ['+ str(datetime.now()) + '] script, list of currently running threads after killed: ' + str(threads)

        if(len(threads)==0):
            print 'At ['+ str(datetime.now()) + '] script, we have finished, get out!'
            exit(0)    

