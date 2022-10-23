#!/usr/bin/python3

import glob
import os

START = '# Automatically added by '
END = '# End automatically added section'
OUT = 'split'

def mkdir_p(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

mkdir_p(OUT)

for postrm in glob.glob('unstable/*/postrm'):
    package = os.path.basename(os.path.dirname(postrm))
    package_dir = os.path.join(OUT, package)

    lines_hardcoded = list()
    helper = None
    lines_helper = list()

    with open(postrm, 'r') as concatenated:
         for line in concatenated:
             line = line.strip('\n').rstrip(' ')

             # unstable/spamass-milter/postrm
             while(line.startswith('##')):
                 line = line[1:]

             # unstable/ganglia-monitor/postrm
             if line and line[0] != '#' and line.lstrip(' ')[0] == '#':
                 line = line.lstrip(' ')

             if line.startswith(START):
                 helper = line[len(START):].split('/')[0]
                 if helper.startswith('dh_'):
                     helper = helper[4:]
             elif line == END and not helper:
                 print('Borked file: %s' % postrm)
             elif line == END:
                 mkdir_p(package_dir)
                 dest = os.path.join(package_dir, helper)
                 with open(dest, 'w') as splitted:
                     splitted.write('\n'.join(lines_helper))
                 helper = None
                 lines_helper = list()
             elif helper:
                 lines_helper.append(line)
             elif line and not line.startswith('#') and line != 'set -e':
                 lines_hardcoded.append(line)

    if lines_hardcoded:
        mkdir_p(package_dir)
        dest = os.path.join(package_dir, 'postrm')
        with open(dest, 'w') as splitted:
            splitted.write('\n'.join(lines_hardcoded))

