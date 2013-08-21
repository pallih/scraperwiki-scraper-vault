# Blank Python
from  lxml.html import document_fromstring , parse , submit_form
import scraperwiki
import re
from datetime import datetime
import time
import random
import mechanize, urllib, urllib2
import lxml.html
from BeautifulSoup import BeautifulSoup
import os

result= parse('http://api.digitaliser.dk/rest/resources/search?query=&firstResult=10&maxResults=100&tags=&classificationChoices=').getroot()

print result.text