import scraperwiki
import scrapemark
import feedparser
import csv
import re
import urllib2,sys
import requests
from BeautifulSoup import BeautifulSoup, NavigableString

applicants = ["Rexroth", "Linde"]


# project URL template: u'http://cordis.europa.eu/projects/rcn/105842_en.html


URL_1 = "http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=EN_PROJ&text=%28"
URL_2="%29&sort=all&querySummary=quick&fieldText=%28MATCH%7BCORDIS%2CWEBPAGESEUROPA%7D%3ASOURCE%29&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&descr="
URL_3 = ";%20Projects"


print "Number of searches: " + str(len(applicants))

# Open CSV file
with open ('output.csv', 'w') as csvfile: 
        csvwriter = csv.writer(open ('output.csv', 'a'))



for applicant in applicants:
    list_url = URL_1 + applicant + URL_2 + applicant + URL_3
    
    
    atom_feed = feedparser.parse(list_url)
    

    
    
    # list of titles and links and writing it into CSV
    number = 0
    
    print atom_feed.entries[(number)].title
    print atom_feed.entries[(number)].link
    csvwriter.writerow([atom_feed.entries[(number)].title] + [atom_feed.entries[(number)].link])
    print 'row %3d written to CSV' % number
    print "++++"
    
    while True:
        try:
            number = number + 1
    
            print atom_feed.entries[(number)].title
            print atom_feed.entries[(number)].link
            csvwriter.writerow([atom_feed.entries[(number)].title] + [atom_feed.entries[(number)].link])
            print 'row %3d written to CSV' % number
            print "++++"
    
        except IndexError:
            print 'All rows have been written to CSV'
            break 
    
    # Parsing HTML
    
    number = 0
    
    non_detail_url = atom_feed.entries[(number)].link
    html = urllib2.urlopen(non_detail_url).read()
    
    soup = BeautifulSoup(html)
    project_id = soup.find('input', attrs={'name':"REF"}).get('value')
    print project_id
    
    PROJECT_URL = "http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn=%(project_id)s"
    detail_url = PROJECT_URL % {'project_id': project_id}
    
    print detail_url
    
    
    details = requests.get(detail_url)
    detail_page = details.content
    
    content = BeautifulSoup(detail_page, convertEntities="html", smartQuotesTo="html", fromEncoding="utf-8")
    
    # extract content
    data_info = content.find(attrs={'class':'projdates'})
    data_coordinator = content.find(attrs={'class': 'projcoord'})
    data_details = content.find(attrs={'class': 'projdet'})
    data_participants = content.find(attrs={'class': 'participants'})
    data_footer = content.find(attrs={'id': 'recinfo'})
    
    print data_info
    print data_coordinator
    print data_details
    print data_participants
    print data_footer
import scraperwiki
import scrapemark
import feedparser
import csv
import re
import urllib2,sys
import requests
from BeautifulSoup import BeautifulSoup, NavigableString

applicants = ["Rexroth", "Linde"]


# project URL template: u'http://cordis.europa.eu/projects/rcn/105842_en.html


URL_1 = "http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=EN_PROJ&text=%28"
URL_2="%29&sort=all&querySummary=quick&fieldText=%28MATCH%7BCORDIS%2CWEBPAGESEUROPA%7D%3ASOURCE%29&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&descr="
URL_3 = ";%20Projects"


print "Number of searches: " + str(len(applicants))

# Open CSV file
with open ('output.csv', 'w') as csvfile: 
        csvwriter = csv.writer(open ('output.csv', 'a'))



for applicant in applicants:
    list_url = URL_1 + applicant + URL_2 + applicant + URL_3
    
    
    atom_feed = feedparser.parse(list_url)
    

    
    
    # list of titles and links and writing it into CSV
    number = 0
    
    print atom_feed.entries[(number)].title
    print atom_feed.entries[(number)].link
    csvwriter.writerow([atom_feed.entries[(number)].title] + [atom_feed.entries[(number)].link])
    print 'row %3d written to CSV' % number
    print "++++"
    
    while True:
        try:
            number = number + 1
    
            print atom_feed.entries[(number)].title
            print atom_feed.entries[(number)].link
            csvwriter.writerow([atom_feed.entries[(number)].title] + [atom_feed.entries[(number)].link])
            print 'row %3d written to CSV' % number
            print "++++"
    
        except IndexError:
            print 'All rows have been written to CSV'
            break 
    
    # Parsing HTML
    
    number = 0
    
    non_detail_url = atom_feed.entries[(number)].link
    html = urllib2.urlopen(non_detail_url).read()
    
    soup = BeautifulSoup(html)
    project_id = soup.find('input', attrs={'name':"REF"}).get('value')
    print project_id
    
    PROJECT_URL = "http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn=%(project_id)s"
    detail_url = PROJECT_URL % {'project_id': project_id}
    
    print detail_url
    
    
    details = requests.get(detail_url)
    detail_page = details.content
    
    content = BeautifulSoup(detail_page, convertEntities="html", smartQuotesTo="html", fromEncoding="utf-8")
    
    # extract content
    data_info = content.find(attrs={'class':'projdates'})
    data_coordinator = content.find(attrs={'class': 'projcoord'})
    data_details = content.find(attrs={'class': 'projdet'})
    data_participants = content.find(attrs={'class': 'participants'})
    data_footer = content.find(attrs={'id': 'recinfo'})
    
    print data_info
    print data_coordinator
    print data_details
    print data_participants
    print data_footer
