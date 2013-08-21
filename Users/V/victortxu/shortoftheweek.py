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

def scrape_table_curts(url, notes, plot):    
    #print '--->url', '\n', url
    #print '--->size', '\n', size    


    htmlFitxa = scraperwiki.scrape(url)
    #print '--->htmFitxa', '\n', htmlFitxa

    soupFitxa = BeautifulSoup(htmlFitxa)
    #print '---> soupFitxa: ', soupFitxa

    try:
        data = {}
        
        data['url_fitxa'] = url
        print '--->url', '\n', url

        titol = soupFitxa.find('h1').contents[0]
        print '--->titol', '\n', titol
        data['title'] = titol

        #year = soupFitxa.find('span', {'class': 'film-date'}).contents[0]
        #print '---> year \n', year
        #data['year'] = year 

        runtime = soupFitxa.find('div', {'class': 'playButton'}).find('span', {'style': 'color:#34403C'}).contents[0]
        print '---> runtime \n', runtime
        data['runtime'] = runtime 

        #plot = soupFitxa.find('div', {'class': 'playButton'}).find('span', {'style': 'color:#34403C'}).contents[0]
        print '---> plot \n', plot
        data['plot'] = plot 

        director = soupFitxa.find('div', {'class': 'cluster'}).li.find('a')
        print '--->director', '\n', director.text
        data['director'] = director.text

        category = soupFitxa.find('div', {'class': 'categoryBig'}).find('a').contents[0]
        print '--->category', '\n', category
        data['category'] = category

        print '---> notes \n', notes
        data['notes'] = notes 
        
        video = soupFitxa.find('a', {'class': 'fancybox-video'})['href']
        print '---> video \n', video
        data['video_url'] = video

  
        scraperwiki.sqlite.save(['url_fitxa'], data, table_name="curts")
   
    except Exception: 
        print '---> error :', url, ara()
        error = {}
        error['url_fitxa'] = url
        error['id'] = ara()



        scraperwiki.sqlite.save(['url_fitxa'], error, table_name="error")
        pass 





def scrape_table_llistat(root):
    html = scraperwiki.scrape(root)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    for url_fitxa in soup.findAll('div', {'class': 'filmlisttext'}):
        url = url_fitxa.find('div', {'class': 'filmlisttitle'}).a['href']
        #print '--->url\n', url

        notes = url_fitxa.find('div', {'class': 'filmlistdetail'}).text
        #print '--->notes\n', notes

        plot = url_fitxa.find('div', {'class': 'excerpt'}).text
        #print '--->plot\n', plot

        
        if not (url == "http://www.twitter.com/shortoftheweek"  or url == "http://www.shortoftheweek.com/submit/" ):     # CORRECT!  
            #print '--->url\n', url
            scrape_table_curts(url, notes, plot)
        
        #url = url_fitxa['href']
        #size = url_fitxa.findNextSibling('span', {'class': 'time-vedeo'}).contents[0]
        #print '---> size: ', size
        #scrape_table_curts(url, size)





def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print  '--->html:\n', html
    
    soup = BeautifulSoup(html)
    #print '--->soup\n', soup
    
    for url_llistat_cat in soup.findAll('div', {'class': 'categoryBig'}):
        #print '--->url_llistat_cat:\n',url_llistat_cat
        for llistat_li in url_llistat_cat.findAll('li'):
            #print llistat_li.a['href']
            scrape_table_llistat(llistat_li.a['href'])

        
base_url = 'http://www.shortoftheweek.com/films/'

#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)