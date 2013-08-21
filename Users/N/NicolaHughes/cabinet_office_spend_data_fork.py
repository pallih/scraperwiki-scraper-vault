import scraperwiki
import urllib
import csv
import urllib2 
import lxml.html        

def links(url): 
    print url
    lines = urllib.urlopen(url.replace(' ','%20')).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    header = header[:9]
    for i in range(9):
            header[i] = header[i].strip()
    if header[8] == 'Descriptions':
        header[8] = 'Description'
    
    if header[7] == 'Amount £':
        header[7] = 'Amount'
    
    for row in clist:
        if row[2] != "":        
            data = dict(zip(header, row)) 
            data['URL'] = url
            print data

        scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'], data=data)

root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/cabinet-office-spend-data").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")

    if (".csv" in anyurl) and ("gpc" not in anyurl):
        links(anyurl)



