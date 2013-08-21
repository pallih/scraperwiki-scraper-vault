import scraperwiki           
import lxml.html
import string
import re

# scrap "https://www.cia.gov/library/publications/world-leaders-1/index.html"
# https://www.cia.gov/library/publications/world-leaders-1/world-leaders-a/world-leaders-a.html

html = scraperwiki.scrape("https://www.cia.gov/library/publications/world-leaders-1/index.html")
root = lxml.html.fromstring(html)

index = 0

indexUrls = root.cssselect("div[id='content'] >div[class='plain'] > p:nth-child(6) > b > a")

for indexUrl in indexUrls:     
    site2 = scraperwiki.scrape("https://www.cia.gov" + indexUrl.attrib['href'])
#    site2 = scraperwiki.scrape("https://www.cia.gov/library/publications/world-leaders-1/world-leaders-g/world-leaders-g.html")
    root2 = lxml.html.fromstring(site2)
    
    countries = root2.cssselect("div[id='region-content'] > div[id='content'] > div[class='plain'] > p > a, div[id='region-content'] > div[id='content'] > div[class='plain'] > p > strong > a")
    for i in range(0, len(countries)-1):
        country = countries[i].text_content()
        #regex = re.compile("([\W])")
        if 1 == 1: #not regex.search(country):
            #print country
            site3 = scraperwiki.scrape("https://www.cia.gov" + countries[i].attrib['href'])
            root3 = lxml.html.fromstring(site3)       
            countryTitle = root3.cssselect("div[id='content'] > h1[class='documentFirstHeading']")
            leaders = root3.cssselect("div[id='content'] > div[class='plain'] > table > tbody > tr, div[class='plain'] > div > div > table > tbody > tr")
            countryLeadersInformation = ">>";
            for leaderData in leaders:
                leaderNode = lxml.html.fromstring(lxml.html.tostring(leaderData))
                leader     = leaderNode.cssselect("td")
                if len(leader) > 1 and leader[0].text != None and leader[0].text != "":
                    if leader[1].text_content() != None and leader[1].text_content() != "":
                        leadersInfo = (leader[0].text) + ":" + string.capitalize(leader[1].text_content())
                        leadersInfo = string.replace(leadersInfo, "\n", "")
                        leadersInfo = string.replace(leadersInfo, "\r", "")

                        if countryLeadersInformation == ">>":
                            countryLeadersInformation =   leadersInfo
                        else:
                            countryLeadersInformation = countryLeadersInformation + "&split&" + leadersInfo
# break
#     print leadersInfo

            index = index + 1
            data = {
                "id"      : index,
                "country" : countryTitle[0].text,
                "leaders" : countryLeadersInformation                            
               }
            
            print data        

            scraperwiki.sqlite.save(unique_keys=['id'], table_name="Leaders", data=data)
