import scraperwiki, csv, urllib2
from BeautifulSoup import BeautifulSoup

# read country ids from geonames countryInfo.txt

ci_src = "http://download.geonames.org/export/dump/countryInfo.txt"
ci_raw = urllib2.urlopen(ci_src)
countryInfo = csv.reader(ci_raw, dialect='excel-tab')

countryIds = {}

uk = ["num"] # unique keys

for row in countryInfo:
    if row[0][0] == "#": continue
    countryIds[row[2]] = row


# scrape UN geographical regions

# gr_src = "http://unstats.un.org/unsd/methods/m49/m49regin.htm"

# as of 2012/01/13, the official page had an error in the html table
# which broke the scraper. I fixed this by coping the relevant table
# to a separate location on my webserver

gr_src = "http://vis4.net/tmp/ungeoregions.html"
soup = BeautifulSoup(scraperwiki.scrape(gr_src))

tables = soup.findAll('table')
table = tables[len(tables)-1]

cur_cont = '-'
cur_region = '-'

cheader2 = 0

rows = []

def store_row(num,name,level):
    num = num.strip()
    if name is None:
        print "warning: name must not be none", num, name, level
        return
    row = {'num':num, 'name':name.strip(), 'level': level, 'cont': cur_cont.strip(), 'region': cur_region.strip() }
    if num in countryIds:
        row['iso2'] = countryIds[num][0]
        row['iso3'] = countryIds[num][1]
    # print row
    rows.append(row)
    

def store_continent(num,name):
    global cur_cont, cur_region
    cur_cont = num
    cur_region = '-'
    store_row(num,name,'continent')

def store_region(num,name):
    global cur_region
    cur_region = num
    store_row(num,name,'region')

def store_country(num,name):
    store_row(num,name,'country')

trs = table.findAll('tr')
print 'found %d table rows' % len(trs)

for tr in trs:
    tds = tr.findAll('td')
    if len(tds) == 0: continue
    if tds[0]['class'] == 'cheader2':
        cheader2 += 1
        if cheader2 > 1:
            print 'exit'
            break # exit at second cheader2 row
        continue

    num_p = tds[0].find('p')
    num = None
    if num_p is None:
        num = tds[0].string
    else:
        if num_p.string is not None:
            num = num_p.string
        else:
            num_span = num_p.find('span')
            if num_span is not None and num_span.string is not None:
                num = num_span.string

    if num is None:
        print num_p, tds[0]
        break
    num = num.strip()
    if num == "" or num == "&nbsp;":
        continue

    print num,

    name = tds[1].find('h3')
    if name is not None:
        spans = name.findAll('span')
        if spans is not None and len(spans) > 0:
            if spans[0].string is None:
                name = spans[0].contents[1]
            else:
                name = spans[0].string
            store_continent(num,name)
            continue
        else:
            b = name.findAll('b')
            if len(b) > 0 and b[0].string is not None:
                name = b[0].string
                store_continent(num,name)
            elif b[0].contents[1] is not None:
                name = b[0].contents[1]
                store_continent(num,name)
                continue

    # check if we have a region (second td contains <b>)
    b = tds[1].findAll('b')
    if len(b) > 0 and b[0].string is not None:
        name = b[0].string
        store_region(num, name)
        continue

    name = tds[1].find('p')
    if name is not None:
        if name.string is not None:
            name = name.string
            store_country(num, name)
            continue

        name_span = name.find('span')
        if name_span is not None and name_span.string is not None:
            name = name_span.string
            store_country(num, name)
            continue
        #print 'continent', tds[0], tds[1]

    if tds[1].string is not None:
        name = tds[1].string
        store_country(num,name)
        continue

    print 'not handled:', tds[1]

scraperwiki.sqlite.save(unique_keys=uk, data=rows)