import scraperwiki
import urllib
import csv
import lxml.html

shortmonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
longmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def parsemonths(d):
    d = d.strip()
    #print len(data['Date'])
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
    lines = [ l.decode('iso8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)    
    header = clist.pop(0)
    header[0] = header[0].strip()
    if len(header) > 4:
        header.pop(4)
    if header[0] == '':
        header[0] = 'Minister'    
    if header[2] == 'Name of External Organisation':
        header[2] = 'Name of Organisation'
    #print header
    rownumber = 1
    entry0 = ''
    entry1 = ''
    entry3 = ''

    for row in clist:
        rownumber += 1
        if row[0] != '':
            entry0 = row[0]
        else:
            row[0] = entry0
        if row[1] != '':
            entry1 = row[1]
        else:
            row[1] = entry1
        if row[3] != '':
            entry3 = row[3]
        else:
            row[3] = entry3
        if row[2] != "" and row[1] != 'nil return':
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Date'] = parsemonths(data['Date'])
    
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/ministerial-gifts-hospitality-travel-and-meetings-external-organisations").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" in anyurl and "meetings" in anyurl:
        #print anyurl
        links(anyurl)
