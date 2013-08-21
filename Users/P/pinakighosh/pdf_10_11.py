import scraperwiki
import urllib2
import lxml.etree
import bs4

url = "http://dget.nic.in/ItiUpgradePPP/list%20of%20%20ITIs%20only%20wth%20industry%20partners10-11.pdf"
pdfdata = urllib2.urlopen(url).read()
#print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
#print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
print xmldata
soup=bs4.BeautifulSoup(xmldata)
#print soup
start=False
ITI=True
sl_no=0
for link in soup.find_all('text'):
    #print link.textcontent()
    #print link.get_text()
    #print str(start)
    text=link.get_text()
    text=text.replace(',',' ')
    if start:
        if len(text)>4 or text.count('NIL')>0:
            #print text
            #if text.count('(ITI-')>0:
                #continue
            if ITI:
                sl_no+=1
                name=text
                ITI=False
            else:
                ind_par=text
                ITI=True
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
            
            #print text 
    if text.find('-02')>0:
        start=True

