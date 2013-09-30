import scraperwiki
import lxml.html
lazycache=scraperwiki.swimport('lazycache')

#url='http://www.mod.uk/DefenceInternet/AboutDefence/CorporatePublications/ConsultationsandCommunications/PublicConsultations/GpssConsultation.htm'
url='http://www.mod.uk/DefenceInternet/DefenceNews/DefencePolicyAndBusiness/FreeTravelForMilitaryPersonnelSupportingSecurityForThe2012Games.htm'
html=lazycache.lazycache(url)
root=lxml.html.fromstring(html)
root.make_links_absolute(url)
print html

def parsenews(root):
    data={}
    divs= root.xpath("//div[@id='left-column']/div[not(@class)]/p[1]/..")
    for x in divs:
        print x.attrib, lxml.html.tostring(x),'*'

parsenews(root)


def parseconsult(root):
    data={}
    data['title']=root.cssselect('h1')[0].text
    #data['body']=lxml.html.tostring(root.xpath("//div[@class='consultationcontent'][2]")[0])
    data['ref'] = root.xpath("//div[@property='dc:identifier']/text()")[0]
    data['assoc_org']='MoD'
    
    data['attachments']=[]
    for attachment in root.xpath("//a[@rel='DC:haspart']"):
        url=attachment.attrib['href']
        name=attachment.text
        data['attachments'].append([name, url])
    
    data['person']=root.xpath("//span[@property='v:fn']/text()")[0]
    data['address']='\n'.join((root.xpath("//span[@property='v:adr']/text()")[0].strip(),
                               root.xpath("//span[@property='v:street-address']/text()")[0].strip(),
                               root.xpath("//span[@property='v:locality']/text()")[0].strip(),
                               root.xpath("//span[@property='v:postal-code']/text()")[0].strip()))
    data['email']=root.xpath("//span[@property='argot:replyByEmail v:email']/a/@href")[0].replace('mailto:','').strip()
    #data['fax']=root.xpath("//span[@property='v:fax']/text()")[0] # TODO: implement properly
        
    profilecontent={'Open Date':'open_date', 'Close Date':'close_date'}
    datexml=root.xpath("//div[@class='profilecontent']/div[@class='profilecontent']")
    for i in datexml:
        matchtext=i.xpath("strong/text()")[0]
        datetext=i.xpath("text()")[0]
        for content in profilecontent:
            if content in matchtext:
                data[profilecontent[content]]=datetext # TODO: parse date ;
                break
        else:
            print "profilecontent not found: '%s'"%matchtext
    
    
    
    print dataimport scraperwiki
import lxml.html
lazycache=scraperwiki.swimport('lazycache')

#url='http://www.mod.uk/DefenceInternet/AboutDefence/CorporatePublications/ConsultationsandCommunications/PublicConsultations/GpssConsultation.htm'
url='http://www.mod.uk/DefenceInternet/DefenceNews/DefencePolicyAndBusiness/FreeTravelForMilitaryPersonnelSupportingSecurityForThe2012Games.htm'
html=lazycache.lazycache(url)
root=lxml.html.fromstring(html)
root.make_links_absolute(url)
print html

def parsenews(root):
    data={}
    divs= root.xpath("//div[@id='left-column']/div[not(@class)]/p[1]/..")
    for x in divs:
        print x.attrib, lxml.html.tostring(x),'*'

parsenews(root)


def parseconsult(root):
    data={}
    data['title']=root.cssselect('h1')[0].text
    #data['body']=lxml.html.tostring(root.xpath("//div[@class='consultationcontent'][2]")[0])
    data['ref'] = root.xpath("//div[@property='dc:identifier']/text()")[0]
    data['assoc_org']='MoD'
    
    data['attachments']=[]
    for attachment in root.xpath("//a[@rel='DC:haspart']"):
        url=attachment.attrib['href']
        name=attachment.text
        data['attachments'].append([name, url])
    
    data['person']=root.xpath("//span[@property='v:fn']/text()")[0]
    data['address']='\n'.join((root.xpath("//span[@property='v:adr']/text()")[0].strip(),
                               root.xpath("//span[@property='v:street-address']/text()")[0].strip(),
                               root.xpath("//span[@property='v:locality']/text()")[0].strip(),
                               root.xpath("//span[@property='v:postal-code']/text()")[0].strip()))
    data['email']=root.xpath("//span[@property='argot:replyByEmail v:email']/a/@href")[0].replace('mailto:','').strip()
    #data['fax']=root.xpath("//span[@property='v:fax']/text()")[0] # TODO: implement properly
        
    profilecontent={'Open Date':'open_date', 'Close Date':'close_date'}
    datexml=root.xpath("//div[@class='profilecontent']/div[@class='profilecontent']")
    for i in datexml:
        matchtext=i.xpath("strong/text()")[0]
        datetext=i.xpath("text()")[0]
        for content in profilecontent:
            if content in matchtext:
                data[profilecontent[content]]=datetext # TODO: parse date ;
                break
        else:
            print "profilecontent not found: '%s'"%matchtext
    
    
    
    print data