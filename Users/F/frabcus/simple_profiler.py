import scraperwiki
import datetime

start = datetime.datetime.now()
print start

scraperwiki.scrape("http://media.scraperwiki.com/images/nav_logo.png")

middle = datetime.datetime.now()
print middle

scraperwiki.sqlite.save(['id'], { 'id': 1, 'animal': 'cow', 'noise': 'moo' })

end = datetime.datetime.now()
print end

print end - start 


# 2011-05-16, 18:47 - 0:00:05.893002




import scraperwiki
import datetime

start = datetime.datetime.now()
print start

scraperwiki.scrape("http://media.scraperwiki.com/images/nav_logo.png")

middle = datetime.datetime.now()
print middle

scraperwiki.sqlite.save(['id'], { 'id': 1, 'animal': 'cow', 'noise': 'moo' })

end = datetime.datetime.now()
print end

print end - start 


# 2011-05-16, 18:47 - 0:00:05.893002




