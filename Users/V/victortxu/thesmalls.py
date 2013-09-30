import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())

def scrape_table_curts(url,size):    
    #print '--->url', '\n', url
    #print '--->size', '\n', size    


    htmlFitxa = scraperwiki.scrape(url)
    #print '--->htmFitxa', '\n', htmlFitxa

    soupFitxa = BeautifulSoup(htmlFitxa)
    #print soupFitxa
    
    try:
        data = {}
        data['url_fitxa'] = url
        data['size'] = size
    
        titol = soupFitxa.find('div', {'class': 'film-title-date'}).span.contents[0]
        #print '--->titol', '\n', titol
        data['title'] = titol
        
        director = soupFitxa.find('div', {'class': 'user-name'}).a.contents[0]
        #print '--->director', '\n', director
        data['director'] = director
    
        plot = soupFitxa.find('div', {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'}).find('div', {'class': 'field-items'}).find('div', {'class': 'field-item even'}).contents[0]
        plot_str = striphtml(str(plot))
        #print '--->plot', '\n', plot_str
        data['plot'] = plot_str
    
        video = soupFitxa.find('div', {'class': 'jwplayer-video'}).source['src']
        #print '---> video \n', video
        data['video_url'] = video
        
        year = soupFitxa.find('span', {'class': 'film-date'}).contents[0]
        print '---> year \n', year
        data['year'] = year    

        scraperwiki.sqlite.save(['url_fitxa'], data, table_name="curts")
       
    except Exception: 
        print '---> error :', url, ara()
        error = {}
        error['url_fitxa'] = url
        error['id'] = ara()



        scraperwiki.sqlite.save(['url_fitxa'], error, table_name="error")
        pass 

     


# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.findAll('a', {'class': 'title-link'})
    #print '--->url_fitxes', '\n', url_fitxes
    for url_fitxa in url_fitxes:
        #print url_fitxa.a['href']

        url = url_fitxa['href']
        size = url_fitxa.findNextSibling('span', {'class': 'time-vedeo'}).contents[0]
        #print '---> size: ', size
        scrape_table_curts(url, size)


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    scrape_table_llistat(soup)

    next_link = soup.find('li', {'class': 'pager-next'}).a['href']
    #print '--->next_link', '\n', next_link
    
    if next_link:
        scrape_and_look_for_next_link(next_link)
        

#base_url = 'http://www.thesmalls.com/browse/films'
base_url = 'http://www.thesmalls.com/browse/films?&&group_location_field_location_tags=&group_equipment_field_audio_equipment=&group_equipment_field_film_tags=&group_equipment_field_lighting_rigs=&group_equipment_field_my_cameras=&group_equipment_field_my_lenses=&group_equipment_field_software=&group_equipment_field_video_editing=&sort_by=created&sort_order=DESC&is_node=1&page=41'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)
import scraperwiki
import time
import re
from BeautifulSoup import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def ara():
    '''return a UNIX style timestamp representing now'''
    return int(time.time())

def scrape_table_curts(url,size):    
    #print '--->url', '\n', url
    #print '--->size', '\n', size    


    htmlFitxa = scraperwiki.scrape(url)
    #print '--->htmFitxa', '\n', htmlFitxa

    soupFitxa = BeautifulSoup(htmlFitxa)
    #print soupFitxa
    
    try:
        data = {}
        data['url_fitxa'] = url
        data['size'] = size
    
        titol = soupFitxa.find('div', {'class': 'film-title-date'}).span.contents[0]
        #print '--->titol', '\n', titol
        data['title'] = titol
        
        director = soupFitxa.find('div', {'class': 'user-name'}).a.contents[0]
        #print '--->director', '\n', director
        data['director'] = director
    
        plot = soupFitxa.find('div', {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'}).find('div', {'class': 'field-items'}).find('div', {'class': 'field-item even'}).contents[0]
        plot_str = striphtml(str(plot))
        #print '--->plot', '\n', plot_str
        data['plot'] = plot_str
    
        video = soupFitxa.find('div', {'class': 'jwplayer-video'}).source['src']
        #print '---> video \n', video
        data['video_url'] = video
        
        year = soupFitxa.find('span', {'class': 'film-date'}).contents[0]
        print '---> year \n', year
        data['year'] = year    

        scraperwiki.sqlite.save(['url_fitxa'], data, table_name="curts")
       
    except Exception: 
        print '---> error :', url, ara()
        error = {}
        error['url_fitxa'] = url
        error['id'] = ara()



        scraperwiki.sqlite.save(['url_fitxa'], error, table_name="error")
        pass 

     


# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.findAll('a', {'class': 'title-link'})
    #print '--->url_fitxes', '\n', url_fitxes
    for url_fitxa in url_fitxes:
        #print url_fitxa.a['href']

        url = url_fitxa['href']
        size = url_fitxa.findNextSibling('span', {'class': 'time-vedeo'}).contents[0]
        #print '---> size: ', size
        scrape_table_curts(url, size)


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    scrape_table_llistat(soup)

    next_link = soup.find('li', {'class': 'pager-next'}).a['href']
    #print '--->next_link', '\n', next_link
    
    if next_link:
        scrape_and_look_for_next_link(next_link)
        

#base_url = 'http://www.thesmalls.com/browse/films'
base_url = 'http://www.thesmalls.com/browse/films?&&group_location_field_location_tags=&group_equipment_field_audio_equipment=&group_equipment_field_film_tags=&group_equipment_field_lighting_rigs=&group_equipment_field_my_cameras=&group_equipment_field_my_lenses=&group_equipment_field_software=&group_equipment_field_video_editing=&sort_by=created&sort_order=DESC&is_node=1&page=41'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)
