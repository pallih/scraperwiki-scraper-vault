import scraperwiki
import os
print os.getpid()
os.kill(os.getpid(), 9)

