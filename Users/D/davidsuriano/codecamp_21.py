from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save

COLUMN_NAMES = ['Category','Total']

#from scraperwiki import pdftoxml
#import datetime

#VERBOSE= False

#def log(foo):
#    if VERBOSE:
#        print(foo)

tagspage = urlopen('http://dribbble.com/tags').read()
html = fromstring(tagspage)

total = html.cssselect('ol > li > em')
category = html.cssselect('ol > li > a > strong')

#print tostring(category[0])
#print map(tostring, category)

catname = [categoryName.text_content() for categoryName in category]
totnum = [int(totalNumber.text_content()) for totalNumber in total]

data = []
counter = 0
for cat in catname:
    data.append(dict(Category=cat,
                     Total=totnum[counter]))
    counter += 1

save([], data)


from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save

COLUMN_NAMES = ['Category','Total']

#from scraperwiki import pdftoxml
#import datetime

#VERBOSE= False

#def log(foo):
#    if VERBOSE:
#        print(foo)

tagspage = urlopen('http://dribbble.com/tags').read()
html = fromstring(tagspage)

total = html.cssselect('ol > li > em')
category = html.cssselect('ol > li > a > strong')

#print tostring(category[0])
#print map(tostring, category)

catname = [categoryName.text_content() for categoryName in category]
totnum = [int(totalNumber.text_content()) for totalNumber in total]

data = []
counter = 0
for cat in catname:
    data.append(dict(Category=cat,
                     Total=totnum[counter]))
    counter += 1

save([], data)


