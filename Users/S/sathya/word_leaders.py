import scraperwiki           
import lxml.html

# scrap "https://www.cia.gov/library/publications/world-leaders-1/index.html"
# https://www.cia.gov/library/publications/world-leaders-1/world-leaders-a/world-leaders-a.html

html = scraperwiki.scrape("https://www.cia.gov/library/publications/world-leaders-1/index.html")
root = lxml.html.fromstring(html)

index = 0

indexUrls = root.cssselect("div[id='content'] >div[class='plain'] > p:nth-child(6) > b > a")

for indexUrl in indexUrls:     
    site2 = scraperwiki.scrape("https://www.cia.gov" + indexUrl.attrib['href'])
    root2 = lxml.html.fromstring(site2)
    
    countries = root2.cssselect("div[id='region-content'] > div[id='content'] > div[class='plain'] > p > a")
    for country in countries:
        site3 = scraperwiki.scrape("https://www.cia.gov" + country.attrib['href'])
        root3 = lxml.html.fromstring(site3)       
        countryTitle = root3.cssselect("div[id='content'] > h1[class='documentFirstHeading']")
        leaders = root3.cssselect("div[id='content'] > div[class='plain'] > table > tbody > tr")
        countryLeadersInformation = []
        for leaderData in leaders:
            leaderNode = lxml.html.fromstring(lxml.html.tostring(leaderData))
            leader     = leaderNode.cssselect("td")
            if len(leader) > 1 and leader[0].text != None and leader[0].text != "":
                if leader[1].text_content() != None and leader[1].text_content() != "":
                    print leader[0].text
                    print leader[1].text_content(
                    countryLeadersInformation.append(leader[0].text + ":" + leader[1].text_content()) 

        index = index + 1
        data = {
                "id"      : index,
                "country" : countryTitle[0].text,
                "leaders" : countryLeadersInformation                            
               }
        
        scraperwiki.sqlite.save(unique_keys=['id'], table_name="Leaders", data=data)
    