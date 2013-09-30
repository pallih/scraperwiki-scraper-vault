import scraperwiki
#calls the scraperwiki library
from BeautifulSoup import BeautifulSoup 
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/2?printco=Forecast&area=Sutton%20Coldfield')
#creates variable html, and uses the method scrape to scrape the URL to it
print html
#displays html variable

soup = BeautifulSoup(html)
#creates variable soup & passing 'html' string to BeautifulSoup
days = soup.findAll('tr')
#creates 'days' variable & assigns each tr in soup to it using the findAll method

for day in days:
    if day['class'].find('day') == -1:
        continue
#loops (continue) while it doesn't find (-1, i.e. false) day mentioned in a class (when 1, i.e. true, then moves to next line)
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
#creates record dictionary with 3 attributes - day, summary & temp. Each has a default empty value
    tds = day.findAll('td')
#creates variable tds and assigns every td in day
    for abbr in tds[0].findAll('abbr'):
#creates abbr variable & finds every instance of abbr in first row of tds [0] because that's where the day always is
        record['day'] = abbr.text
#then assigns text contained within abbr tag (text is any display text contained within html tags) to day field of record variable
    for span in tds[2].findAll('span'):
#for every span in row 3 of the tds variable
        try:
            if span['class'].find('temp max') != -1:
#if the phrase 'temp max' exists in this class (!= -1 means NOT FALSE)
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
#assign value to temp max field ([:-6] REMOVES THE LAST 6 CHARS, i.e. degrees C]
        except:
                pass
        record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text
#again, passes all strong text within the <div> to the summary field
        print record, '------------'
#print record followed by (,) ----

    scraperwiki.datastore.save(["day"], record)
#indent 4 spaces to keep in line with for day in days above
import scraperwiki
#calls the scraperwiki library
from BeautifulSoup import BeautifulSoup 
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/2?printco=Forecast&area=Sutton%20Coldfield')
#creates variable html, and uses the method scrape to scrape the URL to it
print html
#displays html variable

soup = BeautifulSoup(html)
#creates variable soup & passing 'html' string to BeautifulSoup
days = soup.findAll('tr')
#creates 'days' variable & assigns each tr in soup to it using the findAll method

for day in days:
    if day['class'].find('day') == -1:
        continue
#loops (continue) while it doesn't find (-1, i.e. false) day mentioned in a class (when 1, i.e. true, then moves to next line)
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
#creates record dictionary with 3 attributes - day, summary & temp. Each has a default empty value
    tds = day.findAll('td')
#creates variable tds and assigns every td in day
    for abbr in tds[0].findAll('abbr'):
#creates abbr variable & finds every instance of abbr in first row of tds [0] because that's where the day always is
        record['day'] = abbr.text
#then assigns text contained within abbr tag (text is any display text contained within html tags) to day field of record variable
    for span in tds[2].findAll('span'):
#for every span in row 3 of the tds variable
        try:
            if span['class'].find('temp max') != -1:
#if the phrase 'temp max' exists in this class (!= -1 means NOT FALSE)
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
#assign value to temp max field ([:-6] REMOVES THE LAST 6 CHARS, i.e. degrees C]
        except:
                pass
        record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text
#again, passes all strong text within the <div> to the summary field
        print record, '------------'
#print record followed by (,) ----

    scraperwiki.datastore.save(["day"], record)
#indent 4 spaces to keep in line with for day in days above
import scraperwiki
#calls the scraperwiki library
from BeautifulSoup import BeautifulSoup 
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/2?printco=Forecast&area=Sutton%20Coldfield')
#creates variable html, and uses the method scrape to scrape the URL to it
print html
#displays html variable

soup = BeautifulSoup(html)
#creates variable soup & passing 'html' string to BeautifulSoup
days = soup.findAll('tr')
#creates 'days' variable & assigns each tr in soup to it using the findAll method

for day in days:
    if day['class'].find('day') == -1:
        continue
#loops (continue) while it doesn't find (-1, i.e. false) day mentioned in a class (when 1, i.e. true, then moves to next line)
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
#creates record dictionary with 3 attributes - day, summary & temp. Each has a default empty value
    tds = day.findAll('td')
