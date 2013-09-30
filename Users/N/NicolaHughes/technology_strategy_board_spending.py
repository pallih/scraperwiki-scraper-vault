import scraperwiki
import urllib
import urlparse
import csv
import lxml.html

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    header = []
    clist = list(csv.reader(lines))
    while clist[0][3] == "":
        clist.pop(0)
    header = clist.pop(0)
    header[6] = header[6].strip()
    if header[6] == 'Base Amount':
        header[6] = 'Amount'
    if header[1] == ' Area':
        header[1] = 'Expense Area'
    print header

    rownumber = 1

    for row in clist:
        if row[1] != "":
            rownumber += 1
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Amount'] = float(row[6].replace(',', ''))
            print data
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
mainurl = "http://www.innovateuk.org/aboutus/public-data.ashx"
root = lxml.html.parse(mainurl).getroot()
anchors = root.cssselect("div.elContent a")

for el in anchors:
    anyurl = el.attrib.get("href")
    if (".csv" in anyurl) and ("overview" not in anyurl):
        url = urlparse.urljoin(mainurl, anyurl).replace(" ","%20")
        print url
        links(url)
import scraperwiki
import urllib
import urlparse
import csv
import lxml.html

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    header = []
    clist = list(csv.reader(lines))
    while clist[0][3] == "":
        clist.pop(0)
    header = clist.pop(0)
    header[6] = header[6].strip()
    if header[6] == 'Base Amount':
        header[6] = 'Amount'
    if header[1] == ' Area':
        header[1] = 'Expense Area'
    print header

    rownumber = 1

    for row in clist:
        if row[1] != "":
            rownumber += 1
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Amount'] = float(row[6].replace(',', ''))
            print data
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
mainurl = "http://www.innovateuk.org/aboutus/public-data.ashx"
root = lxml.html.parse(mainurl).getroot()
anchors = root.cssselect("div.elContent a")

for el in anchors:
    anyurl = el.attrib.get("href")
    if (".csv" in anyurl) and ("overview" not in anyurl):
        url = urlparse.urljoin(mainurl, anyurl).replace(" ","%20")
        print url
        links(url)
