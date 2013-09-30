###############################################################################
# This scraper was written to collect the reported crime listed for New York City
# and all of the individual precincts from the NYPD's website contained in the 
# pdf files. This only contains the reported crimes of murder, robbery, rape, burglary
# felony assault, grand larceny, and motor vehicle theft, nothing any more specific
# about crimes is available (besides different time periods). If you are interested 
# in older data by precinct, back as far to 2003 send me an email and I may be able
# to help, apwheele+NYPDcrimestats@gmail.com, data store collection began on August
# 17th, 2008
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['area','week','murder','rape','robbery','fa','burg','lar','mvt','volume'])

# scrape_table function: gets passed to an individual page to scrape
def scrape_table(soup_pdf):
    tds = soup_pdf.findAll('text') # get all the <text> tags
    tds_text = [None]*len(tds)
    for i in range(len(tds)): #changing my tags to the text within the tag
        tds_text[i] = tds[i].text
    data = {} #because all I have to go on is the relative location of numbers, I search for specific strings and then
              #take the number in the string afterwords, if the format of the pdf changes, theres a good chance this wont work
    murder_loc = tds_text.index('Murder') + 1
    data['murder'] = tds_text[murder_loc]
    rape_loc = tds_text.index('Rape') + 1
    data['rape'] = tds_text[rape_loc]
    rob_loc = tds_text.index('Robbery') + 1
    data['robbery'] = tds_text[rob_loc]
    fa_loc = tds_text.index('Fel. Assault') + 1
    data['fa'] = tds_text[fa_loc]
    burg_loc = tds_text.index('Burglary') + 1
    data['burg'] = tds_text[burg_loc]
    lar_loc = tds_text.index('Gr. Larceny') + 1
    data['lar'] = tds_text[lar_loc]
    mvt_loc = tds_text.index('G.L.A.') + 1
    data['mvt'] = tds_text[mvt_loc]
    data['volume'] = str(soup_pdf.find(text=re.compile('Volume')))
    data['week'] = str(soup_pdf.find(text=re.compile('Report Covering the Week'))) #im lazy and dont feel like parsing the field to return begin/end
    if tds[8].text == 'Patrol Borough': #this is because for the pdfs for the borough crime the relative location of the area name changes
        data['area'] = tds[9].text
    else:
        data['area'] = tds[8].text   
    scraperwiki.datastore.save(unique_keys=['area','week'],data=data)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# what I do is populate an array with all of the pdf links, and then loop through all of those links
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    find_link = soup.findAll(href=re.compile("/downloads/pdf/crime_statistics/"))
    next_link = [None]*(len(find_link))
    rep_link = [None]*(len(find_link))
    for i in range(len(find_link)):
        next_link[i] = find_link[i]['href']
        rep_link[i] = next_link[i].replace('../..','http://www.nyc.gov/html/nypd')
    for i in range(len(rep_link)):
        a = scraperwiki.scrape(rep_link[i]) #here I call my previously defined function to convert and scrape the pdf
        soup_pdf = BeautifulSoup(scraperwiki.pdftoxml(a))
        scrape_table(soup_pdf)
    
#here I put it all together and call it all at once, later I should insert assert statements 
#to prevent code from executing if illogical numbers occur
url = 'http://www.nyc.gov/html/nypd/html/crime_prevention/crime_statistics.shtml'
scrape_and_look_for_next_link(url)###############################################################################
# This scraper was written to collect the reported crime listed for New York City
# and all of the individual precincts from the NYPD's website contained in the 
# pdf files. This only contains the reported crimes of murder, robbery, rape, burglary
# felony assault, grand larceny, and motor vehicle theft, nothing any more specific
# about crimes is available (besides different time periods). If you are interested 
# in older data by precinct, back as far to 2003 send me an email and I may be able
# to help, apwheele+NYPDcrimestats@gmail.com, data store collection began on August
# 17th, 2008
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['area','week','murder','rape','robbery','fa','burg','lar','mvt','volume'])

# scrape_table function: gets passed to an individual page to scrape
def scrape_table(soup_pdf):
    tds = soup_pdf.findAll('text') # get all the <text> tags
    tds_text = [None]*len(tds)
    for i in range(len(tds)): #changing my tags to the text within the tag
        tds_text[i] = tds[i].text
    data = {} #because all I have to go on is the relative location of numbers, I search for specific strings and then
              #take the number in the string afterwords, if the format of the pdf changes, theres a good chance this wont work
    murder_loc = tds_text.index('Murder') + 1
    data['murder'] = tds_text[murder_loc]
    rape_loc = tds_text.index('Rape') + 1
    data['rape'] = tds_text[rape_loc]
    rob_loc = tds_text.index('Robbery') + 1
    data['robbery'] = tds_text[rob_loc]
    fa_loc = tds_text.index('Fel. Assault') + 1
    data['fa'] = tds_text[fa_loc]
    burg_loc = tds_text.index('Burglary') + 1
    data['burg'] = tds_text[burg_loc]
    lar_loc = tds_text.index('Gr. Larceny') + 1
    data['lar'] = tds_text[lar_loc]
    mvt_loc = tds_text.index('G.L.A.') + 1
    data['mvt'] = tds_text[mvt_loc]
    data['volume'] = str(soup_pdf.find(text=re.compile('Volume')))
    data['week'] = str(soup_pdf.find(text=re.compile('Report Covering the Week'))) #im lazy and dont feel like parsing the field to return begin/end
    if tds[8].text == 'Patrol Borough': #this is because for the pdfs for the borough crime the relative location of the area name changes
        data['area'] = tds[9].text
    else:
        data['area'] = tds[8].text   
    scraperwiki.datastore.save(unique_keys=['area','week'],data=data)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# what I do is populate an array with all of the pdf links, and then loop through all of those links
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    find_link = soup.findAll(href=re.compile("/downloads/pdf/crime_statistics/"))
    next_link = [None]*(len(find_link))
    rep_link = [None]*(len(find_link))
    for i in range(len(find_link)):
        next_link[i] = find_link[i]['href']
        rep_link[i] = next_link[i].replace('../..','http://www.nyc.gov/html/nypd')
    for i in range(len(rep_link)):
        a = scraperwiki.scrape(rep_link[i]) #here I call my previously defined function to convert and scrape the pdf
        soup_pdf = BeautifulSoup(scraperwiki.pdftoxml(a))
        scrape_table(soup_pdf)
    
#here I put it all together and call it all at once, later I should insert assert statements 
#to prevent code from executing if illogical numbers occur
url = 'http://www.nyc.gov/html/nypd/html/crime_prevention/crime_statistics.shtml'
scrape_and_look_for_next_link(url)