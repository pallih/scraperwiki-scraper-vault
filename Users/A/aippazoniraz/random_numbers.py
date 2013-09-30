import scraperwiki
import random

i = 0
data = []
while i < 10:
    data.append({'id' : random.randrange(1, 99999)})
    i+=1

scraperwiki.sqlite.save(['id'], data)import scraperwiki
import random

i = 0
data = []
while i < 10:
    data.append({'id' : random.randrange(1, 99999)})
    i+=1

scraperwiki.sqlite.save(['id'], data)