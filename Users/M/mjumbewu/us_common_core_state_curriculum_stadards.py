###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

standard = scraperwiki.scrape('http://www.pacode.com/secure/data/022/chapter4/chap4toc.html')
soup = BeautifulSoup(standard)

headers = soup.findAll('h1')
for header in headers:
    sub = header.find('sub')
    if sub:
        category_code = sub.text
        category = header.text[:-len(category_code)].strip()
        descriptions = []
        
        current_tag = header
        while True:
            next_tag = current_tag.findNextSibling(re.compile('^[ph].?$')) # stuff that has one or two charachters, and starts with p or h
            print current_tag, next_tag
            current_tag = next_tag
            
            if not current_tag:
                break
            if current_tag.name.lower() != 'p':
                break
            
            inner_i = current_tag.find('i')

            if not inner_i:
                continue
            
            descriptions.append(inner_i.text)
        
        print category
        print category_code
        print descriptions
###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

standard = scraperwiki.scrape('http://www.pacode.com/secure/data/022/chapter4/chap4toc.html')
soup = BeautifulSoup(standard)

headers = soup.findAll('h1')
for header in headers:
    sub = header.find('sub')
    if sub:
        category_code = sub.text
        category = header.text[:-len(category_code)].strip()
        descriptions = []
        
        current_tag = header
        while True:
            next_tag = current_tag.findNextSibling(re.compile('^[ph].?$')) # stuff that has one or two charachters, and starts with p or h
            print current_tag, next_tag
            current_tag = next_tag
            
            if not current_tag:
                break
            if current_tag.name.lower() != 'p':
                break
            
            inner_i = current_tag.find('i')

            if not inner_i:
                continue
            
            descriptions.append(inner_i.text)
        
        print category
        print category_code
        print descriptions
