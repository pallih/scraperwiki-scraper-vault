import re
import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

base_url = "http://www.libdems.org.uk/%s"
candidate_list_url = base_url % "parliamentary_candidates.aspx?show=Candidates&pgNo=%s"
limit = 121

def scrape_candidate_details(href):
    """Gets the details about each candidate"""
    data = {}
    html = scraperwiki.scrape(base_url % href.replace("amp;",""))
    page = BeautifulSoup.BeautifulSoup(html)
    #The heading contains the name
    heading = page.find('div', {'id': 'divHeading'})
    data['name'] = heading.text.split(' &ndash;')[0]
    constituency = page.find('div', {'id': 'divConstituencyContactInfo'}).findAll('a')
    try:
        data['constituency'] = constituency[0].text
    except IndexError:
        constituency = page.find('div', {'id': 'divIntroduction'}).findAll('a')
        to_save = ""
        for link in constituency:
            if link.text != "":
                to_save = link.text
        data['constituency'] = to_save
    #Each candidate has AboutMe section.
    about = page.find('div', {'id': 'divAboutMe'})
    for table in about.findAll('table'):
        for row in table.findAll('tr'):
            data[row.find('th').text.replace(':', '')] = row.find('td').text
    #Extracts the candidates bio
    bio = page.find('div', {'id':'divBiography'})
    bio_text=[]
    for para in bio.findAll('p'):
        bio_text.append(para.text)
    data['bio'] = "\n".join(bio_text)
    #Get the contact info for each candidate
    contact = page.find('div', {'id':'divIndividualContactInfo'})
    for address in contact.findAll('ul', 'address'):
        to_store = []
        for line in address.findAll('li'):
            to_store.append(line.text)
        data['address'] = ', '.join(to_store)
    links = contact.findAll('a')
    if len(links) > 0:
        if len(links) == 2:
            data['email'] = links[0]['href'].replace('mailto:', '')
            data['website'] = links[1]['href']
        else:
            data['email'] = links[0]['href'].replace('mailto:', '')
    #Use re to get telephone number        
    m = re.search("<strong>Telephone:</strong>(.*)<br /><strong>", str(contact))   
    if m is not None:
        data['telephone'] = m.group(1) 
    datastore.save (unique_keys = ['constituency'], data = data)      
    
def scrape_page(the_page):
    """Gets the link to the page about each candidate"""
    for item in the_page.findAll('div', 'divWhoWeAreItem'):
        links = item.findAll('a')
        scrape_candidate_details(str(links[0]['href']))

for i in xrange(0, limit):
    #Parses the multiple pages that contain candidates
    html = scraperwiki.scrape(candidate_list_url % i)
    page = BeautifulSoup.BeautifulSoup(html)
    scrape_page(page)
import re
import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

base_url = "http://www.libdems.org.uk/%s"
candidate_list_url = base_url % "parliamentary_candidates.aspx?show=Candidates&pgNo=%s"
limit = 121

def scrape_candidate_details(href):
    """Gets the details about each candidate"""
    data = {}
    html = scraperwiki.scrape(base_url % href.replace("amp;",""))
    page = BeautifulSoup.BeautifulSoup(html)
    #The heading contains the name
    heading = page.find('div', {'id': 'divHeading'})
    data['name'] = heading.text.split(' &ndash;')[0]
    constituency = page.find('div', {'id': 'divConstituencyContactInfo'}).findAll('a')
    try:
        data['constituency'] = constituency[0].text
    except IndexError:
        constituency = page.find('div', {'id': 'divIntroduction'}).findAll('a')
        to_save = ""
        for link in constituency:
            if link.text != "":
                to_save = link.text
        data['constituency'] = to_save
    #Each candidate has AboutMe section.
    about = page.find('div', {'id': 'divAboutMe'})
    for table in about.findAll('table'):
        for row in table.findAll('tr'):
            data[row.find('th').text.replace(':', '')] = row.find('td').text
    #Extracts the candidates bio
    bio = page.find('div', {'id':'divBiography'})
    bio_text=[]
    for para in bio.findAll('p'):
        bio_text.append(para.text)
    data['bio'] = "\n".join(bio_text)
    #Get the contact info for each candidate
    contact = page.find('div', {'id':'divIndividualContactInfo'})
    for address in contact.findAll('ul', 'address'):
        to_store = []
        for line in address.findAll('li'):
            to_store.append(line.text)
        data['address'] = ', '.join(to_store)
    links = contact.findAll('a')
    if len(links) > 0:
        if len(links) == 2:
            data['email'] = links[0]['href'].replace('mailto:', '')
            data['website'] = links[1]['href']
        else:
            data['email'] = links[0]['href'].replace('mailto:', '')
    #Use re to get telephone number        
    m = re.search("<strong>Telephone:</strong>(.*)<br /><strong>", str(contact))   
    if m is not None:
        data['telephone'] = m.group(1) 
    datastore.save (unique_keys = ['constituency'], data = data)      
    
def scrape_page(the_page):
    """Gets the link to the page about each candidate"""
    for item in the_page.findAll('div', 'divWhoWeAreItem'):
        links = item.findAll('a')
        scrape_candidate_details(str(links[0]['href']))

for i in xrange(0, limit):
    #Parses the multiple pages that contain candidates
    html = scraperwiki.scrape(candidate_list_url % i)
    page = BeautifulSoup.BeautifulSoup(html)
    scrape_page(page)
