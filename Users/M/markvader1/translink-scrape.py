import scraperwiki
import urllib, urlparse
import lxml.etree
import lxml.html
import re

url = "http://www.translink.co.uk/Timetables/Enterprise-Timetables/Enterprise-Service-5-Outbound/"

def Main():
    element = lxml.html.parse(url).getroot()
    element1 = element
    r = 0

    rows = []

    for tr in element.cssselect('tr'):
        row = []
        record = {}
    for td in tr.cssselect('th,td'):
            text = td.text.strip()
            if text == '...':
                text = ''
            row.append(text)
            rows.append(row)

    assert rows
    fl = len(rows[0])
    for row in rows:
        assert len(row) == fl
    return rows

def parseDate(s):
    vf = [int(t, 10) for t in s.split('/')]
    if vf[0] == 99:
        return date.today() + timedelta(days=365)
    return date(2000+vf[2], vf[1], vf[0])

def timeToMinOfDay(timeObj):
    return (timeObj.hour * 60) + timeObj.minute


#        record = {}

#        print list(tr), lxml.etree.tostring(tr)

#        date_range = tr[0].text.split('\r\n\t\t\t- ')
#        if len(date_range) == 2:
#        record['date_to'] = date_range[1].strip()
    record['Regular operator:&nbsp;'] = tr.text
    print record
scraperwiki.datastore.save(["Translink_Scrape"], record)
       
Main()


#from BeautifulSoup import BeautifulSoup
#soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
#tables = soup.findAll('table') # get all the <td> tags
#for table in tables:
#    print table  # the full HTML tag
#    print table.text # just the text inside the HTML tag


#for table in tables:
#     record = { "table" : table.text } # column name and value
#     scraperwiki.datastore.save(["table"], record) # save the records one by oneimport scraperwiki
import urllib, urlparse
import lxml.etree
import lxml.html
import re

url = "http://www.translink.co.uk/Timetables/Enterprise-Timetables/Enterprise-Service-5-Outbound/"

def Main():
    element = lxml.html.parse(url).getroot()
    element1 = element
    r = 0

    rows = []

    for tr in element.cssselect('tr'):
        row = []
        record = {}
    for td in tr.cssselect('th,td'):
            text = td.text.strip()
            if text == '...':
                text = ''
            row.append(text)
            rows.append(row)

    assert rows
    fl = len(rows[0])
    for row in rows:
        assert len(row) == fl
    return rows

def parseDate(s):
    vf = [int(t, 10) for t in s.split('/')]
    if vf[0] == 99:
        return date.today() + timedelta(days=365)
    return date(2000+vf[2], vf[1], vf[0])

def timeToMinOfDay(timeObj):
    return (timeObj.hour * 60) + timeObj.minute


#        record = {}

#        print list(tr), lxml.etree.tostring(tr)

#        date_range = tr[0].text.split('\r\n\t\t\t- ')
#        if len(date_range) == 2:
#        record['date_to'] = date_range[1].strip()
    record['Regular operator:&nbsp;'] = tr.text
    print record
scraperwiki.datastore.save(["Translink_Scrape"], record)
       
Main()


#from BeautifulSoup import BeautifulSoup
#soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
#tables = soup.findAll('table') # get all the <td> tags
#for table in tables:
#    print table  # the full HTML tag
#    print table.text # just the text inside the HTML tag


#for table in tables:
#     record = { "table" : table.text } # column name and value
#     scraperwiki.datastore.save(["table"], record) # save the records one by one