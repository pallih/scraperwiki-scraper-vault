import scraperwiki
import re
import urllib2
from urlparse import urljoin
import lxml.html
import datetime

#date = datetime.datetime.now().date().strftime('%d-%b-%Y')
date = None
url = 'https://www.cas.dh.gov.uk/SearchAlerts.aspx'
data_rows = []
html = urllib2.urlopen(url).read()
page = lxml.html.fromstring(html)
rows = page.cssselect('tr.gridText')
for row in rows:
    data = {}
    data['id'] = row[0].text_content()
    a = row[1].cssselect('a')[0]
    data['link'] = urljoin(url, a.attrib.get('href'))
    data['short_title'] = a.text_content()
    data['when'] = row[3].text_content().strip()
    if date and not date == data['when']:
        print 'Skipping old content'
        continue

    def get_text_if(idfield, page, f=lambda x:x.text_content()):
        elem = page.cssselect(idfield)
        if len(elem) > 0:
            return f(elem[0])
        return ''

    detailpage = lxml.html.fromstring( urllib2.urlopen(data['link']).read() )
    data['title'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewTitle')[0].text_content()
    data['content'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewBroadcastContent')[0].text_content()
    data['originator'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewOriginatingEntity')[0].text_content()
    data['originator_name'] = get_text_if('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewOriginatorName', detailpage)
    data['additional_info'] = get_text_if('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewAdditionalInfo', detailpage)
    
    data_rows.append(data)
scraperwiki.sqlite.save(['id'], data_rows )
import scraperwiki
import re
import urllib2
from urlparse import urljoin
import lxml.html
import datetime

#date = datetime.datetime.now().date().strftime('%d-%b-%Y')
date = None
url = 'https://www.cas.dh.gov.uk/SearchAlerts.aspx'
data_rows = []
html = urllib2.urlopen(url).read()
page = lxml.html.fromstring(html)
rows = page.cssselect('tr.gridText')
for row in rows:
    data = {}
    data['id'] = row[0].text_content()
    a = row[1].cssselect('a')[0]
    data['link'] = urljoin(url, a.attrib.get('href'))
    data['short_title'] = a.text_content()
    data['when'] = row[3].text_content().strip()
    if date and not date == data['when']:
        print 'Skipping old content'
        continue

    def get_text_if(idfield, page, f=lambda x:x.text_content()):
        elem = page.cssselect(idfield)
        if len(elem) > 0:
            return f(elem[0])
        return ''

    detailpage = lxml.html.fromstring( urllib2.urlopen(data['link']).read() )
    data['title'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewTitle')[0].text_content()
    data['content'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewBroadcastContent')[0].text_content()
    data['originator'] = detailpage.cssselect('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewOriginatingEntity')[0].text_content()
    data['originator_name'] = get_text_if('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewOriginatorName', detailpage)
    data['additional_info'] = get_text_if('#ctl00_ContentPlaceHolder1_ucViewAlertDetails_lblViewAdditionalInfo', detailpage)
    
    data_rows.append(data)
scraperwiki.sqlite.save(['id'], data_rows )
