#!/usr/bin/python3
import os

rc_local = "/etc/rc.local"
line_to_add = os.path.join(os.getcwd(), 'autostart.sh')
line_to_add = line_to_add.replace(" ", "\\ ")

with open(rc_local) as f:
    content = f.read()

added = False
with open(rc_local, 'w') as f:
    for line in content.splitlines():
        if line_to_add.strip() == line.strip():
            added = True
        if not added and line.strip().startswith("exit"):
            f.write(line_to_add + "\n")
            added = True
        f.write(line + "\n")
