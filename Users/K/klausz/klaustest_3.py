# Idea/Solution taken from Mjumbe Poe / Boston Eating Establishment Temporary Permit Suspensions
# from @andymboyle - Andy Boyle / Pythoninquiries

# Actually its working.
# Possible improvements:
# - scrape all years (different link on top)
# - check if code can be improved


###############################################################################
# 
# Website: 
# Fields:
#
#    Netzbetreiber = ''
#    Anlagenschluessel = ''
#    Energietraeger = ''
#    Ort = ''
#    Plz = ''
#    StrasseFlst = ''
#    Bundesland = ''
#    InstallierteLeistung = ''
#    KWKAnteil = ''
#    Technologie = ''
#    Inbetriebnahmejahr = ''
#    EinspeiseSpannungsebene = ''
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup



base_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-60C46786-AB1F4138/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage='
# q = 'to:andymboyle+python'
# q = 'to:klausz'
options = '&spannungsebene.id='
while 1:
    try:
        page = scraperwiki.sqlite.get_var("page", 1)
        starting_url = base_url + str(page) + options 


# starting_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-0BE7D766-343024DD/apc_nextgen_inter_trm-prod/http://miniapp-
# internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-
#INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage=2&spannungsebene.id='

        html = scraperwiki.scrape(starting_url)# thats the selection

        soup = BeautifulSoup(html)

        for ldiv in  soup.findAll('table'):
            if ldiv.find('th').text == 'Netzbetreiber':
                div = ldiv

# This Block not changed - should either be corrected or be removed
# Begin

        susp_rows = div.findAll('tr') #the 'bracket around each line'

        def absolutize_url(url): #it seems these are the empty line, tbchanged later
            if url[0] == '/':
                url = 'http://www.cityofboston.gov' + url#what is going on here?
            elif url[:4] != 'http':
                url = 'http://www.cityofboston.gov/isd/health/' + url    
            return url
# End

        recordlist = [ ]
        for susp_row in susp_rows[2:]:## where did this come from? Why?

            Netzbetreiber = ''
            Anlagenschluessel = ''
            Energietraeger = ''
            Ort = ''
            Plz = ''
            StrasseFlst = ''
            Bundesland = ''
            InstallierteLeistung = ''
            KWKAnteil = ''
            Technologie = ''
            Inbetriebnahmejahr = ''
            EinspeiseSpannungsebene = ''

            cells = susp_row.findAll('td')

#    print susp_row # this helped to see what was coming from the scraper -> then correction start from Line 2 instead of Line 1.
    
#Seems to be used when there is content in Line


            def tonum(ss):
                return float(ss.text.strip().replace(".", "").replace(",", "."))


            Netzbetreiber = cells[0].text
            Anlagenschluessel = cells[1].text
            Energietraeger = cells[2].text
            Ort = cells[3].text
            Plz = cells[4].text
            StrasseFlst = cells[5].text
            Bundesland = cells[6].text
            InstallierteLeistung = tonum(cells[7])
            KWKAnteil = cells[8].text
            Technologie = cells[9].text
            Inbetriebnahmejahr = cells[10].text
            EinspeiseSpannungsebene = cells[11].text


# Is this necessary ? Why. Possibly when there are empty lines. It has not been changed.
# Begin
            susp_a = cells[2].find('a')
            if susp_a:
                susp_url = absolutize_url(susp_a['href'])
    
            reinst_a = cells[3].find('a')
            if reinst_a:
                reinst_url = absolutize_url(reinst_a['href'])
# End
    

#Seems to be used when there is content in the line
# It seems to be necessary to define every column in the table, otherwise its not working
            record = {

                'Netzbetreiber' : Netzbetreiber
                ,'Anlagenschluessel': Anlagenschluessel
                ,'Energietraeger' : Energietraeger
                ,'Ort' : Ort
                ,'Plz' : Plz
                ,'StrasseFlst' : StrasseFlst
                ,'Bundesland' : Bundesland
                ,'InstallierteLeistung' : InstallierteLeistung
                ,'KWKAnteil' : KWKAnteil
                ,'Technologie' : Technologie
                ,'Inbetriebnahmejahr' : Inbetriebnahmejahr
                ,'EinspeiseSpannungsebene' : EinspeiseSpannungsebene

            }
    
            recordlist.append(record)
        scraperwiki.sqlite.save(['Anlagenschluessel'], recordlist) #1st Table

        scraperwiki.sqlite.save_var("page", page+1) #2nd Table

    except Exception, e:
        print e
