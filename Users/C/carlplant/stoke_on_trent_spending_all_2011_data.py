import scraperwiki
import urllib
import lxml.html
import urlparse
import csv
import re


def save_data(reader):
    #next_line = reader.next()
    #print next_line()
    record = {}
    for row in reader:
        
        record['Body Name'] = row[0]
        record['Code2'] = row[1]
        record[' Service Label '] = row[2]
        record['Exp code'] = row[3]
        record['Exp cat'] = row[4]
        record['Date'] = row[5]
        record['Trans Number'] = row[6]
        record['Amount'] = row[7]
        record['Supplier'] = row[8]
        print record
        scraperwiki.sqlite.save(['Trans Number'], data=record)

def scrape_doc(csv_link):
    data = scraperwiki.scrape(csv_link)
    trans_link = re.search("Body Name", data)
    #print trans_link
    if trans_link:
        
        #print "line is..." +data
        reader = csv.reader(data.splitlines()) 
        save_data(reader)
        #print reader
    

def table_scrape(table_cell2):
    csv_link = urlparse.urljoin(sotccweb, table_cell2[0].attrib.get('href'))
    #print csv_link
    scrape_doc(csv_link)
    
        

def scrape_page(link):
    html2 = scraperwiki.scrape(link)
    root2 = lxml.html.fromstring(html2)
    cellLink = root2.cssselect("div.attachment ul li")
    if cellLink:
        for cells in cellLink:
        
            table_cell2 = cells.cssselect('a')
            if table_cell2 !=[]:
                #print table_cell2
                table_scrape(table_cell2)

sotccweb = 'http://www.stoke.gov.uk'
html = scraperwiki.scrape('http://www.stoke.gov.uk/ccm/navigation/council-and-democracy/finance/transparency/')
root = lxml.html.fromstring(html)        
info = root.cssselect("li.expanded ul li.content")
#print info
for rows in info:   
    table_cell = rows.cssselect('a')
    if table_cell:
        link = urlparse.urljoin(sotccweb, table_cell[0].attrib.get('href'))
        #print link
        scrape_page(link)

