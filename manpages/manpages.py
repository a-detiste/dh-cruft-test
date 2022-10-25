#!/usr/bin/python3

# I am a dwarf and I'm digging a hole

# this is just a survey

import glob
import gzip
import re
import subprocess

dpkg = set(subprocess.check_output('cat /var/lib/dpkg/info/*.conffiles | sort -u', shell=True, text=True).splitlines())
dpkg.add('/etc')
dpkg_list = set(subprocess.check_output('cat /var/lib/dpkg/info/*.list | sort -u', shell=True, text=True).splitlines())
dpkg |= dpkg_list

cruft = set(subprocess.check_output('cat /home/tchet/cruft-ng/rules/* | grep ^/ | sort -u', shell=True, text=True).splitlines())

is_etc = re.compile(r'/etc/[a-zA-Z0-9/.$*\-]*')

for page in glob.glob('/usr/share/man/*/*gz'):
    with gzip.open(page, 'rt') as fin:
        for line in fin:
            line = line.strip()
            line = line.replace(r'\fB', '')
            line = line.replace(r'\fI', '')
            line = line.replace(r'\fP', '')
            line = line.replace(r'\fR', '')
            line = line.replace(r'\(cq', '')
            line = line.replace(r'\(Fc', '')
            line = line.replace(r'\(Fo', '')
            line = line.replace(r'\*(Aq', '')
            line = line.replace(r'\*(C', '')
            line = line.replace(r'\&.', '.')
            line = line.replace(r'\&', ' ')
            line = line.replace(r'\-', '-')
            for match in re.findall(is_etc, line):
                etc = match.rstrip('./')
                if etc in dpkg:
                    pass
                elif etc in cruft:
                    pass
                else:
                    print(etc)
