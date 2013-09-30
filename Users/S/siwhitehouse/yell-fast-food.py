#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
import string
import time
import datetime
import lxml.html
from scraperwiki import scrape

html = scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=1')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=2')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=3')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=4')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=5')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=6')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=7')
print html
root = lxml.html.fromstring(html)
titles = root.cssselect("title")[0]
print lxml.etree.tostring(titles)

#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
import string
import time
import datetime
import lxml.html
from scraperwiki import scrape

html = scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=1')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=2')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=3')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=4')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=5')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=6')
html = html + scraperwiki.scrape('http://www.yell.com/ucs/UcsSearchAction.do?startAt=60&keywords=fast+food&location=Birmingham&scrambleSeed=2121503118&showOoa=10&ppcStartAt=0&pageNum=7')
print html
root = lxml.html.fromstring(html)
titles = root.cssselect("title")[0]
print lxml.etree.tostring(titles)

