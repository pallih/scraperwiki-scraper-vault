import scraperwiki
import urllib
import csv
import lxml.html

shortmonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
longmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def parsemonths(d):
    d = d.strip()
    print d
    if d=="21-Sep-2010":
        return "2010-09"
    if d=="10-Sep-2010":
        return "2010-09"
    if len(d)==8:
        #print (d[:3])
        imonth = shortmonths.index(d[:3])+1
        d = "20%s-%02d" % (d[-2:], imonth)
    else:
        #print (d[:-6])
        imonth = longmonths.index(d[:-5])+1
        d = "20%s-%02d" % (d[-2:], imonth)
        
    return d

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)    
    header = clist.pop(0)
    if header[4] == 'Value (\xc3\x82\xc2\xa3)' or 'Value (\xc2\xa3)':
        header[4] = 'Value'
    
    rownumber = 1
    entry0 = ''
   
    for row in clist:
        rownumber += 1
        if row[0] != '':
            entry0 = row[0]
        else:
            row[0] = entry0
        
        if row[1] != "":
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Date received'] = parsemonths(data['Date received'])
            print data
    
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/ministerial-gifts-hospitality-travel-and-meetings-external-organisations").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" in anyurl and "gifts" in anyurl:
        links(anyurl)
import scraperwiki
import urllib
import csv
import lxml.html

shortmonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
longmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def parsemonths(d):
    d = d.strip()
    print d
    if d=="21-Sep-2010":
        return "2010-09"
    if d=="10-Sep-2010":
        return "2010-09"
    if len(d)==8:
        #print (d[:3])
        imonth = shortmonths.index(d[:3])+1
        d = "20%s-%02d" % (d[-2:], imonth)
    else:
        #print (d[:-6])
        imonth = longmonths.index(d[:-5])+1
        d = "20%s-%02d" % (d[-2:], imonth)
        
    return d

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)    
    header = clist.pop(0)
    if header[4] == 'Value (\xc3\x82\xc2\xa3)' or 'Value (\xc2\xa3)':
        header[4] = 'Value'
    
    rownumber = 1
    entry0 = ''
   
    for row in clist:
        rownumber += 1
        if row[0] != '':
            entry0 = row[0]
        else:
            row[0] = entry0
        
        if row[1] != "":
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Date received'] = parsemonths(data['Date received'])
            print data
    
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/ministerial-gifts-hospitality-travel-and-meetings-external-organisations").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" in anyurl and "gifts" in anyurl:
        links(anyurl)
