from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib
import csv
import datetime

days4 = datetime.date.today() - datetime.timedelta(2)
days8 = datetime.date.today() - datetime.timedelta(4)

sourcescraper = "takeover-panel-info"

# get from the primary data
limit = 90
offset = 0
rows = list(getData(sourcescraper, limit, offset))


# join the human generated data from the spreadsheet

# couldn't download from google directly!!!  so had to cache the result
#url = "http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&exportFormat=csv"
url = 'http://seagrass.goatchurch.org.uk/~julian/takeoverpanel.csv'
url = 'https://spreadsheets.google.com/pub?key=0Aju6C2vCJrTNdEJkRkNGR1V4ZHJzWHRGR2x6cmEzN1E&output=csv'
fin = urllib.urlopen(url)

hdata = { }
lines = fin.readlines()
clist = list(csv.reader(lines))
headers = clist.pop(0)
for row in clist:
    hrow = dict(zip(headers, row))
    stockcode = hrow.get('OffereeStockCode')
    hrow['articles'] = [ ]
    if stockcode:
        hdata[stockcode] = hrow


rarticles = list(getData('takeover-panel-articles', 3000, 0))
for rart in rarticles:
    hrow = hdata.get(rart['stockcode'])
    if hrow:
        hrow['articles'].append(rart)

for row in rows:
    stockcode = row.get('OffereeStockCode')
    if stockcode:
        hrow = hdata.get(stockcode)
        if hrow:
            for k in ['Sector', 'Revenue (millions)', 'Web links']:
                if hrow.get(k):
                    row[k] = hrow[k]
            row['articles'] = hrow['articles']
            row['articles'].sort(key=lambda x:x.get('date'), reverse=True)

    row['latestnewsdate'] = row['commencedate']
    if row.get('articles'):
        row['latestnewsdate'] = row['articles'][0]['date']


rows.sort(key=lambda x:x.get('latestnewsdate'), reverse=True)

days4 = str(datetime.date.today() - datetime.timedelta(2))
days8 = str(datetime.date.today() - datetime.timedelta(4))
print '<style>th {background:#9090ff;} .days8 td {background:#ffdddd;} .days4 td {background:#ffaaaa;}</style>'

print '<h2>Takeover company views</h2>'
print '<p>The hottest press releases for the companies experiencing takeover procedures</p>'
print '<p>News from last 2 days in <span style="background:#ffaaaa;">red</span></p>'

print '<table border="1" style="border-collapse:collapse;">'
print '<tr><th>Date</th><th>Company</th><th>Sector</th><th>Revenue</th><th>Latest news</th><th>Offerer (if disclosed)</th></tr>'
for row in rows:
    link = 'http://www.investegate.co.uk/CompData.aspx?code=%s&tab=announcements' % row.get('OffereeStockCode')
    trcla = ''
    if row['latestnewsdate'] >= days8:
        trcla = 'days8'
    if row['latestnewsdate'] >= days4:
        trcla = 'days4'
    
    print '<tr class="%s"><td>%s</td> <td><a href="%s">%s</td>' % (trcla, row.get('commencedate')[:10], link, row.get('offeree'))
    rlink = row.get('Web links')
    revenue = row.get('Revenue (millions)') or ''
    if revenue and rlink:
        revenue = '<a href="%s">%s</a>' % (rlink, revenue)
    print '<td>%s</td><td>%s</td>' % (row.get('Sector') or '', revenue)
    if row.get('articles'):
        article = row.get('articles')[0]
        print '<td><a href="%s" title="%s">%s</a></td>' % (article['link'], article['date'], article['headline'])
    else:
        print '<td>no news</td>'
    print '<td>%s</td></tr>' % (row.get('offerer') or '')

print '</table>'



