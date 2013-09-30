import scraperwiki
from time import strftime

now = strftime("%Y-%m-%dT%H:%M:%SZ")

print now

scraperwiki.sqlite.save(['t'], {'t': now})
import scraperwiki
from time import strftime

now = strftime("%Y-%m-%dT%H:%M:%SZ")

print now

scraperwiki.sqlite.save(['t'], {'t': now})
