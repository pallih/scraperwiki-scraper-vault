import scraperwiki
import re
import lxml.html

'''
Scrape country summary table out of main webpage

Creates a dictionary from country name to country's data

Sara-Jayne Farmer
2012
'''
def scrapeSummary():

    borders = {}
    url = "http://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_and_maritime_borders"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    #Get every tr in the data table
    #The table class is "wikitable sortable jquery-tablesorter" but haven't
    #been able to grab this with cssselect, which doesn't like the spaces
    #So have grabbed one of the divs outside it instead, and assume that the
    #data is in the first table in this div.
    tables = root.cssselect('div.mw-content-ltr table')
    trs = tables[0].cssselect('tr')

    #Get table contents
    #Start from 1 so we don't include table headings in the data outputs
    for row in range(1,len(trs)):
        
        #Ignore spacers between data rows
        if len(trs[row]) == 1:
            print("Ignored row")
            continue
        
        #Process country name and create a table key that won't crash the sqlite save
        formattag = trs[row][0][0].tag
        if formattag == "i":
            #Territories are in italics. 
            CorT = "territory"        
            countrycell = trs[row][0][0].cssselect('b')[0][1]
        elif formattag == "b":
            #Countries are in bold. Except some territories have italics inside bold :-(
            if trs[row][0][0].cssselect('b')[0][0].tag == 'i':
                CorT = "territory"
                countrycell = trs[row][0][0].cssselect('b')[0][0][1]            
            else:
                CorT = "country"
                countrycell = trs[row][0][0].cssselect('b')[0][1]
        else:
            #We're not interested in any other format types
            continue
        
        #Countryname is in <a> inside <b> for both countries and territories.
        #Don't just look for <a> in the <td> because some of the map icons have <a>s.
        country = countrycell.text.strip().encode('utf8')
        print("Country: " + country)
        
        countrykey = re.sub(r'[^a-zA-Z0-9 ]','', country)
        borders[countrykey] = {}
        borders[countrykey]['key'] = countrykey
        borders[countrykey]['Country or Territory name'] = country
        borders[countrykey]['Country or Territory'] = CorT
        
        #Process number of neighbours, both recognised and unrecognised
        #Expect to see recognised followed by unrecognised in brackets
        fstr = "(.+?)\((.+?)\)"
        countcell = trs[row][3].text
        tots = re.findall(fstr, countcell)
        if len(tots) < 2:
            recnum  = countcell.strip()
            unrecnum = recnum
        else:
            recnum   = tots[0][0].strip()
            unrecnum = tots[0][1].strip()
        borders[countrykey]["Total Recognised Neighbours"] = recnum
        borders[countrykey]["Total Inc Unrecognised Neighbours"] = unrecnum
        
        #Process list of neighbours
        neighs = ""
        neighcell = trs[row][4]
        neighas = neighcell.cssselect('a')
        for i in range(len(neighas)):
            neighs += neighas[i].text.strip().encode('utf8') + ","
        borders[countrykey]['Neighbours'] = neighs
        
    #Save results to the scraperwiki summary table
    #All neighbours, land neighbours, maritime neighbours
    #scraperwiki.sqlite.save(unique_keys=['key'], table_name='summary', data=borders[countrykey])

    #Another table? Key=countries; Country1 Country2 Bordertype Recognised
                    
    return(borders)

#Main code
borders = scrapeSummary()

import scraperwiki
import re
import lxml.html

'''
Scrape country summary table out of main webpage

Creates a dictionary from country name to country's data

Sara-Jayne Farmer
2012
'''
def scrapeSummary():

    borders = {}
    url = "http://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_and_maritime_borders"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    #Get every tr in the data table
    #The table class is "wikitable sortable jquery-tablesorter" but haven't
    #been able to grab this with cssselect, which doesn't like the spaces
    #So have grabbed one of the divs outside it instead, and assume that the
    #data is in the first table in this div.
    tables = root.cssselect('div.mw-content-ltr table')
    trs = tables[0].cssselect('tr')

    #Get table contents
    #Start from 1 so we don't include table headings in the data outputs
    for row in range(1,len(trs)):
        
        #Ignore spacers between data rows
        if len(trs[row]) == 1:
            print("Ignored row")
            continue
        
        #Process country name and create a table key that won't crash the sqlite save
        formattag = trs[row][0][0].tag
        if formattag == "i":
            #Territories are in italics. 
            CorT = "territory"        
            countrycell = trs[row][0][0].cssselect('b')[0][1]
        elif formattag == "b":
            #Countries are in bold. Except some territories have italics inside bold :-(
            if trs[row][0][0].cssselect('b')[0][0].tag == 'i':
                CorT = "territory"
                countrycell = trs[row][0][0].cssselect('b')[0][0][1]            
            else:
                CorT = "country"
                countrycell = trs[row][0][0].cssselect('b')[0][1]
        else:
            #We're not interested in any other format types
            continue
        
        #Countryname is in <a> inside <b> for both countries and territories.
        #Don't just look for <a> in the <td> because some of the map icons have <a>s.
        country = countrycell.text.strip().encode('utf8')
        print("Country: " + country)
        
        countrykey = re.sub(r'[^a-zA-Z0-9 ]','', country)
        borders[countrykey] = {}
        borders[countrykey]['key'] = countrykey
        borders[countrykey]['Country or Territory name'] = country
        borders[countrykey]['Country or Territory'] = CorT
        
        #Process number of neighbours, both recognised and unrecognised
        #Expect to see recognised followed by unrecognised in brackets
        fstr = "(.+?)\((.+?)\)"
        countcell = trs[row][3].text
        tots = re.findall(fstr, countcell)
        if len(tots) < 2:
            recnum  = countcell.strip()
            unrecnum = recnum
        else:
            recnum   = tots[0][0].strip()
            unrecnum = tots[0][1].strip()
        borders[countrykey]["Total Recognised Neighbours"] = recnum
        borders[countrykey]["Total Inc Unrecognised Neighbours"] = unrecnum
        
        #Process list of neighbours
        neighs = ""
        neighcell = trs[row][4]
        neighas = neighcell.cssselect('a')
        for i in range(len(neighas)):
            neighs += neighas[i].text.strip().encode('utf8') + ","
        borders[countrykey]['Neighbours'] = neighs
        
    #Save results to the scraperwiki summary table
    #All neighbours, land neighbours, maritime neighbours
    #scraperwiki.sqlite.save(unique_keys=['key'], table_name='summary', data=borders[countrykey])

    #Another table? Key=countries; Country1 Country2 Bordertype Recognised
                    
    return(borders)

#Main code
borders = scrapeSummary()

