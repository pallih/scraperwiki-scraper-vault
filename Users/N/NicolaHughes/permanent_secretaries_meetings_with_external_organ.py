import scraperwiki
import urllib
import csv
import lxml.html

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def links(url):
    #print url
    lines = urllib.urlopen(url).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    print header
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
        
        if row[2] != "":
        
            data = dict(zip(header, row)) 
            data['Row_Number'] = rownumber
            data['URL'] = url
            imonth = months.index(data['Date'].strip())+1
            data['Date'] = "2010-%02d" %imonth
            print data
    
            scraperwiki.sqlite.save(unique_keys=['Row_Number', 'URL'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/cabinet-office-permanent-secretaries%25E2%2580%2599-meetings-external-organisations").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")
    #print anyurl
    
    if ".csv" in anyurl:
        links(anyurl)
