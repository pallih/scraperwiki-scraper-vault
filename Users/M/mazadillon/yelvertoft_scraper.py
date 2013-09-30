import scraperwiki
import lxml.html
import datetime
import re

rx = re.compile('[\s\t]+')

html = scraperwiki.scrape('http://www.yelvertoftchurch.org.uk/')
root = lxml.html.fromstring(html)
sidebar = root.cssselect("div[id='diywebSidebar']")[0]
news = sidebar[0].text_content()
res = rx.sub(' ', news.strip()[4:]).strip()

scraperwiki.sqlite.save(['news'], {'news': res,'date': datetime.datetime.now().strftime("%Y-%m-%d")})import scraperwiki
import lxml.html
import datetime
import re

rx = re.compile('[\s\t]+')

html = scraperwiki.scrape('http://www.yelvertoftchurch.org.uk/')
root = lxml.html.fromstring(html)
sidebar = root.cssselect("div[id='diywebSidebar']")[0]
news = sidebar[0].text_content()
res = rx.sub(' ', news.strip()[4:]).strip()

scraperwiki.sqlite.save(['news'], {'news': res,'date': datetime.datetime.now().strftime("%Y-%m-%d")})