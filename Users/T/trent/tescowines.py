import scraperwiki
from BeautifulSoup import BeautifulSoup

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("p", {"class" : "next"})

    if next_link.a != None:
        next_url = next_link.find("a")['href']
        scrape_and_look_for_next_link(next_url)

def scrape_table(soup):
    wineDiv = soup.find('ul','line')
    wineLi = wineDiv.findAll('li')
    for w in wineLi:
        cont = w.find("div","descContent")
        if cont:
            nameA = cont.find("a")
            if nameA:
                keyfacts = w.find("div","keyFacts collapsible")
                if keyfacts:
                    factsodd = keyfacts.find("dl", "odd")
                    factseven = keyfacts.find("dl", "even")
                    if factsodd:
                        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":nameA.text, "factsOdd":factsodd, "factsEven":factseven})

base_url = 'http://www.tesco.com/wine/product/browse/default.aspx'
starting_url = base_url + '?No=0&N=0'
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("p", {"class" : "next"})

    if next_link.a != None:
        next_url = next_link.find("a")['href']
        scrape_and_look_for_next_link(next_url)

def scrape_table(soup):
    wineDiv = soup.find('ul','line')
    wineLi = wineDiv.findAll('li')
    for w in wineLi:
        cont = w.find("div","descContent")
        if cont:
            nameA = cont.find("a")
            if nameA:
                keyfacts = w.find("div","keyFacts collapsible")
                if keyfacts:
                    factsodd = keyfacts.find("dl", "odd")
                    factseven = keyfacts.find("dl", "even")
                    if factsodd:
                        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":nameA.text, "factsOdd":factsodd, "factsEven":factseven})

base_url = 'http://www.tesco.com/wine/product/browse/default.aspx'
starting_url = base_url + '?No=0&N=0'
scrape_and_look_for_next_link(starting_url)
