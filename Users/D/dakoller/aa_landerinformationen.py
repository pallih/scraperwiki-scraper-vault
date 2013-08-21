import scraperwiki           
import lxml.html

#scraperwiki.sqlite.execute("delete from country_swdata")

html = scraperwiki.scrape("http://www.auswaertiges-amt.de/DE/Laenderinformationen/SicherheitshinweiseA-Z-Laenderauswahlseite_node.html")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.glossarLevel2 ul li a"):
    country= el.attrib["title"].split(":")[0]
    detail_link = "http://www.auswaertiges-amt.de/"+el.attrib["href"]

    print country
    print detail_link

    spotlight_country=""
    try:
        spotlight_link= "http://spotlight.dbpedia.org/rest/annotate?text=" + country
        spotlight_html= scraperwiki.scrape(spotlight_link)
        spotlight_root = lxml.html.fromstring(spotlight_html)
        for spotlight_el in spotlight_root.cssselect("div a"):
            spotlight_country=  spotlight_el.attrib["href"] 
    except:
        pass

    print spotlight_country

    data = {
        'country'       : country,
        'detail_link'   : detail_link,
        'country_dbpedia': spotlight_country,
    }
    
    scraperwiki.sqlite.save(unique_keys=["country"], data= data, table_name="country_swdata")
  