# ALL REGISTERED SHIPS, WITH INFO LINK, HOME HARBOUR LINK AND OPERATOR LINK - from: http://sax.is/ - This will be a placeholder database for info links being used by another scraper


import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starturl = 'http://sax.is/?gluggi=skip_listi'



def scrape_ship_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()

    ships = soup.findAll('tr', {'class' : 'leitarlina' })
    for td in ships:
        ship = {}
        name = td.find('td')
        #print name.text
        ship_link = name.findNext('a')
        #print "http://sax.is/" + ship_link['href']
        make = name.findNext('td')
        operator_link = make.findNext('a')
        #print "http://sax.is/" + operator_link['href']
        #print make.text
        operator = make.findNext('td')
        #print operator.text
        build_year = operator.findNext('td')
        #print build_year.text
        harbour_link = build_year.findNext('a')
        #print "http://sax.is/" + harbour_link['href']
        home_harbour = build_year.findNext('td')
        #print home_harbour.text
        pictures = home_harbour.findNext('td')
        #print pictures.text 

        ship['name'] = name.text
        ship['type'] = make.text
        ship['ship_link'] = "http://sax.is/" + ship_link['href']
        ship['operator'] = operator.text
        if operator_link['href'] == '?gluggi=utgerd&id=':
            ship['operator_link'] = "n/a"
        else:
            ship['operator_link'] = "http://sax.is/" + operator_link['href']
        
        ship['build_year'] = build_year.text
        ship['home_harbour'] = home_harbour.text

        if harbour_link == "?gluggi=hofn&id=0":
            ship['harbour_link'] = "n/a"
        else:
            ship['harbour_link'] = "http://sax.is/" + harbour_link['href']

        ship['pictures'] = pictures.text 
        print ship
        scraperwiki.datastore.save(["name"], ship)     

scrape_ship_list(starturl)
