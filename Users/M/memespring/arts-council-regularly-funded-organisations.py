###############################################################################
# Arts Council Regularly Funded Organisations
# TODO: add artform, links to org's website and latlng
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def get_all_links():
    
    links = []
    counter = 1
    end = False
    while end == False:
        # retrieve a page
        starting_url = 'http://www.artscouncil.org.uk/browse/?page=%i&content=RFO' % counter
        html = scraperwiki.scrape(starting_url)
        soup = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)

        search_results = soup.findAll('div', {'class': 'search-result'}) 
        if search_results:
            for div in search_results:
                links.append('http://www.artscouncil.org.uk' + div.find('h3').find('a')['href'])
            counter = counter + 1
        else:
           end = True
    
    return links
                    
links = get_all_links()
for url in links:
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)    
    
    #name
    org_name = soup.find('h1').string
    
    
    #description
    description = ''
    description_p = soup.find('div', {'id': 'column-external'}).find('p')
    if description_p:
        description = soup.find('div', {'id': 'column-external'}).find('p').string
    
    #address
    address = ''
    address_p = soup.find('p', {'class': 'address adr'})
    for line in address_p.contents:
        if line.string and line.string != '' and line.string != ' ' and line.string != ',' and line.string != ', ':
            address = address + line.string + ', '
    
    #lat lng
    latlng = None    
    map_div = soup.find('div', {'class': 'box box-map'})
    if map_div:
        map_img = map_div.find('img')
        latlng_split = map_img['src'].split('|')[1].split(',')
        latlng = [float(latlng_split[0]), float(latlng_split[1])]
    
    
    #save to the max
    scraperwiki.datastore.save(unique_keys=['url',], data={'url': url, 'name': org_name, 'address': address}, latlng=latlng)
    
    
