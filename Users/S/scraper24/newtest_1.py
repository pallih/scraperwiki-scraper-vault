import urllib

import json

import csv

import re

from BeautifulSoup import BeautifulSoup



urls = [
    'http://www.baaa-acro.com/archives/1918.htm'
    ]

def saveData(output):
    filename = 'image-scraper'
    print "Writing CSV output to %s.csv" % filename
    csv_file = csv.writer(open('%s.csv' % filename, 'w'), delimiter=',')
    for line in output:
        csv_file.writerow(line.values())
    print "Done!"


output = []

for url in urls:
    print "Now scraping from %s..." % (url)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    for table in soup.findAll("table")[1:]:
        for tr in table.findAll("tr")[1:]:
            td = tr.findAll("td")
            data = [
                td[0].getText(),
                td[1].getText(),
                url.split('archives/1918.htm')[0] + str(td[2].find("img")).split('src="')[1].split('../')[1].split(' width')[0],
                td[3].getText(),
                url.split('archives/1918.htm')[0] + str(td[4].find("img")).split('src="')[1].split('../')[1].split(' width')[0],
                td[5].getText(),
                td[6].getText()
            ]
            print data
            #output.append(tr.getText().encode('ascii','ignore'))

saveData(output) #save all data for this year

print output
print "Successfully scraped all URLs"import urllib

import json

import csv

import re

from BeautifulSoup import BeautifulSoup



urls = [
    'http://www.baaa-acro.com/archives/1918.htm'
    ]

def saveData(output):
    filename = 'image-scraper'
    print "Writing CSV output to %s.csv" % filename
    csv_file = csv.writer(open('%s.csv' % filename, 'w'), delimiter=',')
    for line in output:
        csv_file.writerow(line.values())
    print "Done!"


output = []

for url in urls:
    print "Now scraping from %s..." % (url)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    for table in soup.findAll("table")[1:]:
        for tr in table.findAll("tr")[1:]:
            td = tr.findAll("td")
            data = [
                td[0].getText(),
                td[1].getText(),
                url.split('archives/1918.htm')[0] + str(td[2].find("img")).split('src="')[1].split('../')[1].split(' width')[0],
                td[3].getText(),
                url.split('archives/1918.htm')[0] + str(td[4].find("img")).split('src="')[1].split('../')[1].split(' width')[0],
                td[5].getText(),
                td[6].getText()
            ]
            print data
            #output.append(tr.getText().encode('ascii','ignore'))

saveData(output) #save all data for this year

print output
print "Successfully scraped all URLs"