base_url = "https://www.cia.gov/library/publications/the-world-factbook"

import scraperwiki
import lxml.html

index_data = scraperwiki.scrape("%s/index.html" % base_url)

root = lxml.html.fromstring(index_data)

country_list = root.xpath("//form[@id='SelectCountry']/select[@id='countryCode']/option")

i=-1
#page_data={}
for option in country_list:
    country=option.get('value')
    if(len(country)): ##there are some empty elements
        i=i+1
        print country
        page_data=( scraperwiki.scrape(base_url+"/geos/"+country+".html" ))
        scraperwiki.sqlite.save(unique_keys=["countryname"], data={"countryname":country, "pagedata":page_data}, table_name="cia_data", verbose=2)
    #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Hi there"})



