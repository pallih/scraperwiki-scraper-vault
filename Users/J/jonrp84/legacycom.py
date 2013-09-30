import scraperwiki

from urllib import urlopen
from BeautifulSoup import BeautifulSoup

f = open('/tmp/workfile', 'w')
#read database, find last, start from there

def searchname(fname, lname, id, stateid):
    url = 'http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname= %s &lastname= %s &countryid=1&stateid=%s&affiliateid=all' % (fname, lname, stateid)
    obits=urlopen(url)
    soup=BeautifulSoup(obits)
    obits_links=soup.findAll("div", {"class":"obitName"})
    #print obits_links
    s = str(obits_links)
    id2 = str(id)
    f.write(s)
    #save the database here
    #savefiles = ['id2', 'fname', 'lname', 'stateid', 's']
    #data = { 'id2': id2, 'fname':fname, 'lname':lname, 'state_id':state_id, 's':s]
    #scraperwiki.sqlite.save([id2], savefiles)


# Import Data from CSV
import scraperwiki
data = scraperwiki.scrape("https://dl.dropbox.com/u/14390755/legacy.csv")
import csv
reader = csv.DictReader(data.splitlines())
for row in reader:
    #scraperwiki.sqlite.save(unique_keys=['id'], 'fname', 'lname', 'state_id', data=row)
    FNAME = str(row['fname'])
    LNAME = str(row['lname'])
    ID = int(row['id'])
    STATE = str(row['state_id'])
    print "Person: %s %s" % (FNAME,LNAME)
    searchname(FNAME, LNAME, ID, STATE)
    if ID >= 30:
        break


f.close()
f = open('/tmp/workfile', 'r')
data = f.read()
print data



#for name in FNAME
#    searchname(FNAME, LNAME)




#for name in FNAME:
#    ad_list=urlopen('http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname=%s&lastname=%s&countryid=1&stateid=0&affiliateid=all').read(), %(FNAME, LNAME)
#    soup=BeautifulSoup(ad_list)
#    print soup
#    ad_link=soup.findAll("div", {"class":"obitName"})
#    print ad_link

#loop using info from csv





import scraperwiki

from urllib import urlopen
from BeautifulSoup import BeautifulSoup

f = open('/tmp/workfile', 'w')
#read database, find last, start from there

def searchname(fname, lname, id, stateid):
    url = 'http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname= %s &lastname= %s &countryid=1&stateid=%s&affiliateid=all' % (fname, lname, stateid)
    obits=urlopen(url)
    soup=BeautifulSoup(obits)
    obits_links=soup.findAll("div", {"class":"obitName"})
    #print obits_links
    s = str(obits_links)
    id2 = str(id)
    f.write(s)
    #save the database here
    #savefiles = ['id2', 'fname', 'lname', 'stateid', 's']
    #data = { 'id2': id2, 'fname':fname, 'lname':lname, 'state_id':state_id, 's':s]
    #scraperwiki.sqlite.save([id2], savefiles)


# Import Data from CSV
import scraperwiki
data = scraperwiki.scrape("https://dl.dropbox.com/u/14390755/legacy.csv")
import csv
reader = csv.DictReader(data.splitlines())
for row in reader:
    #scraperwiki.sqlite.save(unique_keys=['id'], 'fname', 'lname', 'state_id', data=row)
    FNAME = str(row['fname'])
    LNAME = str(row['lname'])
    ID = int(row['id'])
    STATE = str(row['state_id'])
    print "Person: %s %s" % (FNAME,LNAME)
    searchname(FNAME, LNAME, ID, STATE)
    if ID >= 30:
        break


f.close()
f = open('/tmp/workfile', 'r')
data = f.read()
print data



#for name in FNAME
#    searchname(FNAME, LNAME)




#for name in FNAME:
#    ad_list=urlopen('http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname=%s&lastname=%s&countryid=1&stateid=0&affiliateid=all').read(), %(FNAME, LNAME)
#    soup=BeautifulSoup(ad_list)
#    print soup
#    ad_link=soup.findAll("div", {"class":"obitName"})
#    print ad_link

#loop using info from csv





