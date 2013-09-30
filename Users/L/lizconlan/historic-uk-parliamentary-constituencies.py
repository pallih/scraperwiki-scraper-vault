import scraperwiki
import logging
import time
from BeautifulSoup import BeautifulSoup

def get_data(url, tries=0):
    #scraperwiki.scrape seems to choke periodically, this retries it a few times before
    #giving up on it

    max = 5

    try:
        return scraperwiki.scrape(url,[],"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1")
    except:
        if tries >= max:
            raise
        tries += 1
        time.sleep(1)
        get_data(url, tries)

# retrieve a page
starting_url = 'http://en.wikipedia.org/wiki/Wikipedia:WikiProject_UK_Parliament_constituencies/Historic_constituency_names'
html = get_data(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('tr')


#set the order of the columns
if scraperwiki.sqlite.table_info(name="swdata") == []:
    scraperwiki.sqlite.execute("create table swdata (`name` string, `created` string, `abolished` string, `wikipedia_page` string)")


for tr in trs:
    td = tr.find('td')
    link = td.find('a')
    if link:
        follow = 'http://en.wikipedia.org' + link['href']
        cons_html = get_data(follow)
        cons_soup = BeautifulSoup(cons_html)
        data = cons_soup.find("table", { "class" : "infobox vcard" })
        if data:
            name = data.find("th", { "class" : "fn org" }).text
            dtstart = data.find("span", { "class" : "bday dtstart published updated" }).text
            dtend = data.find("span", { "class" : "dtend" })
            if dtend:
                dtend = dtend.text
            else:
                dtend = ""
            #print name + ', ' + dtstart + ' - ' + dtend
            #print data
            record = {"name" : name, "created" : dtstart, "abolished" : dtend, "wikipedia_page" : follow }
            # save records to the datastore
            scraperwiki.sqlite.save(["name"], record)
        else:
            if link['href'] != '/wiki/University_constituency':
                #no point logging this, it's a valid aggregator page but not helpful here
                logging.warn("Possible problem with wikipedia url %s", follow)
    import scraperwiki
import logging
import time
from BeautifulSoup import BeautifulSoup

def get_data(url, tries=0):
    #scraperwiki.scrape seems to choke periodically, this retries it a few times before
    #giving up on it

    max = 5

    try:
        return scraperwiki.scrape(url,[],"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1")
    except:
        if tries >= max:
            raise
        tries += 1
        time.sleep(1)
        get_data(url, tries)

# retrieve a page
starting_url = 'http://en.wikipedia.org/wiki/Wikipedia:WikiProject_UK_Parliament_constituencies/Historic_constituency_names'
html = get_data(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('tr')


#set the order of the columns
if scraperwiki.sqlite.table_info(name="swdata") == []:
    scraperwiki.sqlite.execute("create table swdata (`name` string, `created` string, `abolished` string, `wikipedia_page` string)")


for tr in trs:
    td = tr.find('td')
    link = td.find('a')
    if link:
        follow = 'http://en.wikipedia.org' + link['href']
        cons_html = get_data(follow)
        cons_soup = BeautifulSoup(cons_html)
        data = cons_soup.find("table", { "class" : "infobox vcard" })
        if data:
            name = data.find("th", { "class" : "fn org" }).text
            dtstart = data.find("span", { "class" : "bday dtstart published updated" }).text
            dtend = data.find("span", { "class" : "dtend" })
            if dtend:
                dtend = dtend.text
            else:
                dtend = ""
            #print name + ', ' + dtstart + ' - ' + dtend
            #print data
            record = {"name" : name, "created" : dtstart, "abolished" : dtend, "wikipedia_page" : follow }
            # save records to the datastore
            scraperwiki.sqlite.save(["name"], record)
        else:
            if link['href'] != '/wiki/University_constituency':
                #no point logging this, it's a valid aggregator page but not helpful here
                logging.warn("Possible problem with wikipedia url %s", follow)
    