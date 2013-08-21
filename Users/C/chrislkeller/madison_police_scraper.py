import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup, Tag
import urllib
import urllib2
import re
import types
import time, datetime
from dateutil import parser

mech = Browser()
target_url = 'https://www.cityofmadison.com/police/newsroom/incidentreports/index.cfm?page=1&a=71'
target_page = mech.open(target_url)
target_html = target_page.read()
target_soup = BeautifulSoup(target_html, convertEntities=BeautifulSoup.HTML_ENTITIES)

print target_soup