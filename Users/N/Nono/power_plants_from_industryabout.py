import scraperwiki
import lxml.html
import sys
import re


#normalized forms for some countries
def createCountriesDict():
    countryLookup = dict()
    countryLookup['Catalonia'] = 'Spain'
    countryLookup['Euskalherria'] = 'Spain'
    countryLookup['Galiza'] = 'Spain'
    countryLookup['England'] = 'UK'
    countryLookup['Northern Ireland'] = 'UK'
    countryLookup['Scotland'] = 'UK'
    countryLookup['Wales'] = 'UK'
    countryLookup['Guadeloupe'] = 'France'
    countryLookup['Martinique'] = 'France'
    countryLookup['Reunion'] = 'France'
    countryLookup['Quebec'] = 'Canada'
    countryLookup['USA AB'] = 'USA'
    countryLookup['USA Fossil Fuels-East & South'] = 'USA'
    countryLookup['USA Fossil Fuels-West & Midwest'] = 'USA'
    countryLookup['USA FGH'] = 'USA'
    countryLookup['USA ILMNOPQ'] = 'USA'
    countryLookup['USA RSTUWXYZ'] = 'USA'
    countryLookup['India A-B'] = 'India'
    countryLookup['India C-F'] = 'India'
    countryLookup['India G-O'] = 'India'
    countryLookup['India P-Z'] = 'India'
    return countryLookup

def createPreferredTermsDict():
    preferredTermsLookup = dict()
    preferredTermsLookup['coal'] = 'fuel'
    preferredTermsLookup['kind_of_fuel'] = 'fuel'
    preferredTermsLookup['kind_of_coal'] = 'fuel'
    preferredTermsLookup['origin_of_coal'] = 'origin_of_fuel'
    preferredTermsLookup['web_1'] = 'web'
    preferredTermsLookup['web_3'] = ''
    preferredTermsLookup['wikipedia_1'] = 'wikipedia'
    preferredTermsLookup['wikipedia_2'] = 'wikipedia'
    preferredTermsLookup['wikipedia1'] = 'wikipedia'
    preferredTermsLookup['waikipedia'] = 'wikipedia'
    preferredTermsLookup['annual_capacity'] = 'power_capacity'
    preferredTermsLookup['annual_net_capacity'] = 'power_capacity'
    preferredTermsLookup['annual_net_power_capacity'] = 'power_capacity'
    preferredTermsLookup['capacity_installed'] = 'power_capacity'
    preferredTermsLookup['installed_net_power_capacity'] = 'power_capacity'
    preferredTermsLookup['installed_power_capacity'] = 'power_capacity'
    preferredTermsLookup['net_annual_capacity'] = 'power_capacity'
    preferredTermsLookup['net_annual_power_capacity'] = 'power_capacity'
    preferredTermsLookup['annual_installed_capacity'] = 'installed_capacity'
    preferredTermsLookup['storage_capacity'] = 'installed_capacity'
    preferredTermsLookup['annual_production'] = 'production'
    preferredTermsLookup['products'] = 'production'
    preferredTermsLookup['owners'] = 'owner'
    preferredTermsLookup['sharehoders'] = 'shareholders'
    preferredTermsLookup['shareholers'] = 'shareholders'
    preferredTermsLookup['sharehoolders'] = 'shareholders'
    preferredTermsLookup['shareholders_i'] = 'shareholders'
    preferredTermsLookup['former_name'] = 'other_name'
    preferredTermsLookup['other_names'] = 'other_name'
    preferredTermsLookup['oter_name'] = 'other_name'
    preferredTermsLookup['address_j'] = 'address'
    preferredTermsLookup['adress'] = 'address'
    preferredTermsLookup['phone'] = 'telephone'
    preferredTermsLookup['video'] = ''
    return preferredTermsLookup


processedLinks = []


