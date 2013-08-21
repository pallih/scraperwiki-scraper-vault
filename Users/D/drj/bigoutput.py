import scraperwiki
import time

raise Exception("please do run this scraper")

t0 = time.time()
a = ('*'*100000+'\n')*100

while True:
    print a
    now = time.time()
    elapsed = now - t0
    if elapsed > 3*60:
        break
print elapsed