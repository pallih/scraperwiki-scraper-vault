import scraperwiki
import urllib
import csv
import lxml.html
import datetime
import dateutil.parser           

def parsemonths(d):
    d = d.strip()
    print d
    #print len(data['Date'])
    if d == "Nov-2010":
        return "2010-11"
    if d == "Dec-2010":
        return "2010-12"
    if d=="August, 2010":
        return "2010-8"
    return dateutil.parser.parse(d).date()
        

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    if header[1] == 'Date':
        header[1] = 'Date of Hospitality'
    if len(header) >= 5:
        header.pop(5)
    header = [h.strip() for h in header if len(h.strip()) >0]

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
        #if row[4] != '':
            #del row[4]
        
        if row[2] != "" and row[2] != 'nil return':
            for x in row[:4]:
                print header
                data = dict(zip(header, row)) 
                data['Row_Number'] = rownumber
                data['URL'] = url
                data['Date of Hospitality'] = parsemonths(data['Date of Hospitality'])
                print data
                print data['Date of Hospitality']
    
                scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/ministerial-gifts-hospitality-travel-and-meetings-external-organisations").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" and "hospitality" in anyurl:
        links(anyurl)

