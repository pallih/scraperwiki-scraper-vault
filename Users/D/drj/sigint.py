import os
import signal

pid=os.getpid()
print 'pid', pid
os.kill(pid, signal.SIGINT)