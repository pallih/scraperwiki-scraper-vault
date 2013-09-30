import scraperwiki
import BeautifulSoup
import itertools

from scraperwiki import datastore


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

#scrape page
html = scraperwiki.scrape('http://adaderana.lk')
page = BeautifulSoup.BeautifulSoup(html)

results = []

#find rows
for row in page.findAll('table')[2].findAll('tr'):
    try:
        results.append(row.findAll('a')[1].string)
        results.append(row.findAll('a')[1]['href'])
    except:
        pass

result = [list(g) for g in grouper(4,results)]

for article in result:
    data = {'title':article[0],'link':article[1],'comments':article[2],'discuss':"http://adaderana.lk/{0}".format(article[3]),}
    scraperwiki.datastore.save(unique_keys=['title'], data=data)
import scraperwiki
import BeautifulSoup
import itertools

from scraperwiki import datastore


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

#scrape page
html = scraperwiki.scrape('http://adaderana.lk')
page = BeautifulSoup.BeautifulSoup(html)

results = []

#find rows
for row in page.findAll('table')[2].findAll('tr'):
    try:
        results.append(row.findAll('a')[1].string)
        results.append(row.findAll('a')[1]['href'])
    except:
        pass

result = [list(g) for g in grouper(4,results)]

for article in result:
    data = {'title':article[0],'link':article[1],'comments':article[2],'discuss':"http://adaderana.lk/{0}".format(article[3]),}
    scraperwiki.datastore.save(unique_keys=['title'], data=data)
