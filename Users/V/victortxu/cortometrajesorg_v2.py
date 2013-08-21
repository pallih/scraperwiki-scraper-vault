import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def scrape_table_curts(url):    
    htmlFitxa = scraperwiki.scrape(url)
    #print htmlFitxa
        
    soupFitxa = BeautifulSoup(htmlFitxa)
    #print soupFitxa
    
    data = {}
    data['url_fitxa'] = url

    titol = soupFitxa.h1.contents[0]
    #print titol
    data['title'] = titol

    for dades in soupFitxa.findAll('ul', id="review-tags-list"):
    #print dades
        
        for dades_li in dades.findAll('li'):
            #print dades_li
            #print dades_li.text
            
            txtval = dades_li.text
            pp= txtval.split(':')
            
            #print pp[0]
            #print pp[1]
            
            if pp[0].encode("utf-8") == 'Año':
                  data['year'] = pp[1]
            
            elif pp[0].encode("utf-8") == 'Director':
                  data['director'] = pp[1]
            
            elif pp[0].encode("utf-8") == 'Guión':
                data['writer'] = pp[1]

            elif pp[0].encode("utf-8") == 'Actor':
                data['cast'] = pp[1]

            elif pp[0].encode("utf-8") == 'País':
                data['country'] = pp[1]
    
    #plot = soupFitxa.find('p', text=re.compile("Sinopsis cortometraje:"))
    
    plot = soupFitxa.find('div', {'class': 'review-panel'}).findAll('p')
    
    #print striphtml(''.join(map(str, plot)))
    data['plot'] = striphtml(''.join(map(str, plot)))
    
    video_object = soupFitxa.find('div', {'class': 'review-panel'}).findAll('object')#.findAll('param', {'name': 'src'})
    if video_object:
        video_str = str(video_object)
        match = re.search(r'src="(.*?)"', video_str)
        if match:
            #print ' ---video_object---', match.group(1)
            data['url_video'] = match.group(1)

    video_wp = soupFitxa.find('div', {'class': 'sc-video-inner'})#.findAll(id="video-video_wrapper")#.findAll('param', {'name': 'movie'})
    #print video_wp , '>>> video object wp'
    if video_wp:
        video_str = str(video_wp)
        match = re.search(r'{file: "(.*?)"', video_str)
        if match:
            #print '---video_wp---', match.group(1)  
            data['url_video'] = match.group(1)

    video_iframe = soupFitxa.find('div', {'class': 'review-panel'}).find('iframe')
    #print video , '>>> video iframe'
    if video_iframe:
            #print '---video_iframe---', video_iframe['src']  
            data['url_video'] = video_iframe['src']

    scraperwiki.sqlite.save(['url_fitxa'], data)


# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.cssselect("div.post-thumbnail a")
    #print url_fitxes.attrib['href']
    for url_fitxa in url_fitxes:
        print url_fitxa.attrib['href']
        #print url_fitxa.attrib['title']

        #print data['href']
        url = url_fitxa.attrib['href']
        scrape_table_curts(url)


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    #print root
    scrape_table_llistat(root)
    #print tostring(root, pretty_print=True)
    #next_link = root.find_rel_links('next')
    soup = BeautifulSoup(html)
    #scrape_table_llistat(soup)
    next_link = soup.find('link', rel = 'next')['href']
    #print next_link
    if next_link:
        #next_url = urlparse.urljoin(base_url, next_link)
        #print next_url
        scrape_and_look_for_next_link(next_link)


base_url = 'http://cortometrajes.org/cortometrajes/'
#starting_url = urlparse.urljoin(base_url, 'page/1/')
scrape_and_look_for_next_link(base_url)