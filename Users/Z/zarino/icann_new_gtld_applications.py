import scraperwiki
import requests
import lxml.html
import re

def td_text(tr, i):
    if tr.cssselect('td')[i].text != '-':
        return re.sub(r'\r\n\s+', ' ', tr.cssselect('td')[i].text)
    else:
        return None;

# pretty screenshot
requests.get('http://newgtlds.icann.org/en/program-status/application-results/strings-1200utc-13jun12-en')

applications = []

html = requests.get('http://newgtlds-cloudfront.icann.org/sites/default/files/reveal/strings-1200utc-13jun12-en.html')
dom = lxml.html.fromstring(html.text)

for tr in dom.cssselect('tbody tr'):
    applications.append({
        'gtld': td_text(tr, 0),
        'applicant': td_text(tr, 1),
        'location': td_text(tr, 2),
        'community': td_text(tr, 3),
        'geographic': td_text(tr, 4),
        'primary_contact': td_text(tr, 5),
        'email': td_text(tr, 6),
        'application_id': td_text(tr, 7)
    })

scraperwiki.sqlite.save(['application_id'], applications, 'applications')import scraperwiki
import requests
import lxml.html
import re

def td_text(tr, i):
    if tr.cssselect('td')[i].text != '-':
        return re.sub(r'\r\n\s+', ' ', tr.cssselect('td')[i].text)
    else:
        return None;

# pretty screenshot
requests.get('http://newgtlds.icann.org/en/program-status/application-results/strings-1200utc-13jun12-en')

applications = []

html = requests.get('http://newgtlds-cloudfront.icann.org/sites/default/files/reveal/strings-1200utc-13jun12-en.html')
dom = lxml.html.fromstring(html.text)

for tr in dom.cssselect('tbody tr'):
    applications.append({
        'gtld': td_text(tr, 0),
        'applicant': td_text(tr, 1),
        'location': td_text(tr, 2),
        'community': td_text(tr, 3),
        'geographic': td_text(tr, 4),
        'primary_contact': td_text(tr, 5),
        'email': td_text(tr, 6),
        'application_id': td_text(tr, 7)
    })

scraperwiki.sqlite.save(['application_id'], applications, 'applications')