# http://www.ncil.org.uk/categoryid21.html

import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import time

start_url = "http://www.ncil.org.uk/show.php?contentid=95&q=&type=0&area=0&categoryid=21"


def scrape_link_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    content = soup.find('div', {'id' : 'contentcontainer' })
    #content_stuff = soup.findAll(text=True)
    link = content.findAll('a')
    for a in link[3:]:
        url= a['href']
        #print a
        scrape_detail(url)

def scrape_detail(url):
    seen_before = scraperwiki.metadata.get(url)
    if seen_before is not None:
        print "Seen before - skip: " + url
        return
    else:
        details = {}
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
        content = soup.find('div', {'id' : 'contentcontainer' })
        name = content.h3
        print "**** processing: " + name.text + ' - url: ' + url
    
    
        text = content(text=True)
        #remove newlines
        text = map(str.strip, text)

        contact1_name = re.sub("&nbsp;","",text[14])[:-3]
        contact1_title = text[15]
        contact2_name = re.sub("&nbsp;","",text[18])[:-3]
        contact2_title = text[19]

        next = content.findAll('p')

        address = next[2](text=True)[1:] 
        address = map(str.strip, address)
        address = " ".join(address)

        #extract postcode and geocode for maps
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    
        contact = next[3](text=True)
        contact = map(str.strip, contact)
        count = len(contact)

        #these if statements are lame checks for 3 various cases (happens when email and web are empty) - this can be done better, but is sufficient for now... 

        if count == 16:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[15]))
        if count == 14:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[13]))
        else:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[14]))        
    
        details['name'] = name.text
        details['contact1_name'] = contact1_name
        details['contact1_title'] = contact1_title
        details['contact2_name'] = contact2_name
        details['contact2_title'] = contact2_title
        details['address'] = address
        details['telephone'] = telephone
        details['fax'] = fax
        details['minicom'] = minicom
        details['email'] = email
        details['web'] = web
        details['postcode'] = postcode
        details['latlng'] = latlng
    
        #save url as metadata so we can check if it´s been done and then skip ... needs to be done as a "blocked" error keeps coming up:
        #The link http://www.ncil.org.uk/show.php?contentid=98&type= has been blocked. Click here for details.
        #Finished: 626 seconds elapsed, 30 CPU seconds used

        #This is bad since on a re-run old items are not checked for updates - maybe if it's possible to delete metadata at some interval?
        #Or code some time check for the metadata ... is the metadata timestamped? Or maybe store the url as data and check last scraped ...

        scraperwiki.metadata.save(url,"1")
        scraperwiki.datastore.save(["name","telephone"], details, latlng=(latlng))
        time.sleep(0.5)

scrape_link_list(start_url)
# http://www.ncil.org.uk/categoryid21.html

import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import time

start_url = "http://www.ncil.org.uk/show.php?contentid=95&q=&type=0&area=0&categoryid=21"


def scrape_link_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    content = soup.find('div', {'id' : 'contentcontainer' })
    #content_stuff = soup.findAll(text=True)
    link = content.findAll('a')
    for a in link[3:]:
        url= a['href']
        #print a
        scrape_detail(url)

def scrape_detail(url):
    seen_before = scraperwiki.metadata.get(url)
    if seen_before is not None:
        print "Seen before - skip: " + url
        return
    else:
        details = {}
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()
        content = soup.find('div', {'id' : 'contentcontainer' })
        name = content.h3
        print "**** processing: " + name.text + ' - url: ' + url
    
    
        text = content(text=True)
        #remove newlines
        text = map(str.strip, text)

        contact1_name = re.sub("&nbsp;","",text[14])[:-3]
        contact1_title = text[15]
        contact2_name = re.sub("&nbsp;","",text[18])[:-3]
        contact2_title = text[19]

        next = content.findAll('p')

        address = next[2](text=True)[1:] 
        address = map(str.strip, address)
        address = " ".join(address)

        #extract postcode and geocode for maps
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    
        contact = next[3](text=True)
        contact = map(str.strip, contact)
        count = len(contact)

        #these if statements are lame checks for 3 various cases (happens when email and web are empty) - this can be done better, but is sufficient for now... 

        if count == 16:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[15]))
        if count == 14:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[13]))
        else:
            telephone = re.sub("&nbsp;","",contact[1])
            fax = re.sub("&nbsp;","",contact[4])
            minicom = re.sub("&nbsp;","",contact[7])
            email = re.sub("&nbsp;","",contact[11])
            web = re.sub("&nbsp;"," ",str(contact[14]))        
    
        details['name'] = name.text
        details['contact1_name'] = contact1_name
        details['contact1_title'] = contact1_title
        details['contact2_name'] = contact2_name
        details['contact2_title'] = contact2_title
        details['address'] = address
        details['telephone'] = telephone
        details['fax'] = fax
        details['minicom'] = minicom
        details['email'] = email
        details['web'] = web
        details['postcode'] = postcode
        details['latlng'] = latlng
    
        #save url as metadata so we can check if it´s been done and then skip ... needs to be done as a "blocked" error keeps coming up:
        #The link http://www.ncil.org.uk/show.php?contentid=98&type= has been blocked. Click here for details.
        #Finished: 626 seconds elapsed, 30 CPU seconds used

        #This is bad since on a re-run old items are not checked for updates - maybe if it's possible to delete metadata at some interval?
        #Or code some time check for the metadata ... is the metadata timestamped? Or maybe store the url as data and check last scraped ...

        scraperwiki.metadata.save(url,"1")
        scraperwiki.datastore.save(["name","telephone"], details, latlng=(latlng))
        time.sleep(0.5)

scrape_link_list(start_url)
