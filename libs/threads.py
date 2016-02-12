import os, sys
import aux

pro = 'nmap'
STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2
from datetime import datetime

def redirect_output(dir):
    # redirect stdout            
    new_stdout = os.open(os.path.join(dir, 'nmap.out'), os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    os.dup2(new_stdout, STDOUT_FILENO)

    # redirect stderr
    new_stderr = os.open(os.path.join(dir, 'nmap.err'), os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    os.dup2(new_stderr, STDERR_FILENO)

def nmap_start_runner(ip, dir):
    outfile = ip.replace('/', '..')
    outfile = os.path.join(dir, outfile)
    args = ['nmap', '-sV', '-O', '-Pn', '-oX',outfile + '.xml', '-o', outfile + '.out', ip]
    aux.mnmap_msg('starting: '+ pro + ' ' + str(args))

    redirect_output(dir)
    os.execvp(pro, args)

def nmap_resume_runner(ip, dir):  
    outfile = ip.replace('/', '..')
    outfile = os.path.join(dir, outfile)
    args = ['nmap', '--resume', outfile + '.out']
    aux.mnmap_msg('starting: ' + pro + ' ' + str(args))

    redirect_output(dir)
    os.execvp(pro, args)

