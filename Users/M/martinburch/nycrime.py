###############################################################################
# This scraper was written to collect the reported crime listed for New York City
# and all of the individual precincts from the NYPD's website contained in the 
# pdf files.
# This scraper is based on an earlier scraper by Andrew Wheeler.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

def precinct_number(area):
    if (area == "Central Park Precinct"):
        area = "22nd Precinct"
    if (area == "Midtown Precinct South"):
        area = "14th Precinct"
    if (area == "Midtown Precinct North"):
        area = "18th Precinct"
    for i in range(len(area)):
        if area[i].isdigit() == False:
            if i > 0:
                return int(area[0:i])
            else:
                break
    return ""

#This commented section imports historical numbers from Andy's scraper


scraperwiki.sqlite.attach("current-week-reported-crime-city-wide-and-for-prec", "src")

'''
# Get one week of data for testing purposes (cmb)
results = scraperwiki.sqlite.select("`area`, `week`, `murder`, `rape`, `robbery`, `fa` as `felony_assault`, `burg` as `burglary`, `lar` as `grand_larceny`, `mvt` as `grand_larceny_auto`, `volume` as `edition` FROM src.swdata")

for result in results:
    dates = result['week'].split() #Report Covering the Week <start> Through <end>
    result['start_date'] = dates[4]
    result['end_date'] = dates[6]
    del result['week']
    result['precinct'] = precinct_number(result['area'])
    print result

scraperwiki.sqlite.save(unique_keys=['area','end_date'],data=results,table_name="CrimeStatistics")
'''


# define the order our columns are displayed in the datastore
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `CrimeStatistics` (`edition` text ,`area` text,`start_date` text,`end_date` text,`murder` integer,`rape` integer,`robbery` integer,`felony_assault` integer,`burglary` integer,`grand_larceny` integer,`grand_larceny_auto` integer,`petit_larceny` integer,`misdemeanor_assault` integer,`misdemeanor_sex_crimes` integer,`shooting_victim` integer,`shooting_incident` integer)")

#If this is the first PDF, update the current week in the database, if necessary
global first
first = True

def string_cleaner(data):
    data = data.split()[0].replace(",","")
    return data

# scrape_table function: gets passed to an individual page to scrape
def scrape_table(soup_pdf):
    global first
    tds = soup_pdf.findAll('text') # get all the <text> tags
    tds_text = [None]*len(tds)
    for i in range(len(tds)): #changing my tags to the text within the tag
        tds_text[i] = tds[i].text
    data = {} #because all I have to go on is the relative location of numbers, I search for specific strings and then
              #take the number in the string afterwords, if the format of the pdf changes, theres a good chance this wont work

    data['murder'] = string_cleaner(tds_text[tds_text.index('Murder') + 1])
    data['rape'] = string_cleaner(tds_text[tds_text.index('Rape') + 1])
    data['robbery'] = string_cleaner(tds_text[tds_text.index('Robbery') + 1])
    data['felony_assault'] = string_cleaner(tds_text[tds_text.index('Fel. Assault') + 1])
    data['burglary'] = string_cleaner(tds_text[tds_text.index('Burglary') + 1])
    data['grand_larceny'] = string_cleaner(tds_text[tds_text.index('Gr. Larceny') + 1])
    data['grand_larceny_auto'] = string_cleaner(tds_text[tds_text.index('G.L.A.') + 1])
    data['petit_larceny'] = string_cleaner(tds_text[tds_text.index('Petit Larceny') + 1])
    data['misdemeanor_assault'] = string_cleaner(tds_text[tds_text.index('Misd. Assault') + 1])
    data['misdemeanor_sex_crimes'] = string_cleaner(tds_text[tds_text.index('Misd. Sex Crimes') + 1])
    #data['shooting_victim'] = string_cleaner(tds_text[tds_text.index('Shooting Vic.') + 1])
    #data['shooting_incident'] = string_cleaner(tds_text[tds_text.index('Shooting Inc.') + 1])

    data['edition'] = str(soup_pdf.find(text=re.compile('Volume')))
    dates = str(soup_pdf.find(text=re.compile('Report Covering the Week'))).split() #Report Covering the Week <start> Through <end>
    data['start_date'] = dates[4]
    data['end_date'] = dates[6]
    if tds[8].text == 'Patrol Borough': #this is because for the pdfs for the borough crime the relative location of the area name changes
        data['area'] = tds[9].text
    else:
        data['area'] = tds[8].text
    data['precinct'] = precinct_number(data['area'])

    scraperwiki.sqlite.save(unique_keys=['area','end_date'],data=data,table_name="CrimeStatistics")
    
    # If this is the first time though the loop
    if first == True:
        first = False
        # Update the information about the scrape
        stored_end_date = scraperwiki.sqlite.get_var('current_end_date')
        if stored_end_date != data['end_date']:
            scraperwiki.sqlite.save_var('previous_end_date', stored_end_date)
            scraperwiki.sqlite.save_var('current_end_date', data['end_date'])
    
        
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
    
#here I put it all together and call it all at once
url = 'http://www.nyc.gov/html/nypd/html/crime_prevention/crime_statistics.shtml'
scrape_and_look_for_next_link(url)

'''
#Test one PDF - convert and scrape the pdf
#a = scraperwiki.scrape("http://www.nyc.gov/html/nypd/downloads/pdf/crime_statistics/cscity.pdf") #the citywide numbers
a = scraperwiki.scrape("http://www.nyc.gov/html/nypd/downloads/pdf/crime_statistics/cs001pct.pdf") # precinct one
soup_pdf = BeautifulSoup(scraperwiki.pdftoxml(a))
scrape_table(soup_pdf)
'''