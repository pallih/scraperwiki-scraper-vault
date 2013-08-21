import scraperwiki

# Blank Python
import scraperwiki
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

import re



TotalLawyers =[]

for i in range(46)[1:]:
    strAddr = "http://codingtrying.herobo.com/"+str(i)+".html"
    html = urllib.urlopen(strAddr)
    html = html.read()
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)

    mainContent = tree.xpath("//table[@id='tabdata_Professionals']")[0]
    nodes = tree.xpath("//tr[@class='show_bio_short']")
    
    for node in nodes:
        Total ={}
        contentHTML= (etree.tostring(node, pretty_print=True))
        tree   = etree.parse(StringIO(contentHTML), parser)
        givenName = tree.xpath("//div[@class='atty_name']/descendant::*/text()")
        if givenName != []:
            Total["name"]= givenName[0].strip()
        else:
            break

        Total['link'] = tree.xpath("//div[@class='atty_name']/a/@href")[0].strip()
        Total['location'] = tree.xpath("//div[@class='atty_office']/a/text()")[0].strip()
        
        myEmail =  tree.xpath("//div[@class='atty_email']/a/@href")[0].strip()
        Emails= myEmail.split(',')
        for eachMail in Emails:
            foundmail = re.findall("'.*<at>bakermckenzie.com'",eachMail)
            if foundmail!=[]:
                foundmail=foundmail[0].replace("'","").replace("<at>","@")
                break
        Total['email']=foundmail

        Total['title'] = tree.xpath("//div[@class='atty_title']/text()")[0].strip()
        phone =tree.xpath("//div[@class='atty_phone']/text()")
        Total['phone']=""
        if phone!=[]:
            Total['phone'] = phone[0].strip()
        print Total
        TotalLawyers.append(Total)

i=0
for lawyer in TotalLawyers:
    url = lawyer['link']
    html = urllib.urlopen(url)
    html = html.read()
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//h4[text()='Education']/following-sibling::*[1]/text()")
    education=[]
    for eachItem in mainContent:
         eachItem = eachItem.replace("  ","")
         eachItem= eachItem.strip()
         eachItem = eachItem.replace("\r\n"," ")
         eachItem = eachItem.replace("\\xa0"," ")

         print eachItem
         education.append(eachItem)
    lawyer['education']= ' ; '.join(education)
    print lawyer
    
    lawyer["i"]=str(i)
    scraperwiki.sqlite.save(unique_keys=["i"], data=lawyer)
    i=i+1
    





'''
#print mainContent

contentHTML= (etree.tostring(mainContent, pretty_print=True))

#print contentHTML
tree   = etree.parse(StringIO(contentHTML), parser)
lawyers = tree.xpath("//tbody/tr")
#print eachLawyer


TotalList = []
for eachLawyer in lawyers:
    print eachLawyer
    Total = {}

    contentHTML= (etree.tostring(eachLawyer, pretty_print=True))
    tree   = etree.parse(StringIO(contentHTML), parser)
    #print contentHTML
    Total['name'] = tree.xpath("//td/a/text()")[0].strip()
    print Total['name']    
    Total['link'] = tree.xpath("//td/a/@href")[0].strip()
    Total['title'] = tree.xpath("//td[2]/text()")[0].strip()
    email = tree.xpath("//td[3]/a/text()")
    if email!=[]:
        Total['email']=email[0].strip()
    else:
        Total['email']=""

    Total['location'] = tree.xpath("//td[4]/table/tr/td[1]/a/text()")[0].strip()
    Total['telephone'] = tree.xpath("//td[4]/table/tr/td[2]/text()")[0].strip()
    
    #print Total
    TotalList.append(Total)

print TotalList
    
i = 0
for total in TotalList:
    url = "http://www.lw.com" +total['link']
    #print url
    html = urllib.urlopen(url)
    html = html.read()

    #print html
    educationList = []
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//ul[@id='AttorneyMetaData']/li/ul[2]/descendant-or-self::*/text()")
    for eachEdu in mainContent:
        eachEdu = eachEdu.strip()
        #print eachEdu
        educationList.append(eachEdu)
    total["i"]=str(i)       
    total['education'] =  ':'.join(educationList)
    print total
    scraperwiki.sqlite.save(unique_keys=["i"], data=total)
    i=i+1
'''