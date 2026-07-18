import sys
import subprocess

p = subprocess.Popen(['.venv/bin/python3', '-m', 'dirsearch.dirsearch', '-u', 'http://example.com', '-t', '1', '-e', 'php'], stdout=subprocess.PIPE, text=False, bufsize=1)
out = p.stdout.read(1500)
print(list(out[-50:]))
p.terminate()
