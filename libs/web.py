import os, aux

def generate_html(ips, init_file, running_ips, next_ips):
    dir = init_file + '.dir'
    out_dir = 'html'

    fin = aux.read_init_file(init_file)

    counter = 0
    for i in range(len(ips)-1, next_ips, -1):
        fin.remove(fin[i])

    for i in reversed(fin):
        for k in running_ips.values():
            if i == k:
                fin.remove(i)
    out = []

    for i in fin:
        tmp = i.replace('/', '..')
        out.append(tmp)
    
    for k in out:
        os.system('xsltproc ' + os.path.join(dir, k + '.xml') + ' -o ' + os.path.join(out_dir, k + '.html'))
