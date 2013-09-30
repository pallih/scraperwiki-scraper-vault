def searchname(fname, lname, id, stateid):
    url = 'http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname= %s &lastname= %s &countryid=1&stateid=%s&affiliateid=all' % (fname, lname, stateid)
    obits=urlopen(url)
    soup=BeautifulSoup(obits)
    obits_links=soup.findAll("div", {"class":"obitName"})
    print obits_links
    s = str(obits_links)
    id2 = int(id)
    f.write(s)
    #save the database here
    scraperwiki.sqlite.save(unique_keys=['id2'], data=['id2', 'fname', 'lname', 'state_id', 's'])


# Import Data from CSV
import scraperwiki
data = scraperwiki.scrape("https://dl.dropbox.com/u/14390755/legacy.csv")
import csv
reader = csv.DictReader(data.splitlines())
for row in reader:
    #scraperwiki.sqlite.save(unique_keys=['id'], 'fname', 'lname', 'state_id', data=row)
    FNAME = str(row['fname'])
    LNAME = str(row['lname'])
    ID = str(row['id'])
    STATE = str(row['state_id'])
    print "Person: %s %s" % (FNAME,LNAME)
    searchname(FNAME, LNAME, ID, STATE)


f.close()
f = open('/tmp/workfile', 'r')
data = f.read()
print dataimport scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin
def searchname(fname, lname, id, stateid):
    url = 'http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname= %s &lastname= %s &countryid=1&stateid=%s&affiliateid=all' % (fname, lname, stateid)
    obits=urlopen(url)
    soup=BeautifulSoup(obits)
    obits_links=soup.findAll("div", {"class":"obitName"})
    print obits_links
    s = str(obits_links)
    id2 = int(id)
    f.write(s)
    #save the database here
    scraperwiki.sqlite.save(unique_keys=['id2'], data=['id2', 'fname', 'lname', 'state_id', 's'])


# Import Data from CSV
import scraperwiki
data = scraperwiki.scrape("https://dl.dropbox.com/u/14390755/legacy.csv")
import csv
reader = csv.DictReader(data.splitlines())
for row in reader:
    #scraperwiki.sqlite.save(unique_keys=['id'], 'fname', 'lname', 'state_id', data=row)
    FNAME = str(row['fname'])
    LNAME = str(row['lname'])
    ID = str(row['id'])
    STATE = str(row['state_id'])
    print "Person: %s %s" % (FNAME,LNAME)
    searchname(FNAME, LNAME, ID, STATE)


f.close()
f = open('/tmp/workfile', 'r')
data = f.read()
print data