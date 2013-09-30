import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.workinstartups.com/job-board/jobs"
root = lxml.html.fromstring(scraperwiki.scrape(url))
jobs = {}

for job in root.cssselect('ul.job-list li'):
  

  line = job.text_content()
  array = line.split()
  company = array[-4]
  for x in array[-5::-1]:
    if x != 'at':
      company = x + " " + company
    else:
      break
  jobs['company'] = company
  jobs['date'] = job.cssselect('span.time-posted')[0].text_content()
  jobs['link'] = job.cssselect('a.job-link')[0].attrib['href']
  jobs['title'] = job.cssselect('a.job-link')[0].text
  scraperwiki.sqlite.save(['link'],jobs)
  

  
  
  
  
  
    







import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.workinstartups.com/job-board/jobs"
root = lxml.html.fromstring(scraperwiki.scrape(url))
jobs = {}

for job in root.cssselect('ul.job-list li'):
  

  line = job.text_content()
  array = line.split()
  company = array[-4]
  for x in array[-5::-1]:
    if x != 'at':
      company = x + " " + company
    else:
      break
  jobs['company'] = company
  jobs['date'] = job.cssselect('span.time-posted')[0].text_content()
  jobs['link'] = job.cssselect('a.job-link')[0].attrib['href']
  jobs['title'] = job.cssselect('a.job-link')[0].text
  scraperwiki.sqlite.save(['link'],jobs)
  

  
  
  
  
  
    







