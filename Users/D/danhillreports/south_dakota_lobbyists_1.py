import scraperwiki
import lxml.html
from geopy import geocoders

g = geocoders.GeoNames()

def process_name(name):
    names = name.split(',')
    first = names[0]
    last = names[1][:-1]
    return first + ' ' + last

def process_ll(address):
    try:
        add_string = g.geocode(address)
        if add_string:
            return (add_string)[1]
        else:
            return ' '
    except:
        return ' '

def scrape_page(html):
    page = scraperwiki.scrape(html)
    root = lxml.html.fromstring(page)
    table = root.cssselect("table")[4]
    links = root.cssselect("form")
    

    for tr in table.cssselect("tr")[1:]:
        #print tr.text_content()
        cells = tr.cssselect("td")
        #process_ll(cells[3].text_content()[:-1])
        data = {
            'year' : int(cells[0].text_content()),
            'lobbyist': process_name(cells[1].text_content()[:-1]),
            'lobbyist_address' : cells[2].text_content()[:-1],
            'lobbyist_city_state_zip' : cells[3].text_content()[:-1],
            'employer_name' : cells[4].text_content()[:-1],
            'employer_address' : cells[5].text_content()[:-1],
            'employer_city_state_zip' : cells[6].text_content()[:-1],
            'lat_lon' : process_ll(cells[3].text_content()[:-1])
        }
        print data
        #scraperwiki.sqlite.save(data.keys(), data=data)

base = "http://apps.sd.gov/applications/ST12ODRS/LobbyistViewlist.asp"
for n in range(1, 406, 20):
    start = "?start=" + str(n)
    html = base+start
    scrape_page(html)import scraperwiki
import lxml.html
from geopy import geocoders

g = geocoders.GeoNames()

def process_name(name):
    names = name.split(',')
    first = names[0]
    last = names[1][:-1]
    return first + ' ' + last

def process_ll(address):
    try:
        add_string = g.geocode(address)
        if add_string:
            return (add_string)[1]
        else:
            return ' '
    except:
        return ' '

def scrape_page(html):
    page = scraperwiki.scrape(html)
    root = lxml.html.fromstring(page)
    table = root.cssselect("table")[4]
    print table
    links = root.cssselect("form")
    

    for tr in table.cssselect("tr")[1:]:
        #print tr.text_content()
        cells = tr.cssselect("td")
        #process_ll(cells[3].text_content()[:-1])
        data = {
            'year' : int(cells[0].text_content()),
            'lobbyist': process_name(cells[1].text_content()[:-1]),
            'lobbyist_address' : cells[2].text_content()[:-1],
            'lobbyist_city_state_zip' : cells[3].text_content()[:-1],
            'employer_name' : cells[4].text_content()[:-1],
            'employer_address' : cells[5].text_content()[:-1],
            'employer_city_state_zip' : cells[6].text_content()[:-1],
            'lat_lon' : process_ll(cells[3].text_content()[:-1])
        }
        #print data
        #scraperwiki.sqlite.save(data.keys(), data=data)

base = "http://apps.sd.gov/applications/ST12ODRS/LobbyistViewlist.asp"
for n in range(1, 406, 20):
    start = "?start=" + str(n)
    html = base+start
    scrape_page(html)