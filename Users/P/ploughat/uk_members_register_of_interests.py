###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

record = {}
#record['source'] = 'Members Register of Interests'
record['date'] = '101206'
#base_url = 'http://www.publications.parliament.uk/pa/cm/cmregmem/100927/'
base_url = 'http://www.publications.parliament.uk/pa/cm/cmregmem/' + record['date'] + '/'
page1 = 'part1contents.htm'
#page2 = 'part2contents.htm'

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['MP', 'Interest Catetgory', 'Interest Detail'])


# scrape_table function: gets passed an individual page to scrape
def scrape_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    namestart = soup.find('p', attrs={"class" : "atozLinks"})
    #print namestart
    nameparas = namestart.findAllNext('p')
    for para in nameparas:
        #print para
        #print link['href']
        link = para.a
        scrape_mp(link['href'])


def scrape_mp(url):
    html = scraperwiki.scrape(base_url + url)
    soup = BeautifulSoup(html)
    #name = soup.h2.text
    #print name

    # extract name and constituency
    pat = re.compile('(.*?)\s*\((.*)\)')
    mat = pat.search(soup.h2.text)
    #record['name'] = soup.h2.text
    record['name'] = mat.group(1)
    #record['constuency'] = mat.group(2)

    # find category headings
    cats = soup.findAll('h3')
    for cat in cats:
        cattype = 0
        #if cat.text == '2. Remunerated employment, office, profession etc':
        record['category'] = cat.text
        nextNode = cat
        while True:
            if nextNode.nextSibling == None:
                break
            nextNode = nextNode.nextSibling
            if getattr(nextNode, 'name', None) == 'h3':
                break
            recordThisNode = False
            if cattype == 4 and getattr(nextNode, 'name', None) == 'p' and (nextNode.get('class', None) == 'indent' or nextNode.get('class', None) == 'indent2'):
                    # TODO: only record if a donor name is present and put it into organisation field
                    record['organisation'] = "Unknown"
                    recordThisNode = True;
            else:
                if getattr(nextNode, 'name', None) == 'p' and nextNode.get('class', None) == 'indent':
                    # TODO: would be good if we could make a guess at the company from the text
                    record['organisation'] = "Unknown"
                    recordThisNode = True;
            if recordThisNode==True:
                record['content'] = nextNode.text
                #print record ['name']
                #print record ['constuency']
                #print record['category']
                #print record['company']
                #print record['content']
                #print record['source']
                #print record['date']
                scraperwiki.datastore.save(["name", "content"] , record)

#nextNode = soup.find('p', {'class': 'top'})
#while True:
#    # process
#    nextNode = nextNode.nextSibling
#    if getattr(nextNode, 'name', None)  == 'p' and nextNode.get('class', None) == 'end':
#        break


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
scrape_link(base_url + page1 )
#scrape_link(base_url + 'part2contents.htm')


#worked for old format
def scrape_mp2(url):
    html = scraperwiki.scrape(base_url + url)
    soup = BeautifulSoup(html)
    name = soup.h2.text
    print name
    cat = soup.h3
    if cat != None:
        if cat.text == '2. Remunerated employment, office, profession etc':
            works = cat.findAllNext('p', attrs={"class" : "indent"})
            for work in works:
                print work.text

# worked for old format
# scrape_table function: gets passed an individual page to scrape
def scrape_link2(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    namestart = soup.find(text='Terms of Reference').findNext('p')
    links = namestart.findAllNext('a', href=True)
    for link in links:
        #print link
        #print link['href']
        scrape_mp(link['href'])


# scrape_table function: gets passed an individual page to scrape
#def scrape_link3(url):
#    html = scraperwiki.scrape(url)
#    soup = BeautifulSoup(html)
#    name1 = soup.find(text='Terms of Reference').findNext('p').a
#findNext('a')
#    print name1['href']




#def scrape_link2(url):
#    html = scraperwiki.scrape(url)
#    soup = BeautifulSoup(html)
#    paras = soup.findAll("p",)
#    name = 0
#    count = 0
#    for para in paras:
#        if count<20:
#            if (para.a!= None):
#                if name!=0:
#                    #print "got a link"
#                    #print para.a.contents
#                    scrape_mp(para.a[href])
#                    count += 1
#                else:
#                    #print para.a.contents 
#                    if para.a.string == "Terms of Reference":
#                        name = 1
#


    
        #    next
        # Set up our data record - we'll need it later
        #record = {}
        #table_cells = row.findAll("td")
        #if table_cells:
        #    record['Artist'] = table_cells[0].text
        #    record['Album'] = table_cells[1].text
        #    record['Released'] = table_cells[2].text
        #    record['Sales (m)'] = table_cells[4].text
            # Print out the data we've gathered
        #    print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        #    scraperwiki.datastore.save(["Artist"], record)
        

###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

record = {}
#record['source'] = 'Members Register of Interests'
record['date'] = '101206'
#base_url = 'http://www.publications.parliament.uk/pa/cm/cmregmem/100927/'
base_url = 'http://www.publications.parliament.uk/pa/cm/cmregmem/' + record['date'] + '/'
page1 = 'part1contents.htm'
#page2 = 'part2contents.htm'

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['MP', 'Interest Catetgory', 'Interest Detail'])


