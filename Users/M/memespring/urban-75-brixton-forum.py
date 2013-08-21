import scraperwiki
from BeautifulSoup import BeautifulSoup


forum_url = 'http://bolt.org/board/forumdisplay.php?f=19'
html = scraperwiki.scrape(forum_url)
soup = BeautifulSoup(html)

#find all the threads
threads = soup.findAll('div', {'class': 'threadinfo'})
for thread in threads:
    
    #link & title
    link = thread.find('a', {'class': 'title'})
    url = 'http://bolt.org/board/' + link['href'] 
    title = link.string
    

    #save to datastore    
    scraperwiki.datastore.save(unique_keys=['url',], data={'url': url, 'title': title})    

