import sys, shutil, os
from multiprocessing import Process
from time import sleep
from threads import nmap_start_runner, nmap_resume_runner
import state, aux
from datetime import datetime
import web

def scan(max_thread, action, init_file):
    # if sys.argv[0] == start, new scan
    # if sys.argv[0] == resume, resume scan
    
    ips = []
    threads = []
    running_ips = {}
    next_ips = 0

    dir = init_file + '.dir'

    if action == 'start':
        aux.mnmap_msg("reading init file '" + init_file + "'")
        ips = aux.read_init_file(init_file)
        # check if there're previous scan
        shutil.rmtree(dir, True)
        os.mkdir(dir)

        aux.mnmap_msg('you have chosen to start new scanning')
        for i in range(max_thread):
            t = Process(target = nmap_start_runner, args = (ips[i], dir))
            t.daemon = True
            t.start()
            threads.append(t) 

            running_ips[t.name] = ips[i]

        aux.mnmap_msg('initial threads: ' + str(threads))
        next_ips = max_thread
    
    elif action == 'resume':
        aux.mnmap_msg('you have chosen to resume an old scanning')
        try:
            os.remove(os.path.join(init_file+'.dir', 'save'))
        except:
            pass
        next_ips = state.load_state(threads, ips, running_ips, init_file)

    else:
        aux.mnmap_msg('please use start/resume for your action')
        exit(1)

    while True:
        state.check_for_save(threads, ips, running_ips, next_ips, init_file)
        aux.test_network(threads, ips, running_ips, next_ips, init_file)
        aux.print_status(next_ips, ips)
        web.generate_html(ips, init_file, running_ips, next_ips)

        aux.remove_thread(threads, running_ips)

        if len(threads) < max_thread:
            
            if scan.start_flag == True:
                if next_ips < len(ips):
                    aux.mnmap_msg('currently, the number of thread running is less than specified, starting a new one')
                    t = Process(target = nmap_start_runner, args = (ips[next_ips], dir))
                    t.daemon = True
                    t.start()

                    threads.append(t)
                    running_ips[t.name] = ips[next_ips]
                    next_ips = next_ips + 1

                    aux.mnmap_msg('threads after added new one: ' + str(threads))
                    aux.mnmap_msg('running_ips after added new one: ' + str(running_ips))
                else:
                    aux.mnmap_msg('we have iterate over all the init lines')
                    break
            else:
                # do nothing
                pass

    while True:
        state.check_for_save(threads, ips, running_ips, next_ips, init_file)
        aux.test_network(threads, ips, running_ips, next_ips, init_file)
        aux.print_status(next_ips, ips)
        web.generate_html(ips, init_file, running_ips, next_ips)

        aux.remove_thread(threads, running_ips)

        if(len(threads)==0):
            aux.mnmap_msg('we have finished, get out!')
            exit(0)    

