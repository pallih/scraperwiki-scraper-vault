import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

def scrape_table_curts(root):
    htmlFitxa = scraperwiki.scrape(root)
    print htmlFitxa
        
    soupFitxa = BeautifulSoup(htmlFitxa)
    #print soupFitxa
        
    #scrape_table_curt(rootFitxa)
        
    titol = soupFitxa.h1.contents[0]
    print titol
    data['title'] = titol
    any = soupFitxa.right.ul.li.a.contents[0]
    #print any
    data['year'] = any
    
    director = soupFitxa.right.ul('li')[1].a.contents[0]
    #print director
    data['director'] = director

    productor = soupFitxa.right.ul('li')[2].a.contents[0]
    #print productor
    data['productor'] = productor        

    guion = soupFitxa.right.ul('li')[3].a.contents[0]
    #print guion
    data['writer'] = guion 
        
    actor = soupFitxa.right.ul('li')[4].a.contents[0]
    #print actor
    data['cast'] = actor 

    pais = soupFitxa.right.ul('li')[5].a.contents[0]
    #print pais
    data['year'] = pais 

    plot = soupFitxa.find('p', text=re.compile("Sinopsis cortometraje:"))
    #print plot
    data['plot'] = plot

        #plot2 = soupFitxa.findAll('p', text=re.compile("Sinopsis cortometraje:"))
        #print plot2

    scraperwiki.sqlite.save(['href'], data)





# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.cssselect("div.post-thumbnail a")
    #print url_fitxes.attrib['href']
    for url_fitxa in url_fitxes:
        print url_fitxa.attrib['href']
        #print url_fitxa.attrib['title']
        data = {}
        data['href'] = url_fitxa.attrib['href']
        url = url_fitxa.attrib['href']
        #data['title'] = url_fitxa.attrib['title']
        #print data['href']
        scrape_table_curts(url):
        ######


        
        
##html body.single div#page-wrapper div#content-wrapper div#content div#review-container div#review-panel-right right ul#review-tags-list li a
#<h1 class="page-title">Clock (2012)</h1>
        
 

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
scrape_and_look_for_next_link(base_url)import scraperwiki
#import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

def scrape_table_curts(root):
    htmlFitxa = scraperwiki.scrape(root)
    print htmlFitxa
        
    soupFitxa = BeautifulSoup(htmlFitxa)
    #print soupFitxa
        
    #scrape_table_curt(rootFitxa)
        
    titol = soupFitxa.h1.contents[0]
    print titol
    data['title'] = titol
    any = soupFitxa.right.ul.li.a.contents[0]
    #print any
    data['year'] = any
    
    director = soupFitxa.right.ul('li')[1].a.contents[0]
    #print director
    data['director'] = director

    productor = soupFitxa.right.ul('li')[2].a.contents[0]
    #print productor
    data['productor'] = productor        

    guion = soupFitxa.right.ul('li')[3].a.contents[0]
    #print guion
    data['writer'] = guion 
        
    actor = soupFitxa.right.ul('li')[4].a.contents[0]
    #print actor
    data['cast'] = actor 

    pais = soupFitxa.right.ul('li')[5].a.contents[0]
    #print pais
    data['year'] = pais 

    plot = soupFitxa.find('p', text=re.compile("Sinopsis cortometraje:"))
    #print plot
    data['plot'] = plot

        #plot2 = soupFitxa.findAll('p', text=re.compile("Sinopsis cortometraje:"))
        #print plot2

    scraperwiki.sqlite.save(['href'], data)





# scrape_table function: gets passed an individual page to scrape
def scrape_table_llistat(root):
    url_fitxes = root.cssselect("div.post-thumbnail a")
    #print url_fitxes.attrib['href']
    for url_fitxa in url_fitxes:
        print url_fitxa.attrib['href']
        #print url_fitxa.attrib['title']
        data = {}
        data['href'] = url_fitxa.attrib['href']
        url = url_fitxa.attrib['href']
        #data['title'] = url_fitxa.attrib['title']
        #print data['href']
        scrape_table_curts(url):
        ######


        
        
##html body.single div#page-wrapper div#content-wrapper div#content div#review-container div#review-panel-right right ul#review-tags-list li a
#<h1 class="page-title">Clock (2012)</h1>
        
 

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