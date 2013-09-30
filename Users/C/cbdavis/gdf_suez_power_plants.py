import scraperwiki
import lxml.html
import unicodedata

preferredTerms = dict()
preferredTerms['BE'] = 'Belgium'
preferredTerms['DE'] = 'Germany'
preferredTerms['FR GDFSUEZ'] = 'France'
preferredTerms['FR SHEM'] = 'France'
preferredTerms['HU'] = 'Hungary'
preferredTerms['IT'] = 'Italy'
preferredTerms['LU'] = 'Luxembourg'
preferredTerms['NL'] = 'Netherlands'
preferredTerms['PL'] = 'Poland'
preferredTerms['UK'] = 'United Kingdom'
preferredTerms['WA (Water)'] = 'Hydro'
preferredTerms['GO (Gas oil)'] = 'Fuel Oil' 
preferredTerms['NG (Natural Gas)'] = 'Natural Gas'
preferredTerms['PC (Pulverized coal)'] = 'Coal'
preferredTerms['NU (Nuclear)'] = 'Nuclear'

#function that checks if key exists before translating
def translate(key):
    if key in preferredTerms:
        return preferredTerms[key]
    else:
        return key


link = "http://transparency.gdfsuez.com/plant-units"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#find out how many pages
pageLinks = root.xpath('//div[@class="pagenavi"]/a/@href')

#add the first page to this list
pageLinks.insert(0, link)

for page in pageLinks:
    print page

    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)

    table = root.xpath("//table[@class='table-umm table-umm2']")[0]
    rows = table.xpath("//tr[position()>1]")
    for row in rows:
        
        installationInfo = dict()
        installationInfo['Name'] = row.xpath("./td[1]/span/text()")[0].title()
        installationInfo['Capacity'] = row.xpath("./td[2]/span/text()")[0].replace(',', '.')
        installationInfo['Country'] = translate(row.xpath("./td[3]/span/text()")[0])
        installationInfo['Fuel Type'] = translate(row.xpath("./td[4]/span/text()")[0])
        
        #add reference link to original data source
        installationInfo['reference_link'] = page

        scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
import scraperwiki
import lxml.html
import unicodedata

preferredTerms = dict()
preferredTerms['BE'] = 'Belgium'
preferredTerms['DE'] = 'Germany'
preferredTerms['FR GDFSUEZ'] = 'France'
preferredTerms['FR SHEM'] = 'France'
preferredTerms['HU'] = 'Hungary'
preferredTerms['IT'] = 'Italy'
preferredTerms['LU'] = 'Luxembourg'
preferredTerms['NL'] = 'Netherlands'
preferredTerms['PL'] = 'Poland'
preferredTerms['UK'] = 'United Kingdom'
preferredTerms['WA (Water)'] = 'Hydro'
preferredTerms['GO (Gas oil)'] = 'Fuel Oil' 
preferredTerms['NG (Natural Gas)'] = 'Natural Gas'
preferredTerms['PC (Pulverized coal)'] = 'Coal'
preferredTerms['NU (Nuclear)'] = 'Nuclear'

#function that checks if key exists before translating
def translate(key):
    if key in preferredTerms:
        return preferredTerms[key]
    else:
        return key


link = "http://transparency.gdfsuez.com/plant-units"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#find out how many pages
pageLinks = root.xpath('//div[@class="pagenavi"]/a/@href')

#add the first page to this list
pageLinks.insert(0, link)

for page in pageLinks:
    print page

    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)

    table = root.xpath("//table[@class='table-umm table-umm2']")[0]
    rows = table.xpath("//tr[position()>1]")
    for row in rows:
        
        installationInfo = dict()
        installationInfo['Name'] = row.xpath("./td[1]/span/text()")[0].title()
        installationInfo['Capacity'] = row.xpath("./td[2]/span/text()")[0].replace(',', '.')
        installationInfo['Country'] = translate(row.xpath("./td[3]/span/text()")[0])
        installationInfo['Fuel Type'] = translate(row.xpath("./td[4]/span/text()")[0])
        
        #add reference link to original data source
        installationInfo['reference_link'] = page

        scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
