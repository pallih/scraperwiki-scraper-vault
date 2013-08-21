# A view which is slow, but does not consume many resources.
import sys
import time

print "starting..."
s = "Hello, world!"
for x in s:
    time.sleep(1)
    sys.stdout.write(x)