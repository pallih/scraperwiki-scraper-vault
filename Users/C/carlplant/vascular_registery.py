#Scraper based on numerous tutorials including Paul Bradshaw's excellent ebook Scraping
#for journalists

import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
from datetime import date 

url = 'http://www.vsqip.org.uk/wp/wp-content/uploads/2013/06/NVR-2013-Report-on-Surgical-Outcomes-Consultant-Level-Statistics.pdf'
     
pdfdata = urllib2.urlopen(url).read() 
xmldata = scraperwiki.pdftoxml(pdfdata) 
print xmldata
root = lxml.etree.fromstring(xmldata)

pages = list(root) 




for page in pages[11:31]:

    lines = page.findall('.//text')
    #print lines


    record = {}

    for textchunk in lines:

        leftcoord = int(textchunk.attrib.get('left'))

        if leftcoord == 116: 
            
            if textchunk.text:
                        
                record['surgeon'] = textchunk.text.strip()

        if leftcoord == 63: 
            
            if textchunk.text:
                        
                record['trust'] = textchunk.text.strip()

        if leftcoord == 748: 
            
            if textchunk.text:
                mort = textchunk.text.strip()
                mortality = re.split('\%',mort)
            
                        
                record['mortality_percentage'] = mortality[0]
           

        if leftcoord == 457: 
            
                if textchunk.text:
                        
                    record['GMC_reg'] = textchunk.text.strip()

        if leftcoord == 551: 
            
                if textchunk.text:
                        
                    record['AAA'] = textchunk.text.strip()

        if leftcoord == 615: 
            
                if textchunk.text:
                            
                    record['open'] = textchunk.text.strip()

        if leftcoord == 679: 
            
                if textchunk.text:
                        
                    record['EVAR'] = textchunk.text.strip()
                
    
                    record['ScrapeDate'] = date.today()  

    print record
    scraperwiki.sqlite.save(unique_keys=[],data=record)
        