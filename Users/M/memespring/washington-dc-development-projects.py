import time
import scraperwiki
from BeautifulSoup import BeautifulSoup


def get_urls():
    urls = []
    carry_on = True
    counter = 0
    while carry_on:
        starting_url = 'http://dmped.dc.gov/DC/DMPED/Projects/Development+Projects?renderPage=%d' % counter
        html = scraperwiki.scrape(starting_url)
        soup = BeautifulSoup(html)

        # use BeautifulSoup to get all <a href> tags to parse further
        project_divs = soup.findAll('div', {'class': 'dcEvent'}) 
        if project_divs:
            for project_div in project_divs:
                url = 'http://dmped.dc.gov' + project_div.find('a')['href']
                urls.append(url)
                print "GETTING PAGE:  " + url
            counter = counter + 1
            #carry_on = False #UNCOMMENT TO TEST
        else:
            carry_on = False
            print "STOPPING NOW."
        #be nice to the server
        time.sleep(2)
        
    return urls
    
def save_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    data = {}
    data['url'] = url

    #get title
    title = soup.find('h2', {'class': 'contentBodyTitle'}).string.replace('&nbsp;', '')
    data['title'] = title
    
    #get stats
    stats_divs = soup.find('div', {'class': 'rightNavContainerOne'}).findAll('div', {'class': 'rightNavContentOne'})
    
    #convert to a string as no tags to go on
    stats_string = '';
    for stat in stats_divs[1].find('p').contents:
        if stat.string != None:
            stats_string = stats_string  + stat.string.replace('/r', '')
            
    #split out by looking for new lines and colons        
    for stat in stats_string.split('\n'):
        key_value = stat.split(':')
        if len(key_value) == 2:
            if key_value[0] != 'Project Title':
                data[key_value[0]] = key_value[1]

    scraperwiki.datastore.save(['url',], data=data)
    

urls = get_urls()
for url in urls:
    try:
        save_page(url)
        print "SAVING PAGE:  " + url
        #be nice to the server
        time.sleep(2)
    except:
        print "failed to scrape: " + url
        pass
import time
import scraperwiki
from BeautifulSoup import BeautifulSoup


def get_urls():
    urls = []
    carry_on = True
    counter = 0
    while carry_on:
        starting_url = 'http://dmped.dc.gov/DC/DMPED/Projects/Development+Projects?renderPage=%d' % counter
        html = scraperwiki.scrape(starting_url)
        soup = BeautifulSoup(html)

        # use BeautifulSoup to get all <a href> tags to parse further
        project_divs = soup.findAll('div', {'class': 'dcEvent'}) 
        if project_divs:
            for project_div in project_divs:
                url = 'http://dmped.dc.gov' + project_div.find('a')['href']
                urls.append(url)
                print "GETTING PAGE:  " + url
            counter = counter + 1
            #carry_on = False #UNCOMMENT TO TEST
        else:
            carry_on = False
            print "STOPPING NOW."
        #be nice to the server
        time.sleep(2)
        
    return urls
    
def save_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    data = {}
    data['url'] = url

    #get title
    title = soup.find('h2', {'class': 'contentBodyTitle'}).string.replace('&nbsp;', '')
    data['title'] = title
    
    #get stats
    stats_divs = soup.find('div', {'class': 'rightNavContainerOne'}).findAll('div', {'class': 'rightNavContentOne'})
    
    #convert to a string as no tags to go on
    stats_string = '';
    for stat in stats_divs[1].find('p').contents:
        if stat.string != None:
            stats_string = stats_string  + stat.string.replace('/r', '')
            
    #split out by looking for new lines and colons        
    for stat in stats_string.split('\n'):
        key_value = stat.split(':')
        if len(key_value) == 2:
            if key_value[0] != 'Project Title':
                data[key_value[0]] = key_value[1]

    scraperwiki.datastore.save(['url',], data=data)
    

urls = get_urls()
for url in urls:
    try:
        save_page(url)
        print "SAVING PAGE:  " + url
        #be nice to the server
        time.sleep(2)
    except:
        print "failed to scrape: " + url
        pass
