# Some sexy libraries
import scraperwiki
import lxml.html
import requests
import re
import time

# Declare list for results
inspections = []

# Use request library to run post request
# Permit type 11 is school cafeterias
headers  = {"a":"Inspections",
"inputEstabName":"",
"inputPermitType":11,
"inputInspType":"ANY",
"inputWard":"ANY",
"inputQuad":"ANY",
"btnSearch":"Search"}

requestPost = requests.post("http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm", data = headers)

# Find the links on the page

postParse = lxml.html.fromstring(requestPost.text)
links = postParse.xpath('//div[@id="divInspectionSearchResults"]//a/@href')

inspections = []

#Follow each of them and scrape the subsequent page
for link in links:

    #just the html results
    if "_paper_food_inspection_report" in link:
        
        inspection_dict = {}
        inspection_dict['info'] = {}

        #turn relative url into absolute
        url = link.replace("..","http://washington.dc.gegov.com/webadmin/dhd_431")
        try:
            result = scraperwiki.scrape(url)
        except:
            pass
        if result:
            print "Scraping "+url
            resultParse = lxml.html.fromstring(result)

            #table for name address, date of inspection
            inspectionInfo = resultParse.xpath('//table[@class = "pt8 times"]//table')[0]
            infoRows = inspectionInfo.xpath('tr/td')
            inspection_dict['info']['url'] = url
            inspection_dict['info']['name'] = infoRows[0].xpath('span')[0].text_content().strip()
            rawAddy = infoRows[1].xpath('span')
            streetAddy = rawAddy[0].text_content().strip()
            zipAndStuff = rawAddy[1].text_content().strip()
            inspection_dict['info']['street_address'] = streetAddy
            inspection_dict['info']['zip_and_etc'] = zipAndStuff
            rawDate = infoRows[3].xpath('span')
            inspection_dict['info']['date'] = rawDate[0].text_content().strip()+"/"+rawDate[1].text_content().strip()+"/"+rawDate[2].text_content().strip()        
        
            observation = resultParse.xpath('//table[@class = "times fs_10px"]/tr')            
            
            inspection_dict['violations']=[]
            for row in observation[1:]:
                violation = {}
        
                td = row.xpath('td[not(@colspan="3")]')
                if td:
                    violation['action'] = td[2].text_content().strip()
                    violation['code'] = td[1].text_content().strip()
                    violation['description'] = td[0].text_content().strip()
                    inspection_dict['violations'].append(violation)
            inspections.append(inspection_dict)
            
            time.sleep(5)

for inspection in inspections:
    scraperwiki.sqlite.save([], inspection, table_name='dc_restaurant_inspections_2012')