# Idea/Solution taken from Mjumbe Poe / Boston Eating Establishment Temporary Permit Suspensions
# from @andymboyle - Andy Boyle / Pythoninquiries

# Actually its working.
# Possible improvements:
# - scrape all years (different link on top)
# - check if code can be improved


###############################################################################
# 
# Website: 
# Fields:
#
#    Netzbetreiber = ''
#    Anlagenschluessel = ''
#    Energietraeger = ''
#    Ort = ''
#    Plz = ''
#    StrasseFlst = ''
#    Bundesland = ''
#    InstallierteLeistung = ''
#    KWKAnteil = ''
#    Technologie = ''
#    Inbetriebnahmejahr = ''
#    EinspeiseSpannungsebene = ''
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup



base_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-60C46786-AB1F4138/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage='
# q = 'to:andymboyle+python'
# q = 'to:klausz'
options = '&spannungsebene.id='
while 1:
    try:
        page = scraperwiki.sqlite.get_var("page", 1)
        starting_url = base_url + str(page) + options 


# starting_url = 'http://www.50hertz-transmission.net/cps/rde/papp/SID-0BE7D766-343024DD/apc_nextgen_inter_trm-prod/http://miniapp-
# internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-
#INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=&bundesland.id=&pagingDescriptor.currentPage=2&spannungsebene.id='

        html = scraperwiki.scrape(starting_url)# thats the selection

        soup = BeautifulSoup(html)

        for ldiv in  soup.findAll('table'):
            if ldiv.find('th').text == 'Netzbetreiber':
                div = ldiv

# This Block not changed - should either be corrected or be removed
# Begin

        susp_rows = div.findAll('tr') #the 'bracket around each line'

        def absolutize_url(url): #it seems these are the empty line, tbchanged later
            if url[0] == '/':
                url = 'http://www.cityofboston.gov' + url#what is going on here?
            elif url[:4] != 'http':
                url = 'http://www.cityofboston.gov/isd/health/' + url    
            return url
# End

        recordlist = [ ]
        for susp_row in susp_rows[2:]:## where did this come from? Why?

            Netzbetreiber = ''
            Anlagenschluessel = ''
            Energietraeger = ''
            Ort = ''
            Plz = ''
            StrasseFlst = ''
            Bundesland = ''
            InstallierteLeistung = ''
            KWKAnteil = ''
            Technologie = ''
            Inbetriebnahmejahr = ''
            EinspeiseSpannungsebene = ''

            cells = susp_row.findAll('td')

#    print susp_row # this helped to see what was coming from the scraper -> then correction start from Line 2 instead of Line 1.
    
#Seems to be used when there is content in Line


            def tonum(ss):
                return float(ss.text.strip().replace(".", "").replace(",", "."))


            Netzbetreiber = cells[0].text
            Anlagenschluessel = cells[1].text
            Energietraeger = cells[2].text
            Ort = cells[3].text
            Plz = cells[4].text
            StrasseFlst = cells[5].text
            Bundesland = cells[6].text
            InstallierteLeistung = tonum(cells[7])
            KWKAnteil = cells[8].text
            Technologie = cells[9].text
            Inbetriebnahmejahr = cells[10].text
            EinspeiseSpannungsebene = cells[11].text


# Is this necessary ? Why. Possibly when there are empty lines. It has not been changed.
# Begin
            susp_a = cells[2].find('a')
            if susp_a:
                susp_url = absolutize_url(susp_a['href'])
    
            reinst_a = cells[3].find('a')
            if reinst_a:
                reinst_url = absolutize_url(reinst_a['href'])
# End
    

#Seems to be used when there is content in the line
# It seems to be necessary to define every column in the table, otherwise its not working
            record = {

                'Netzbetreiber' : Netzbetreiber
                ,'Anlagenschluessel': Anlagenschluessel
                ,'Energietraeger' : Energietraeger
                ,'Ort' : Ort
                ,'Plz' : Plz
                ,'StrasseFlst' : StrasseFlst
                ,'Bundesland' : Bundesland
                ,'InstallierteLeistung' : InstallierteLeistung
                ,'KWKAnteil' : KWKAnteil
                ,'Technologie' : Technologie
                ,'Inbetriebnahmejahr' : Inbetriebnahmejahr
                ,'EinspeiseSpannungsebene' : EinspeiseSpannungsebene

            }
    
            recordlist.append(record)
        scraperwiki.sqlite.save(['Anlagenschluessel'], recordlist) #1st Table

        scraperwiki.sqlite.save_var("page", page+1) #2nd Table

    except Exception, e:
        print e