def parsePPLpage(url, table):
    try:
        pplHtml = scraperwiki.scrape(url)
        pplRoot = lxml.html.fromstring(pplHtml)

    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return
    
    installationInfo=dict()

    #get PPL name on top of page
    pplName = pplRoot.xpath("string(//td[@class='contentheading'])").strip()
    installationInfo['name'] = pplName

    #get country just below
    pplCountry = pplRoot.xpath("//table[@class='contentpaneopen']//span/a/text()")[0]
    pplCountry = pplCountry.strip()
    if pplCountry in countryLookup:
        if pplCountry.find(countryLookup[pplCountry]) < 0:
            installationInfo['area'] = pplCountry
        pplCountry = countryLookup[pplCountry]
    installationInfo['country'] = pplCountry

    #get coordinates in javascript code for google maps
    coordMatcher = re.search(r"new GLatLng\(\s+([0-9.-]+),\s+([0-9.-]+)\)", pplHtml)
    if coordMatcher:
        installationInfo['latitude'] = coordMatcher.group(1)
        installationInfo['longitude'] = coordMatcher.group(2)

    installationInfo['url'] = url

    #iterate on bulleted info lines
    pplInfos = pplRoot.xpath("//table[@class='contentpaneopen']//li")
    for infoLine in pplInfos:
        key = infoLine.xpath("string(.//strong)")
        if len(key) > 0:
            key = key.replace(':','').lower().strip().replace(' ','_')
            if key in preferredTermsLookup:
                key = preferredTermsLookup[key]
            if key.replace('_','').isalnum():
                value = infoLine.xpath("string(.//strong/../text()[. != ' '] | .//strong/following-sibling::a/text())")
                if len(value) > 0 and not (key in installationInfo):
                    #clean up some buggy key/value combinations
                    if key == "power_capacity" and value.find("m3") > 0:
                        key = "water_capacity"
                    elif key == "power_capacity" and table.find("power") < 0:
                        key = "installed_capacity"
                    elif (key == "web" or key == "web_2") and value.find("wikipedia") > 0:
                        key = "wikipedia"
                    elif key == "wikipedia" and value.find("wikipedia") < 0:
                        key = "web"
                    if key == "area" and key in installationInfo:
                        installationInfo[key] += ", " + value.strip()
                    elif key == "web" or key == "web_2" or key == "wikipedia":
                        installationInfo[key] = value.strip()
                    else:
                        installationInfo[key] = value.replace(':','').strip()
            else:
                print "invalid key '" + key + "' in " + url

    #save to the database
    try:
        scraperwiki.sqlite.save(unique_keys=['url'], data=installationInfo, table_name=table)
    except:
        print "Error saving to DB" + ": " + str(sys.exc_info()[1])


def parseCategoryPage(url, table):

    targetUrl = url
    try:
        html = scraperwiki.scrape(targetUrl)
        root = lxml.html.fromstring(html)
    
        #handle pagination when there are more than 50 countries for a given fuel type
        pagination = root.xpath("//a[@title='Next']/@href")
        if len(pagination) > 0:
            targetUrl = 'http://www.industryabout.com'+pagination[0].replace('start=50','limit=0')
            html = scraperwiki.scrape(targetUrl)
            root = lxml.html.fromstring(html)

    except:
        print sys.exc_info()[0]
        print "Can't download " + targetUrl
        return
    
    subLinks = []

    #this matches on category pages (list of fuels or countries)
    if len(root.xpath("//table[@class='contentpane']//td/a[@class='category']")) > 0:
        subLinks = root.xpath("//a[@class='category']/@href")

    #this matches on intermediate pages that occur for some contries (especially the US)
    #those may be linked from several different paths and should be skipped if already processed
    elif len(root.xpath("//table[@class='contentpane']//li//a")) > 0:
        if table == "powerplants":
            subLinks = root.xpath("//table[@class='contentpane']//li//a[contains(.,'Energy') or contains(.,'Power')]/@href")
        elif table == "refineries":
            subLinks = root.xpath("//table[@class='contentpane']//li//a[contains(.,'Refineries')]/@href")
        
    #this matches on a special page for hydro power in France
    elif len(root.xpath("//table[@class='contentpane']//p[contains(.,'Complete list of power stations')]")) > 0:
        subLinks = root.xpath("//table[@class='contentpane']//p[contains(.,'Complete list of power stations')]//a/@href")
        
    for link in subLinks:
        if link not in processedLinks:
            processedLinks.append(link)
            parseCategoryPage('http://www.industryabout.com'+link, table)

    #this matches on powerplants list
    if len(root.xpath("//tr[starts-with(@class,'sectiontableentry')]//a")) > 0:
        subLinks = root.xpath("//tr[starts-with(@class,'sectiontableentry')]//a/@href")
        for link in subLinks:
            if link not in processedLinks:
                parsePPLpage('http://www.industryabout.com'+link, table)
                processedLinks.append(link)
    
    if len(subLinks) == 0:
        print "No links could be found in " + targetUrl

    return


countryLookup = createCountriesDict()
preferredTermsLookup = createPreferredTermsDict()


#starting page: energy home page
#home = "http://www.industryabout.com/energy"

#split in chunks to avoid reaching execution time limit

section = scraperwiki.sqlite.get_var('section', 2)

if section == 0:
    home = "http://www.industryabout.com/energy/fossil-fuels-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://industryabout.com/chemical-industry/oil-refineries"
    parseCategoryPage(home, 'refineries')
    scraperwiki.sqlite.save_var('section', 1)

elif section == 1:
    home = "http://www.industryabout.com/energy/hydro-power"
    parseCategoryPage(home, 'powerplants')
    scraperwiki.sqlite.save_var('section', 2)

elif section == 2:
    home = "http://www.industryabout.com/energy/biomass-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/geothermal-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/nuclear-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/solar-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/tidal-a-wave-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/waste-to-energy"
    parseCategoryPage(home, 'powerplants')
    home = "http://www.industryabout.com/energy/wind-energy"
    parseCategoryPage(home, 'powerplants')
    scraperwiki.sqlite.save_var('section', 0)



