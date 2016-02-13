import os

def correct_and_process_me(out, dir):
    if os.stat(os.path.join(dir, 'err.xslt')).st_size == 0:
        cmd = 'xsltproc ' + os.path.join(dir, out) + '.xml -o ' + os.path.join('html/', out + '.html') + '>/dev/null'
        os.system(cmd)
        return

    with open('err.xslt', 'r') as f:
        a1 = f.readlines()

    a2 = []
    for i in range(0, len(list(a1))-1):
        if i % 3 == 0:
            a2.append(a1[i])

    a3 = []
    for i in a2:
        a3.append(i.split(':')[1])

    a3.sort()

    with open(os.path.join(dir, out+'.xml'), 'r') as f:
        lines = f.readlines()
    
    candle = len(lines)

    for i in reversed(a3):
        if (int(i)-1) == candle:
            lines.append('</nmaprun>')
        else:
            del lines[int(i)-1]

    with open(os.path.join(dir, out+'.xml'), 'w') as f:
        for line in lines:
            f.write(line)

    cmd = 'xsltproc ' + os.path.join(dir, out) + '.xml -o ' + os.path.join('html/' + '.html') + '>/dev/null'
    os.system(cmd)

    
    