# scrape_table function: gets passed an individual page to scrape
def scrape_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    namestart = soup.find('p', attrs={"class" : "atozLinks"})
    #print namestart
    nameparas = namestart.findAllNext('p')
    for para in nameparas:
        #print para
        #print link['href']
        link = para.a
        scrape_mp(link['href'])


def scrape_mp(url):
    html = scraperwiki.scrape(base_url + url)
    soup = BeautifulSoup(html)
    #name = soup.h2.text
    #print name

    # extract name and constituency
    pat = re.compile('(.*?)\s*\((.*)\)')
    mat = pat.search(soup.h2.text)
    #record['name'] = soup.h2.text
    record['name'] = mat.group(1)
    #record['constuency'] = mat.group(2)

    # find category headings
    cats = soup.findAll('h3')
    for cat in cats:
        cattype = 0
        #if cat.text == '2. Remunerated employment, office, profession etc':
        record['category'] = cat.text
        nextNode = cat
        while True:
            if nextNode.nextSibling == None:
                break
            nextNode = nextNode.nextSibling
            if getattr(nextNode, 'name', None) == 'h3':
                break
            recordThisNode = False
            if cattype == 4 and getattr(nextNode, 'name', None) == 'p' and (nextNode.get('class', None) == 'indent' or nextNode.get('class', None) == 'indent2'):
                    # TODO: only record if a donor name is present and put it into organisation field
                    record['organisation'] = "Unknown"
                    recordThisNode = True;
            else:
                if getattr(nextNode, 'name', None) == 'p' and nextNode.get('class', None) == 'indent':
                    # TODO: would be good if we could make a guess at the company from the text
                    record['organisation'] = "Unknown"
                    recordThisNode = True;
            if recordThisNode==True:
                record['content'] = nextNode.text
                #print record ['name']
                #print record ['constuency']
                #print record['category']
                #print record['company']
                #print record['content']
                #print record['source']
                #print record['date']
                scraperwiki.datastore.save(["name", "content"] , record)

#nextNode = soup.find('p', {'class': 'top'})
#while True:
#    # process
#    nextNode = nextNode.nextSibling
#    if getattr(nextNode, 'name', None)  == 'p' and nextNode.get('class', None) == 'end':
#        break


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
scrape_link(base_url + page1 )
#scrape_link(base_url + 'part2contents.htm')


#worked for old format
def scrape_mp2(url):
    html = scraperwiki.scrape(base_url + url)
    soup = BeautifulSoup(html)
    name = soup.h2.text
    print name
    cat = soup.h3
    if cat != None:
        if cat.text == '2. Remunerated employment, office, profession etc':
            works = cat.findAllNext('p', attrs={"class" : "indent"})
            for work in works:
                print work.text

# worked for old format
# scrape_table function: gets passed an individual page to scrape
def scrape_link2(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    namestart = soup.find(text='Terms of Reference').findNext('p')
    links = namestart.findAllNext('a', href=True)
    for link in links:
        #print link
        #print link['href']
        scrape_mp(link['href'])


# scrape_table function: gets passed an individual page to scrape
#def scrape_link3(url):
#    html = scraperwiki.scrape(url)
#    soup = BeautifulSoup(html)
#    name1 = soup.find(text='Terms of Reference').findNext('p').a
#findNext('a')
#    print name1['href']




#def scrape_link2(url):
#    html = scraperwiki.scrape(url)
#    soup = BeautifulSoup(html)
#    paras = soup.findAll("p",)
#    name = 0
#    count = 0
#    for para in paras:
#        if count<20:
#            if (para.a!= None):
#                if name!=0:
#                    #print "got a link"
#                    #print para.a.contents
#                    scrape_mp(para.a[href])
#                    count += 1
#                else:
#                    #print para.a.contents 
#                    if para.a.string == "Terms of Reference":
#                        name = 1
#


    
        #    next
        # Set up our data record - we'll need it later
        #record = {}
        #table_cells = row.findAll("td")
        #if table_cells:
        #    record['Artist'] = table_cells[0].text
        #    record['Album'] = table_cells[1].text
        #    record['Released'] = table_cells[2].text
        #    record['Sales (m)'] = table_cells[4].text
            # Print out the data we've gathered
        #    print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        #    scraperwiki.datastore.save(["Artist"], record)
        

