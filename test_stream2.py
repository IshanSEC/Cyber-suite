import sys
import subprocess

cmd = ['.venv/bin/python3', '-m', 'dirsearch.dirsearch', '-u', 'http://example.com', '-t', '1', '-e', 'php']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
for i in range(20):
    line = p.stdout.readline()
    print(repr(line))
p.terminate()
