import scraperwiki
from lxml.html import fromstring
import re

linkre = re.compile('.*ndxp(\d+).html.*')
rootpage = scraperwiki.scrape('http://www.nuforc.org/webreports/ndxpost.html')
print linkre.match(rootpage)

import scraperwiki
from lxml.html import fromstring
import re

linkre = re.compile('.*ndxp(\d+).html.*')
rootpage = scraperwiki.scrape('http://www.nuforc.org/webreports/ndxpost.html')
print linkre.match(rootpage)

import scraperwiki
from lxml.html import fromstring
import re

linkre = re.compile('.*ndxp(\d+).html.*')
rootpage = scraperwiki.scrape('http://www.nuforc.org/webreports/ndxpost.html')
print linkre.match(rootpage)

