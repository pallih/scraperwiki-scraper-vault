import scraperwiki
import BeautifulSoup
import datetime
import mechanize

from scraperwiki import sqlite

AMERICAN_DATE_FORMAT = "%m.%d.%y"
UK_DATE_FORMAT = "%d/%m/%Y"

#scraperwiki.metadata.save('data_columns', ['date', 'city', 'venue'])

#scrape page
browser = mechanize.Browser()
request = browser.open('http://www.benfolds.com/tour-dates')
pages = [BeautifulSoup.BeautifulSoup(request.read())]

while True:
    try:
        request = browser.follow_link(text_regex='next >*')
        pages.append(BeautifulSoup.BeautifulSoup(request.read()))
    except:
        break # No more pages

#find rows
for page in pages:
    tbody = page.find('tbody')
    for row in tbody.findAll('tr'):
        cells = row.findAll('td')
        
        date_string = cells[0].find('span').text.strip()
        date = datetime.datetime.strptime(date_string, AMERICAN_DATE_FORMAT)
        city = cells[1].find('a').text
        venue = cells[2].find('a').text
    
        data = {'date': date.strftime(UK_DATE_FORMAT), 'city': city, 'venue': venue}
        sqlite.save(unique_keys=['date'], data=data, date=date)
