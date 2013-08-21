import scraperwiki           
import lxml.html

scraperwiki.sqlite.execute("delete from swdata")

html = scraperwiki.scrape("http://www.auswaertiges-amt.de/DE/Laenderinformationen/01-Reisewarnungen-Liste_node.html#doc536872bodyText2")
root = lxml.html.fromstring(html)

for el in root.cssselect("ul.discLinkMarginBottom li a"):
    country= el.attrib["title"].split(":")

    spotlight_country=""
    try:
        spotlight_link= "http://spotlight.dbpedia.org/rest/annotate?text=" + country[0]
        spotlight_html= scraperwiki.scrape(spotlight_link)
        spotlight_root = lxml.html.fromstring(spotlight_html)
        for spotlight_el in spotlight_root.cssselect("div a"):
            spotlight_country=  spotlight_el.attrib["href"] 

    except:
        pass

    warning_detail=''
    try:
        warning_link= "http://www.auswaertiges-amt.de/"+ el.attrib["href"]
        warning_html = scraperwiki.scrape(warning_link)
        warning_root= lxml.html.fromstring(warning_html)
        
    except:
        pass

    data = {
      'country_name' : country[0],
      'detail_link'  : "http://www.auswaertiges-amt.de/"+ el.attrib["href"],  
      'country_dbpedia' : spotlight_country,
      'warning_detail'  : ''  
    }
 
    scraperwiki.sqlite.save(unique_keys=['country_name'], data=data)