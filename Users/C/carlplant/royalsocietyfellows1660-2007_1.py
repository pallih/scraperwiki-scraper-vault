import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser
import datetime

Now = datetime.datetime.now()



#Read the pdf from the url given and prints the total length bytes of the pdf 
url = "http://www.stoke.gov.uk/ccm/cms-service/download/asset/?asset_id=405843"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#Convert the pdf data into xml and prints the total length bytes of the xml
xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata
print "After converting to xml it has %d bytes" % len(xmldata)


root = lxml.etree.fromstring(xmldata)
pages = list(root)
#UnknownID=1
ResumeAtPage = 2
print pages

for page in pages:
    pagenumber=int(page.attrib.get("number"))
    if pagenumber < ResumeAtPage:
        #print "Skipping page %d, before ResumeAtPage" % pagenumber
        continue 
    #if pagenumber>400 and pagenumber<500:
        #print "Skipping page %d because it is frontmatter:" % pagenumber
        #continue

for textchunk in (page.xpath('text')):
    leftcoord = int(textchunk.attrib.get('left'))
    
    
    if leftcoord>45 and leftcoord<58: #not all lines have the same left= coordinates
            
        if textchunk.text:
                
            detail = textchunk.text.strip()
            print detail

    if leftcoord>1330 and leftcoord<1406: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            date = textchunk.text.strip()
            #print date 
 
    if leftcoord>222 and leftcoord<254: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            code = textchunk.text.strip()
            #print code 
    if leftcoord>1130 and leftcoord<1140: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            suitable_sme = textchunk.text.strip()
            print suitable_sme 
 
            scraperwiki.sqlite.save(unique_keys=[],data={'Scrape_date' : Now, 'detail': detail, 'end_date':date,'contract_ref':code, 'suitable_sme':suitable_sme, 'URL' : url})
        
        
                 
                
                #Unexpected={"ID":UnknownID,"Text":textchunk.text,"Page":page.attrib.get("number"),"left":leftcoord}
            
                #UnknownID=UnknownID+1 


        import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser
import datetime

Now = datetime.datetime.now()



#Read the pdf from the url given and prints the total length bytes of the pdf 
url = "http://www.stoke.gov.uk/ccm/cms-service/download/asset/?asset_id=405843"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#Convert the pdf data into xml and prints the total length bytes of the xml
xmldata = scraperwiki.pdftoxml(pdfdata)
print xmldata
print "After converting to xml it has %d bytes" % len(xmldata)


root = lxml.etree.fromstring(xmldata)
pages = list(root)
#UnknownID=1
ResumeAtPage = 2
print pages

for page in pages:
    pagenumber=int(page.attrib.get("number"))
    if pagenumber < ResumeAtPage:
        #print "Skipping page %d, before ResumeAtPage" % pagenumber
        continue 
    #if pagenumber>400 and pagenumber<500:
        #print "Skipping page %d because it is frontmatter:" % pagenumber
        #continue

for textchunk in (page.xpath('text')):
    leftcoord = int(textchunk.attrib.get('left'))
    
    
    if leftcoord>45 and leftcoord<58: #not all lines have the same left= coordinates
            
        if textchunk.text:
                
            detail = textchunk.text.strip()
            print detail

    if leftcoord>1330 and leftcoord<1406: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            date = textchunk.text.strip()
            #print date 
 
    if leftcoord>222 and leftcoord<254: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            code = textchunk.text.strip()
            #print code 
    if leftcoord>1130 and leftcoord<1140: #not all lines have the same left= coordinates
            
        if textchunk.text:
                        
            suitable_sme = textchunk.text.strip()
            print suitable_sme 
 
            scraperwiki.sqlite.save(unique_keys=[],data={'Scrape_date' : Now, 'detail': detail, 'end_date':date,'contract_ref':code, 'suitable_sme':suitable_sme, 'URL' : url})
        
        
                 
                
                #Unexpected={"ID":UnknownID,"Text":textchunk.text,"Page":page.attrib.get("number"),"left":leftcoord}
            
                #UnknownID=UnknownID+1 


        