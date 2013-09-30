# Scraper of early day motion data from current parliamentary session
#http://www.parliament.uk/edm/2010-12/by-topic

import scraperwiki
import string,lxml.html

def parseEDMpage(edm_id,subject):
    url='http://www.parliament.uk'+edm_id
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    #get EDM name
    edm_name=page.find('.//h2').text
    print edm_name
    #get EDM description
    edm_desc=page.find('.//div[@class="details"]')[2].text
    print edm_desc
    el=page.find('.//ul[@class="summary"]')
    #get EDM Session
    edm_session=el[0][1].text
    print "session:",edm_session
    #get EDM Date tabled
    edm_dateTabled=el[1][1].text
    print "dateTabled:",edm_dateTabled
    #get EDM Primary sponsor
    edm_primarySponsor=el[2][1][0].text
    edm_primarySponsorID=el[2][1][0].get('href')
    print "primarySponsor:",edm_primarySponsor,'primarySponsorID:',edm_primarySponsorID
    scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':edm_primarySponsorID,'mp_name':edm_primarySponsor,'sponsor_type':'primary','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':edm_dateTabled,'subject':subject,'party':'','constituency':''})

    scraperwiki.sqlite.save(unique_keys=['edm_id'], table_name='EDMSummary', data={ 'edm_id':edm_id, 'edm_name':edm_name,'edm_desc':edm_desc,'edm_date':edm_dateTabled,'subject':subject,'mp_id':edm_primarySponsorID,'mp_name':edm_primarySponsor,'edm_session':edm_session})

    #get EDM Sponsors
    for el in page.findall('.//ul[@class="value"]/li/a'):
        edm_sponsorName=el.text
        edm_sponsorID=el.get('href')
        print 'sponsorName:',edm_sponsorName,'sponsorID:',edm_sponsorID
        scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':edm_sponsorID,'mp_name':edm_sponsorName,'sponsor_type':'sponsor','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':edm_dateTabled,'subject':subject,'party':'','constituency':''})
    #get EDM signatories
    for el in page.findall('.//tbody/tr'):
        print 'SigName:',el[0][0].text,'SigName_ID',el[0][0].get('href'),'SigParty:',el[1].text,'SigConstituency:',el[2].text,'SigDate:',el[3].text
        scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':el[0][0].get('href'),'mp_name':el[0][0].text,'sponsor_type':'signatory','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':el[3].text,'subject':subject,'party':el[1].text,'constituency':el[2].text})
    #get EDM withdrawls

def getEDMsbySpecificSubjectPage(url,subject):
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for el in page.findall('.//tbody/tr'):
        edmStub=el[0][0].get('href')
        print edmStub,el[0][0].text
        scraperwiki.sqlite.save(unique_keys=['edm_id'], table_name='EDMbySubject', data={ 'edm_id':edmStub, 'edm_name':el[0][0].text,'subject':subject})
        parseEDMpage(edmStub,subject)

def getEDMsfromSubjectsPage():
    url='http://www.parliament.uk/edm/2010-12/by-topic'
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for el in page.findall('.//td[@scope="row"]/a'):
        edmSubjectStub=el.get('href')
        print edmSubjectStub
        getEDMsbySpecificSubjectPage('http://www.parliament.uk'+edmSubjectStub,el.text)

##tests
#getEDMsbySpecificSubjectPage('http://www.parliament.uk/edm/2010-12/by-topic/59141/adult-education','Adult education')
#parseEDMpage('http://www.parliament.uk/edm/2010-12/2325')

#scraperwiki.sqlite.execute('drop table "EDMsupporters"')
#scraperwiki.sqlite.execute('drop table "EDMbySubject"')
#scraperwiki.sqlite.execute('drop table "EDMSummary"')

getEDMsfromSubjectsPage()
# Scraper of early day motion data from current parliamentary session
#http://www.parliament.uk/edm/2010-12/by-topic

import scraperwiki
import string,lxml.html

def parseEDMpage(edm_id,subject):
    url='http://www.parliament.uk'+edm_id
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    #get EDM name
    edm_name=page.find('.//h2').text
    print edm_name
    #get EDM description
    edm_desc=page.find('.//div[@class="details"]')[2].text
    print edm_desc
    el=page.find('.//ul[@class="summary"]')
    #get EDM Session
    edm_session=el[0][1].text
    print "session:",edm_session
    #get EDM Date tabled
    edm_dateTabled=el[1][1].text
    print "dateTabled:",edm_dateTabled
    #get EDM Primary sponsor
    edm_primarySponsor=el[2][1][0].text
    edm_primarySponsorID=el[2][1][0].get('href')
    print "primarySponsor:",edm_primarySponsor,'primarySponsorID:',edm_primarySponsorID
    scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':edm_primarySponsorID,'mp_name':edm_primarySponsor,'sponsor_type':'primary','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':edm_dateTabled,'subject':subject,'party':'','constituency':''})

    scraperwiki.sqlite.save(unique_keys=['edm_id'], table_name='EDMSummary', data={ 'edm_id':edm_id, 'edm_name':edm_name,'edm_desc':edm_desc,'edm_date':edm_dateTabled,'subject':subject,'mp_id':edm_primarySponsorID,'mp_name':edm_primarySponsor,'edm_session':edm_session})

    #get EDM Sponsors
    for el in page.findall('.//ul[@class="value"]/li/a'):
        edm_sponsorName=el.text
        edm_sponsorID=el.get('href')
        print 'sponsorName:',edm_sponsorName,'sponsorID:',edm_sponsorID
        scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':edm_sponsorID,'mp_name':edm_sponsorName,'sponsor_type':'sponsor','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':edm_dateTabled,'subject':subject,'party':'','constituency':''})
    #get EDM signatories
    for el in page.findall('.//tbody/tr'):
        print 'SigName:',el[0][0].text,'SigName_ID',el[0][0].get('href'),'SigParty:',el[1].text,'SigConstituency:',el[2].text,'SigDate:',el[3].text
        scraperwiki.sqlite.save(unique_keys=[], table_name='EDMsupporters', data={ 'mp_id':el[0][0].get('href'),'mp_name':el[0][0].text,'sponsor_type':'signatory','edm_id':edm_id,'edm_name':edm_name,'edm_session':edm_session,'edm_date':el[3].text,'subject':subject,'party':el[1].text,'constituency':el[2].text})
    #get EDM withdrawls

def getEDMsbySpecificSubjectPage(url,subject):
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for el in page.findall('.//tbody/tr'):
        edmStub=el[0][0].get('href')
        print edmStub,el[0][0].text
        scraperwiki.sqlite.save(unique_keys=['edm_id'], table_name='EDMbySubject', data={ 'edm_id':edmStub, 'edm_name':el[0][0].text,'subject':subject})
        parseEDMpage(edmStub,subject)

def getEDMsfromSubjectsPage():
    url='http://www.parliament.uk/edm/2010-12/by-topic'
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    for el in page.findall('.//td[@scope="row"]/a'):
        edmSubjectStub=el.get('href')
        print edmSubjectStub
        getEDMsbySpecificSubjectPage('http://www.parliament.uk'+edmSubjectStub,el.text)

##tests
#getEDMsbySpecificSubjectPage('http://www.parliament.uk/edm/2010-12/by-topic/59141/adult-education','Adult education')
#parseEDMpage('http://www.parliament.uk/edm/2010-12/2325')

#scraperwiki.sqlite.execute('drop table "EDMsupporters"')
#scraperwiki.sqlite.execute('drop table "EDMbySubject"')
#scraperwiki.sqlite.execute('drop table "EDMSummary"')

getEDMsfromSubjectsPage()
