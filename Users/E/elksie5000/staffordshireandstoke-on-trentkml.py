import scraperwiki
import lxml.html
import lxml.etree

FULL_STOP= ".html"



base_url = ("http://mapit.mysociety.org/area/2568/children.html", "http://mapit.mysociety.org/area/2432/children.html", "http://mapit.mysociety.org/area/2436/children.html", "http://mapit.mysociety.org/area/2437/children.html", "http://mapit.mysociety.org/area/2435/children.html")


            
def scrape_base (base_url):
    html =  scraperwiki.scrape(base_url)     
    root = lxml.html.fromstring(html)
    a_links = root.cssselect("article.content ol.area_list li h3 a")
    for el in a_links:
        id_URL = el.attrib['href']
        id = id_URL[6:]
        new_id =""
        for char in id:
            if char not in FULL_STOP:
                new_id += char
        url_KML = "http://mapit.mysociety.org/area/"+new_id+".kml"
        print "About to scrape "+url_KML
        KML_data = scraperwiki.scrape(url_KML)     
        KML_root = lxml.html.fromstring(KML_data)
        name = KML_root.cssselect("name")
        name = lxml.html.tostring(name[0])
        KML = KML_root.cssselect("polygon")
        KML = lxml.html.tostring(KML[0])
        record = {}
        record['Name'] = name[6:-7]
        record['KML'] = KML
        print record, '--------'
        scraperwiki.sqlite.save(['Name'], record)   



for el in base_url:
    print el
    scrape_base(el)

