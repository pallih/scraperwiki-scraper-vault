#Scraper based on numerous tutorials including Paul Bradshaw's excellent ebook Scraping
#for journalists

import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
from datetime import date 



html = scraperwiki.scrape('http://www.stoke.gov.uk/ccm/content/business/general/procurement/current-tender-and-quotation-opportunities.en/')
base_url ='http://www.stoke.gov.uk'


root2 = lxml.html.fromstring(html) # turn our HTML into an lxml object

for link in root2.cssselect("li.attachment-link a"):
    ext_link = link.attrib['href']
    #print ext_link
    url = base_url+ext_link     
     

#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
pdfdata = urllib2.urlopen(url).read()
#use pdftoxml to convert that into an xml document
pdfread = scraperwiki.pdftoxml(pdfdata)
print pdfread
#use lxml.etree to convert that into an lxml object
pdfroot = lxml.etree.fromstring(pdfread)
#find all <text> tags and put in list variable 'lines'
lines = pdfroot.findall('.//text')
#print lines

record = {}

for textchunk in lines:

    leftcoord = int(textchunk.attrib.get('left'))

    if leftcoord>47 and leftcoord<49: 
            
        if textchunk.text:
                        
            record['detail'] = textchunk.text.strip()
            #print detail 

    if leftcoord>159 and leftcoord<166: 
            
        if textchunk.text:
                        
            record['code'] = textchunk.text.strip()
            #print code 

    if leftcoord>747 and leftcoord<750: 
            
            if textchunk.text:
                        
                record['sme'] = textchunk.text.strip()
                #print sme 

    if leftcoord>865 and leftcoord<894: 
            
            if textchunk.text:
                        
                record['ExpiryDate'] = textchunk.text.strip()
                #print date 
                record['ScrapeDate'] = date.today()  

    #print record
            scraperwiki.sqlite.save(unique_keys=[],data=record)
        
        

                
                
                


        
    