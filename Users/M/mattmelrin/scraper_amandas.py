import scraperwiki
from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

print soup.prettify()

print soup.find_all("table")
print len(soup.find_all("table"))  ##looks at the number of tables found (len=length)

## how many tables did that find?

#  not simple enough. So use the element inspector to confirm that we want  a table with <table border="0" cellspacing="1" cellpadding="2">

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})
print len(tables)

print tables

## Okay, so now let's get fancy:
for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()   #strip commmand gets rid of white spaces

## Let's find our header row:

rows = tables[1].find_all('tr')           #second table is table no. 1    #creates a new varible called row


for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()



#it looks like we have five columns in this table. So let's push this into a data store:

print "now for the data"

for row in rows:
    cells = row.find_all("td")
    print "there is/are", len(cells), "in this row"
    if len(cells) > 5: 
        print "rank", cells[0].get_text().strip()
        print "state", cells[1].get_text().strip()
        print 'total_filings', cells[2].get_text().strip()
        print '1_per_x' , cells[3].get_text().strip()


print "zero", cells[0]          #print zero is for array no. zero




for row in rows:
    cells = row.find_all("td")
    if len(cells) > 5:
        data = {
            'rank' : cells[0].get_text().strip(),
            'state' : cells[1].get_text().strip(),
            'total_filings' : cells[2].get_text().strip(),
            '1_per_x' : cells[3].get_text().strip(),
            'change_dec_jan' : cells[4].get_text().strip(),
            'change_jan08' : cells[5].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['state'],data=data)


import scraperwiki
from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

print soup.prettify()

print soup.find_all("table")
print len(soup.find_all("table"))  ##looks at the number of tables found (len=length)

## how many tables did that find?

#  not simple enough. So use the element inspector to confirm that we want  a table with <table border="0" cellspacing="1" cellpadding="2">

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})
print len(tables)

print tables

## Okay, so now let's get fancy:
for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()   #strip commmand gets rid of white spaces

## Let's find our header row:

rows = tables[1].find_all('tr')           #second table is table no. 1    #creates a new varible called row


for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()



#it looks like we have five columns in this table. So let's push this into a data store:

print "now for the data"

for row in rows:
    cells = row.find_all("td")
    print "there is/are", len(cells), "in this row"
    if len(cells) > 5: 
        print "rank", cells[0].get_text().strip()
        print "state", cells[1].get_text().strip()
        print 'total_filings', cells[2].get_text().strip()
        print '1_per_x' , cells[3].get_text().strip()


print "zero", cells[0]          #print zero is for array no. zero




for row in rows:
    cells = row.find_all("td")
    if len(cells) > 5:
        data = {
            'rank' : cells[0].get_text().strip(),
            'state' : cells[1].get_text().strip(),
            'total_filings' : cells[2].get_text().strip(),
            '1_per_x' : cells[3].get_text().strip(),
            'change_dec_jan' : cells[4].get_text().strip(),
            'change_jan08' : cells[5].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['state'],data=data)


