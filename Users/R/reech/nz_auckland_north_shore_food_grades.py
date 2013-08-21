#!/usr/bin/env python
# Scrape Auckland food ratings

#Albany,Bayswater,Bayview,Beach Haven,Belmont,Birkdale,Birkenhead,Browns Bay,Campbells Bay,Castor Bay,Chatswood,City Wide,Devonport,Fairview Heights,Forrest Hill,Glenfield,Greenhithe,Hauraki,Hillcrest,Long Bay,Lucas Heights,Mairangi Bay,Milford,Murrays Bay,Narrow Neck,Northcote,Northcote Point,Northcross,Oteha,Pinehill,Rosedale,Rothesay Bay,Schnapper Rock,Sunnynook,Takapuna,Torbay,Totara Vale,Unsworth Heights,Waiake,Wairau Valley,Windsor Park

# http://www.northshorecity.govt.nz/Services/OnlineServices/Pages/IFFoodgrade.aspx
import scraperwiki
from scrapemark import scrape
from datetime import datetime, timedelta
from dateutil import parser
import urllib, urllib2
import lxml.html
import json
import sys
from time import sleep
import mechanize
from random import randint

# Nasty Nasty  aspx
BASE_URL = 'http://www.northshorecity.govt.nz/Services/OnlineServices/Pages/IFFoodgrade.aspx' #'http://www.aucklandcity.govt.nz/council/services/foodsearch'#
# ABCDEXEMPT
GRADE_VALUES_FIELD = 'ctl00%24ContentAll%24SPWebPartManager1%24g_8dd2f599_502e_4b46_b6d1_3fbe43dcee16%24ctl00%24lstbxGrades'

# Nested forms break mechanize in this instance
def mech_scrape(url):
    
    print "Scraper %(url)s" % { 'url': url, }
    br = mechanize.Browser() # factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686;  en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    #print "Response :: "

    response = br.open(url)
    
    #print "Response :: "
    print response.read()
    print "All forms:", [ form.name  for form in br.forms() ]
    return

mech_scrape(BASE_URL)

