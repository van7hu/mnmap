import os, sys

pro = 'nmap'
STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2
from datetime import datetime

def redirect_output():
    # redirect stdout            
    new_stdout = os.open('nmap.out', os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    os.dup2(new_stdout, STDOUT_FILENO)

    # redirect stderr
    new_stderr = os.open('nmap.err', os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    os.dup2(new_stderr, STDERR_FILENO)

def nmap_start_runner(ip):
    outfile = ip.replace('/', '..')
    args = ['-sV', '-O', '-Pn', '-o',outfile + '.out', ip]
    print 'At ['+ str(datetime.now()) + '] script, starting: '+ pro + ' ' + str(args)

    redirect_output()
    os.execvp(pro, args)

def nmap_resume_runner(ip):  
    outfile = ip.replace('/', '..')
    args = ['nmap --resume ', outfile + '.out']
    print 'At ['+ str(datetime.now()) + '] script, starting: ' + pro + str(args)

    redirect_output()
    os.execvp(pro, args)

