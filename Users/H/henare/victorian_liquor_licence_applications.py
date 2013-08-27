import scraperwiki
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

# The site errors when direct linking to anything but the home page
info_url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&WCU'
comment_url = info_url

def search_result_details(bar, regex):
    r = re.compile(regex)
    print type(bar)
    print type(r)
    foo = filter(r.search, bar)
    #return filter(r.search, result_details)[0].p.text

url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=search_licence_applications&WCU'

form_data = {
  'Submit': 'Submit Request',
  'licence_category': '312',
  'sort_by': 'BY.DSND LODGE.DATE BY PREMISES.RESID.SUBURB|RECEIVED DATE, SUBURB'
}

page_html = requests.post(url, data=form_data, verify=False).content
page = BeautifulSoup(page_html)

results = page.find_all(attrs='result')

for result in results:
    result_details = result.find_all(attrs='result-details')
    search_result_details(result_details, "Premises Address")
    
    application = {
        "council_reference": result.find(attrs='result-title').text.split()[0],
        "date_received": datetime.strptime(result_details[0].p.text, '%d/%m/%Y').strftime('%Y-%m-%d'),
        #"address": result_details[1].p.text,
        #"address": search_result_details(result_details, "Premises Address"),
        "description": result_details[2].p.text,
        "date_scraped": date.today(),
        "info_url": info_url,
        "comment_url": comment_url,
        # Non-PlanningAlerts data that might be interesting too:
        "licence_category": result_details[5].p.text,
        "licence_number": result_details[6].p.text,
        "demerit_points": result_details[7].p.text.split()[0]
    }
    
    scraperwiki.sqlite.save(unique_keys=["council_reference"], data=application)

import scraperwiki
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

# The site errors when direct linking to anything but the home page
info_url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&WCU'
comment_url = info_url

def search_result_details(bar, regex):
    r = re.compile(regex)
    print type(bar)
    print type(r)
    foo = filter(r.search, bar)
    #return filter(r.search, result_details)[0].p.text

url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=search_licence_applications&WCU'

form_data = {
  'Submit': 'Submit Request',
  'licence_category': '312',
  'sort_by': 'BY.DSND LODGE.DATE BY PREMISES.RESID.SUBURB|RECEIVED DATE, SUBURB'
}

page_html = requests.post(url, data=form_data, verify=False).content
page = BeautifulSoup(page_html)

results = page.find_all(attrs='result')

for result in results:
    result_details = result.find_all(attrs='result-details')
    search_result_details(result_details, "Premises Address")
    
    application = {
        "council_reference": result.find(attrs='result-title').text.split()[0],
        "date_received": datetime.strptime(result_details[0].p.text, '%d/%m/%Y').strftime('%Y-%m-%d'),
        #"address": result_details[1].p.text,
        #"address": search_result_details(result_details, "Premises Address"),
        "description": result_details[2].p.text,
        "date_scraped": date.today(),
        "info_url": info_url,
        "comment_url": comment_url,
        # Non-PlanningAlerts data that might be interesting too:
        "licence_category": result_details[5].p.text,
        "licence_number": result_details[6].p.text,
        "demerit_points": result_details[7].p.text.split()[0]
    }
    
    scraperwiki.sqlite.save(unique_keys=["council_reference"], data=application)

import scraperwiki
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

# The site errors when direct linking to anything but the home page
info_url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&WCU'
comment_url = info_url

def search_result_details(bar, regex):
    r = re.compile(regex)
    print type(bar)
    print type(r)
    foo = filter(r.search, bar)
    #return filter(r.search, result_details)[0].p.text

url = 'https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=search_licence_applications&WCU'

form_data = {
  'Submit': 'Submit Request',
  'licence_category': '312',
  'sort_by': 'BY.DSND LODGE.DATE BY PREMISES.RESID.SUBURB|RECEIVED DATE, SUBURB'
}

page_html = requests.post(url, data=form_data, verify=False).content
page = BeautifulSoup(page_html)

results = page.find_all(attrs='result')

for result in results:
    result_details = result.find_all(attrs='result-details')
    search_result_details(result_details, "Premises Address")
    
    application = {
        "council_reference": result.find(attrs='result-title').text.split()[0],
        "date_received": datetime.strptime(result_details[0].p.text, '%d/%m/%Y').strftime('%Y-%m-%d'),
        #"address": result_details[1].p.text,
        #"address": search_result_details(result_details, "Premises Address"),
        "description": result_details[2].p.text,
        "date_scraped": date.today(),
        "info_url": info_url,
        "comment_url": comment_url,
        # Non-PlanningAlerts data that might be interesting too:
        "licence_category": result_details[5].p.text,
        "licence_number": result_details[6].p.text,
        "demerit_points": result_details[7].p.text.split()[0]
    }
    
    scraperwiki.sqlite.save(unique_keys=["council_reference"], data=application)

