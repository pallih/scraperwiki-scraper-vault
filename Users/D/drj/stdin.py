# Demonstrate reading from stdin.
# Pointless, but possible.
import sys

if False:
    import os
    os.close(0)

print sys.stdin.readline()
