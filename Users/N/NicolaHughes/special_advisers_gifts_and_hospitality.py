import scraperwiki
import urllib
import csv
import lxml.html
import datetime
import dateutil.parser           


def parsemonths(d):
    d = d.strip()
    print d
    return dateutil.parser.parse(d).date()

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    if len(header) > 5:
        header.pop(5)
    if header[1] == 'Name of Adviser':
        header[1] = 'Name of Special Adviser'
    if header[2] == 'Date received':
        header[2] = 'Date of Hospitality'
    if header[3] == 'From':
        header[3] = 'Name of Organisation'
    if header[4] == 'Gift':
        header[4] = 'Type of hospitality received'
    #print header
    rownumber = 1
    entry0 = ''
    entry1 = ''
    entry3 = ''
    entry4 = ''
    
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
        if row[4] != '':
            entry4 = row[4]
        else:
            row[4] = entry4
        if row[2] != "" and row[2] != 'nil return':
        
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            data['Date of Hospitality'] = parsemonths(data['Date of Hospitality'])
            print data
    
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/special-advisers-gifts-hospitality").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" in anyurl:
        links(anyurl)