#creates variable tds and assigns every td in day
    for abbr in tds[0].findAll('abbr'):
#creates abbr variable & finds every instance of abbr in first row of tds [0] because that's where the day always is
        record['day'] = abbr.text
#then assigns text contained within abbr tag (text is any display text contained within html tags) to day field of record variable
    for span in tds[2].findAll('span'):
#for every span in row 3 of the tds variable
        try:
            if span['class'].find('temp max') != -1:
#if the phrase 'temp max' exists in this class (!= -1 means NOT FALSE)
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
#assign value to temp max field ([:-6] REMOVES THE LAST 6 CHARS, i.e. degrees C]
        except:
                pass
        record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text
#again, passes all strong text within the <div> to the summary field
        print record, '------------'
#print record followed by (,) ----

    scraperwiki.datastore.save(["day"], record)
#indent 4 spaces to keep in line with for day in days above
import scraperwiki
#calls the scraperwiki library
from BeautifulSoup import BeautifulSoup 
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/2?printco=Forecast&area=Sutton%20Coldfield')
#creates variable html, and uses the method scrape to scrape the URL to it
print html
#displays html variable

soup = BeautifulSoup(html)
#creates variable soup & passing 'html' string to BeautifulSoup
days = soup.findAll('tr')
#creates 'days' variable & assigns each tr in soup to it using the findAll method

for day in days:
    if day['class'].find('day') == -1:
        continue
#loops (continue) while it doesn't find (-1, i.e. false) day mentioned in a class (when 1, i.e. true, then moves to next line)
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
#creates record dictionary with 3 attributes - day, summary & temp. Each has a default empty value
    tds = day.findAll('td')
#creates variable tds and assigns every td in day
    for abbr in tds[0].findAll('abbr'):
#creates abbr variable & finds every instance of abbr in first row of tds [0] because that's where the day always is
        record['day'] = abbr.text
#then assigns text contained within abbr tag (text is any display text contained within html tags) to day field of record variable
    for span in tds[2].findAll('span'):
#for every span in row 3 of the tds variable
        try:
            if span['class'].find('temp max') != -1:
#if the phrase 'temp max' exists in this class (!= -1 means NOT FALSE)
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
#assign value to temp max field ([:-6] REMOVES THE LAST 6 CHARS, i.e. degrees C]
        except:
                pass
        record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text
#again, passes all strong text within the <div> to the summary field
        print record, '------------'
#print record followed by (,) ----

    scraperwiki.datastore.save(["day"], record)
#indent 4 spaces to keep in line with for day in days above
import scraperwiki
#calls the scraperwiki library
from BeautifulSoup import BeautifulSoup 
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/2?printco=Forecast&area=Sutton%20Coldfield')
#creates variable html, and uses the method scrape to scrape the URL to it
print html
#displays html variable

soup = BeautifulSoup(html)
#creates variable soup & passing 'html' string to BeautifulSoup
days = soup.findAll('tr')
#creates 'days' variable & assigns each tr in soup to it using the findAll method

for day in days:
    if day['class'].find('day') == -1:
        continue
#loops (continue) while it doesn't find (-1, i.e. false) day mentioned in a class (when 1, i.e. true, then moves to next line)
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
#creates record dictionary with 3 attributes - day, summary & temp. Each has a default empty value
    tds = day.findAll('td')
#creates variable tds and assigns every td in day
    for abbr in tds[0].findAll('abbr'):
#creates abbr variable & finds every instance of abbr in first row of tds [0] because that's where the day always is
        record['day'] = abbr.text
#then assigns text contained within abbr tag (text is any display text contained within html tags) to day field of record variable
    for span in tds[2].findAll('span'):
#for every span in row 3 of the tds variable
        try:
            if span['class'].find('temp max') != -1:
#if the phrase 'temp max' exists in this class (!= -1 means NOT FALSE)
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
#assign value to temp max field ([:-6] REMOVES THE LAST 6 CHARS, i.e. degrees C]
        except:
                pass
        record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text
#again, passes all strong text within the <div> to the summary field
        print record, '------------'
#print record followed by (,) ----

    scraperwiki.datastore.save(["day"], record)
#indent 4 spaces to keep in line with for day in days above
