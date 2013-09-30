import subprocess

host = "google.com"

ping = subprocess.Popen(
    ["ping", "-c", "4", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

out, error = ping.communicate()
for r in out.split('\n'):
    print rimport subprocess

host = "google.com"

ping = subprocess.Popen(
    ["ping", "-c", "4", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

out, error = ping.communicate()
for r in out.split('\n'):
    print r