'''
This is a Python template for a Sunlight Labs Great American Scraper Project
http://services.sunlightlabs.com/gasp/legislators/
'''

import re
import scraperwiki
from lxml.html import defs
from lxml.html.clean import Cleaner
from dateutil.parser import parse
from pyquery import PyQuery as pq
from time import sleep

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper('b673f984f7884d40a85c587a19fa1be9', 'M000934')

BASE_URL = 'http://moran.senate.gov/public/index.cfm/'
ALLOWED_TAGS = ['a', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'img', 'ol', 'ul', 'li']
BLOCK_TAGS = ['p', 'div']
ATTR_WHITELIST = ['src', 'alt', 'href', 'rowspan', 'colspan']

class AttrWhitelistCleaner(Cleaner):
    """An HTML Cleaner that can use an attribute whitelist.  Defaults to using
    the attributes that are whitelisted by default with ``safe_attrs_only``
    turned on."""

    def __init__(self, **kw):
        self.attr_whitelist = kw.pop('attr_whitelist', set(defs.safe_attrs))
        super(AttrWhitelistCleaner, self).__init__(**kw)

    def __call__(self, doc):
        self.safe_attrs_only = False
        super(AttrWhitelistCleaner, self).__call__(doc)
        if hasattr(doc, 'getroot'):
            doc = doc.getroot()

        whitelist = self.attr_whitelist
        for el in doc.iter():
            attrib = el.attrib
            for aname in attrib.keys():
                if aname not in whitelist:
                    del attrib[aname]

cleaner = AttrWhitelistCleaner(attr_whitelist=set(ATTR_WHITELIST), allow_tags=set(ALLOWED_TAGS + BLOCK_TAGS), remove_unknown_tags=False)

def _format_phone(string):
    pat = re.compile(r'[()\- ]')
    parts = pat.split(string)
    return '-'.join([part for part in parts if part])

def _extract_date_from(html):
    return parse(pq(html).find('h4.date').text())

def _extract_title_from(html):
    return pq(html).find('h1.title').text()


def _readable(html):
    try:
        html = cleaner.clean_html(unicode(html))
        html = re.sub(r'[\r\n\t]', '', cleaner.clean_html(unicode(html)))
        html = re.sub(r'[ ]+', ' ', html)
        html = html.replace('</p>', "\n\n")
        html = re.sub(r'</?(div|p)>', '', html)
    except:
        pass
    return html.encode('ascii', 'xmlcharrefreplace')

def scrape_issues():
    page = pq(scraperwiki.scrape(BASE_URL + 'issues'))
    for html in page.find('.table-of-contents ul li'):
        title = content = el = None
        el = pq(html)
        title = el.find('h2 a').text()
        content = el.find('div.abstract').html()
        try:
            content_url = '%s%s' % (BASE_URL, el.find('a.read-more').attr('href'))
            content = pq(scraperwiki.scrape(content_url)).find('div.article').html()
        except:
            pass
        gasp.add_issue(title, _readable(content))

def scrape_bio():
    page = pq(scraperwiki.scrape(BASE_URL + 'biography'))
    content = _readable(page.find('#copy .article'))
    gasp.add_biography(content)

def scrape_offices():
    page = pq(scraperwiki.scrape(BASE_URL + 'contact-info'))
    for office in page.find('.article'):
        try:
            office = pq(office).find('#pittsburgOffice').remove().end().html()
        except:
            pass
        phone = fax = ''
        address = []
        office = pq(office).find('.header').remove().end().html().strip()
        office = pq(re.sub(r'<br ?/>', "\n\n", office)).text().encode('ascii', 'xmlcharrefreplace')
        for line in office.split("\n\n"):
            line = line.strip()
            if line.lower().startswith('phone:'):
                phone = _format_phone(line.lower().strip('phone: '))
            elif line.lower().startswith('fax:'):
                fax = _format_phone(line.lower().strip('fax: '))
            elif line.strip().startswith('*'):
                continue    
            else:
                address.append(line)

        gasp.add_office("\n\n".join(address), phone, fax)

def scrape_press_releases():
    releases_page = pq(scraperwiki.scrape(BASE_URL + 'news-releases'))
    for row in releases_page.find('.recordListTitle'):
        sleep(1)

        title = ''
        date = None
        content = ''
        attachments = []

        links = pq(row).find('a')
        page = pq(scraperwiki.scrape(links.eq(0).attr('href')))
        title = _extract_title_from(page)
        content = _readable(page.find('.content').html())
        date = _extract_date_from(page)
        for attachment in page.find('.file_link a'):
            att = pq(attachment)
            attachments.append({att.text(): att.attr('html')})
    
        args = [title, date, content]
        kwargs = {}
        if len(attachments):
            kwargs.update(attachments=attachments)
        
        gasp.add_press_release(*args, **kwargs)

def scrape_speeches():
    speeches_page = pq(scraperwiki.scrape(BASE_URL + 'speeches'))
    links = speeches_page.find('.recordListTitle a.ContentGrid')
    for link in links:
        link = pq(link)
        sleep(1)

        title = ''
        date = None
        content = ''
        extra = {}

        page = pq(scraperwiki.scrape(link.attr('href')))
        title = _extract_title_from(page)
        content = _readable(page.find('.content').html())
        date = _extract_date_from(page)
        extra.update(type='speech')

        gasp.add_other_update(title, date, content, **extra)

def scrape_editorials():
    editorials_page = pq(scraperwiki.scrape(BASE_URL + 'editorials'))
    links = editorials_page.find('.recordListTitle a.ContentGrid')
    for link in links:
        link = pq(link)
        sleep(1)

        title = ''
        date = None
        content = ''
        extra = {}

        page = pq(scraperwiki.scrape(link.attr('href')))
        title = _extract_title_from(page)
        content = _readable(page.find('.content').html())
        date = _extract_date_from(page)
        extra.update(type='editorial')

        gasp.add_news_update(title, date, content, **extra)

def scrape_social_media():
    page = pq(scraperwiki.scrape(BASE_URL))
    gasp.add_facebook(page.find('.socialNet .facebook').attr('href'))
    gasp.add_twitter(page.find('.socialNet .twitter').attr('href'))
    gasp.add_youtube(page.find('.socialNet .youtube').attr('href'))
    gasp.add_social_media('rss', page.find('.socialNet .rss').attr('href'))


scrape_issues()
scrape_bio()
scrape_offices()
scrape_press_releases()
scrape_speeches()
scrape_editorials()
scrape_social_media()


'''Step 3) Run Your Scraper
   call gasp.finish() to let our server know your scraper succeeded'''
gasp.finish()