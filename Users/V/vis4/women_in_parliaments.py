import scraperwiki
# this is not really ported to scraperwiki yet
# (the scraper tries to write the data into files)

from bs4 import BeautifulSoup
import requests
import re

# load archive index
base = 'http://www.ipu.org'
url = base + '/wmn-e/classif-arc.htm'


soup = BeautifulSoup(requests.get(url).text)

lyr = 0

countries = {}
years = []

for a in soup.body.center.table.findAll('tr')[2].findAll('a'):
    url = a['href']

    # extract the two-diget year from the url
    yr = url[22:24]

    # we only want to store one record per year, so we check
    # whether the year has changed
    if yr != lyr:
        lyr = yr
        if int(yr) < 50:
            year = '20' + yr
        else:
            year = '19' + yr
        years.append(year)
        soup2 = BeautifulSoup(requests.get(base + url).text)
        table = soup2.find('table', {'class': 'data'})
        if table is None:
            table = soup2.find('table', {'border': '1'})
        if table is None:
            print url
            exit()
        trs = table.findAll('tr', {'bgcolor': '#FFFFFF'})
        if len(trs) == 0:
            trs = table.findAll('tr')[2:]
        for tr in trs:
            tds = tr.findAll('td')
            country = tds[1].text
            # remove footnotes and trailing spaces
            country = re.sub('[\d\*]', '', country).strip()
            seats = tds[3].text.strip()
            women = tds[4].text.strip()
            rate = tds[5].text.strip()
            if rate[-1] == '%':
                rate = rate[:-1]
            if country not in countries:
                countries[country] = {}
            scraperwiki.sqlite.save(["country", "year"], dict(country=country, year=year, seats=seats, women=women, rate=rate))


