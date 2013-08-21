import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

parties = {
    "CDA":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie5kd3um06h",
    "PvdA":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6ejf9l2s4",
    "SP":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6eq64q3s6",
    "VVD":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6elqwcss5",
    "PVV":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6exfae7x4",
    "GroenLinks":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6ehbt5cs3", 
    "ChristenUnie":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6ezaz2sx5",
    "D66":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6f1752nx6",
    "SGP":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6f7dlfxx8",
    "Partij voor de Dieren":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6f3kxasx7",
    "Trots op Nederland":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vie6fgnntdx9",
    "Niew Nederland":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif2berxm55k",
    "Partij voor Mens en Spirit":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif2d8o654oh",
    "Heel NL":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif3eilf7yqn",
    "Partij één":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif2jdonynwf",
    "Piratenpartij":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif4b84s4izc",
    "lijst-Lacé":
        "http://www.parlement.com/9353000/1/j9vvhy5i95k8zxl/vif3fxqy6eqo"
}

for party in parties:
    print "Starting to scrape " + party
    html = scraperwiki.scrape(parties[party])
    start = html.find('<a name="par2" class="h1">Kandidaten</a>')
    page = BeautifulSoup.BeautifulSoup(html[start:])
    if "table" in page:
        for person_row in page.find("table").findAll("tr"):
            try:
                name_and_position = person_row.findAll('td')[1].a.string
                position = int(name_and_position.split()[0])
                name = " ".join(name_and_position.split()[1:])   
                link = "http://www.parlement.com" + person_row.td.a["href"]
            
                person_html = scraperwiki.scrape(link)
                person_page = BeautifulSoup.BeautifulSoup(person_html)
                image_url = "http://www.parlement.com" + person_page.find("img")["src"]
        
                person = {"name": name, "position": position, "link": link, "party": party, "image_url": image_url}            
                datastore.save(unique_keys=['link',], data=person)
            except:
                pass


