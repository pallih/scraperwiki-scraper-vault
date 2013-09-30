# from @andymboyle - Andy Boyle / Pythoninquiries

import scraperwiki
import simplejson

# retrieve a page
#base_url = 'http://search.twitter.com/search.json?q='
#q = '%3A('
#options = '&rpp=100&page='
#page = 1


base_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-60C46786-AB1F4138/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage='
# q = 'to:andymboyle+python'
# q = 'to:klausz'
options = '&spannungsebene.id='
page = 1


while 1:
    try:
        url = base_url + str(page) + options 
        html = scraperwiki.scrape(url)
        print html

        soup = BeautifulSoup(html)

        for ldiv in  soup.findAll('table'):
        if ldiv.find('th').text == 'Netzbetreiber':
            div = ldiv

        cells = susp_row.findAll('td')


        soup = simplejson.loads(html)
        for result in soup['Einzelwerte']:
            data = {}



        print susp_row # this helped to see what was coming from the scraper -> then correction start from Line 2 instead of Line 1.
    
#Seems to be used when there is content in Line

#    Netzbetreiber = cells[0].text
#    Anlagenschluessel = cells[1].text
#    Energietraeger = cells[2].text
#    Ort = cells[3].text
#    Plz = cells[4].text
#    StrasseFlst = cells[5].text
#    Bundesland = cells[6].text
#    InstallierteLeistung = cells[7].text
#    KWKAnteil = cells[8].text
#    Technologie = cells[9].text
#    Inbetriebnahmejahr = cells[10].text
#    EinspeiseSpannungsebene = cells[11].text



            # save records to the datastore
#            scraperwiki.datastore.save(["id"], data)
        page = page + 1
    except:
        print str


# from @andymboyle - Andy Boyle / Pythoninquiries

import scraperwiki
import simplejson

# retrieve a page
#base_url = 'http://search.twitter.com/search.json?q='
#q = '%3A('
#options = '&rpp=100&page='
#page = 1


base_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-60C46786-AB1F4138/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage='
# q = 'to:andymboyle+python'
# q = 'to:klausz'
options = '&spannungsebene.id='
page = 1


while 1:
    try:
        url = base_url + str(page) + options 
        html = scraperwiki.scrape(url)
        print html

        soup = BeautifulSoup(html)

        for ldiv in  soup.findAll('table'):
        if ldiv.find('th').text == 'Netzbetreiber':
            div = ldiv

        cells = susp_row.findAll('td')


        soup = simplejson.loads(html)
        for result in soup['Einzelwerte']:
            data = {}



        print susp_row # this helped to see what was coming from the scraper -> then correction start from Line 2 instead of Line 1.
    
#Seems to be used when there is content in Line

#    Netzbetreiber = cells[0].text
#    Anlagenschluessel = cells[1].text
#    Energietraeger = cells[2].text
#    Ort = cells[3].text
#    Plz = cells[4].text
#    StrasseFlst = cells[5].text
#    Bundesland = cells[6].text
#    InstallierteLeistung = cells[7].text
#    KWKAnteil = cells[8].text
#    Technologie = cells[9].text
#    Inbetriebnahmejahr = cells[10].text
#    EinspeiseSpannungsebene = cells[11].text



            # save records to the datastore
#            scraperwiki.datastore.save(["id"], data)
        page = page + 1
    except:
        print str


