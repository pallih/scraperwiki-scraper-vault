import scraperwiki

html = scraperwiki.scrape('http://www.stat.cmu.edu/~larry/all-of-statistics/=data/faithful.dat')
start = False

for row in html.splitlines():
    if start:
        data = row.split()
        scraperwiki.sqlite.save(unique_keys=[], data = {'eruptions' : data[1], 'waiting' : data[2]})
    elif row == '    eruptions waiting': 
        start = True

