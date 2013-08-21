import scraperwiki
import urllib2
import lxml.etree
import bs4

url = "http://dget.nic.in/ItiUpgradePPP/List%20of%20ITIs%20along%20with%20Industry%20Partners%20for%20the%20Scheme08-09.pdf"
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
exceptions_ind=['Hyderabad', 'Industry.', 'Guwahatis', 'Ltd.', 'Pvt.', 'Choolatheruvu', 'Industries.', 'Jabalpur', 'Barthi', 'Narsinghpur', 'Hoshangabad', 'Osmanabad.', 'Mumbai', 'Commerce.', 'Delhi.', 'Pur', 'Bhismram', 'Chamoli', 'Education.', 'Nagar']

exceptions_iti=['Areacode,Malappuram', 'Malvan', '(WBW)', 'Varanasi', 'Meerut', 'Gorakhpur']

def exc_ind(text):
    flag=False
    for i in exceptions_ind:
        if text.find(i)==0:
            return True
    return False

def exc_iti(text):
    flag=False
    for i in exceptions_iti:
        if text.find(i)==0:
            return True
    return False

for link in soup.find_all('text'):
    #print link.textcontent()
    #print link.get_text()
    #print str(start)
    text=link.get_text()
    text=text.replace(',',' ')
    if start:
        if len(text)>6 or text.count('NIL')>0:
            #print text
            #if text.count('(ITI-')>0:
                #continue
            if ITI:
                #if text.find('Hyderabad') == 0 or text.find('Industry.') == 0:
                if exc_ind(text):
                    print text
                    ind_par+=' '+text
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
                elif exc_iti(text):
                #elif text.find('Nagar') == 0 or text.find('Chowdhury') == 0:
                    print 'ITI  '+text
                    name+=' '+text
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
                    ITI=False
                else:
                    sl_no+=1
                    name=text
                    ITI=False
            else:
                #if text.find('Ltd.') == 0 or text.find('Development') == 0:
                if exc_ind(text):
                    print text
                    ind_par+=' '+text
                    sl_no-=1
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
                #elif text.find('Nagar') == 0 or text.find('Chowdhury') == 0:
                elif exc_iti(text):
                    print 'Else   '+text
                    #ITI=True
                    name+=' '+text
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
                else:
                    #print text
                    ind_par=text
                    #sl_no-=1
                    ITI=True
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"ITI":name,"Industry Partner":ind_par})
            
            #print text 
    if text.find('-36')>0:
        start=True
#for i in xmldata:
 #   print i
pages = list(root)

