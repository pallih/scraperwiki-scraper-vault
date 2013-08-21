import resource
import scraperwiki
import sys

# We artificially lower the soft CPU limit to 2 seconds, so that we
# run this scraper and see the exception in reasonable time.
resource.setrlimit(resource.RLIMIT_CPU, (2, 4))

# A loop that consumes CPU
a=2
try:
    while True:
        print a
        a = a*a
except scraperwiki.Exception as e:
    if 'CPU' in str(e):
        print "CPU exception caught"
    else:
        print "Error, unexpected exception"

