import scraperwiki
import lxml.html
from lxml import etree
import csv
import StringIO

#letters = ['a']
#Get shit ready...
data = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0AmzK_8HvP9mldHlxUTVseElrUjBiazFqMm5IUE9xNGc&single=true&gid=0&output=csv")

#Scrape CSV file
reader = csv.reader(data.splitlines())

#FOR EVERY MED IN CSV FILE...
for med in reader:
    
    #Get/Parse HTML
    url = "http://www.ncbi.nlm.nih.gov/pcsubstance/?db=pcsubstance&term=%s" % (med[0]);
    html = scraperwiki.scrape(url);
    
    
    #Parse HTML
    tree = etree.HTML(html)

    #Find target data and extract
    for a in tree.xpath("//div[@class='rprtnum nohighlight']/input[@sid='1']"):
        data = {
            'SID' : a.attrib['value'],
            'MEDICATION' : med[0]
        }
        scraperwiki.sqlite.save(unique_keys=['SID'], data=data)
        print data

import scraperwiki
import lxml.html
from lxml import etree
import csv
import StringIO

#letters = ['a']
#Get shit ready...
data = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0AmzK_8HvP9mldHlxUTVseElrUjBiazFqMm5IUE9xNGc&single=true&gid=0&output=csv")

#Scrape CSV file
reader = csv.reader(data.splitlines())

#FOR EVERY MED IN CSV FILE...
for med in reader:
    
    #Get/Parse HTML
    url = "http://www.ncbi.nlm.nih.gov/pcsubstance/?db=pcsubstance&term=%s" % (med[0]);
    html = scraperwiki.scrape(url);
    
    
    #Parse HTML
    tree = etree.HTML(html)

    #Find target data and extract
    for a in tree.xpath("//div[@class='rprtnum nohighlight']/input[@sid='1']"):
        data = {
            'SID' : a.attrib['value'],
            'MEDICATION' : med[0]
        }
        scraperwiki.sqlite.save(unique_keys=['SID'], data=data)
        print data

