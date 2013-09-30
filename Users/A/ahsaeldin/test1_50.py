import scraperwiki

import sys
import mechanize

propertyLst = []

start_url = 'http://www.thorgills.com/results.asp?onmap=2&displayperpage=10&view=list&displayorder=PriceAskd&pricehigh=0&pricelow=0&pricetype=3&offset=0'

br = mechanize.Browser()

def Navigate(url):
    br.open(url)
    for link in br.links(url_regex='/property/'):
        if link.url[0:1] == '/':
            propertyURL = 'http://www.thorgills.com' + link.url
        else:
            propertyURL = 'http://www.thorgills.com/' + link.url

        if not propertyURL in propertyLst:
            propertyLst.append(propertyURL)

def ShowProgress(state, progress):
    sys.stdout.write("\r%d"  %progress + ' ' + state)
    sys.stdout.flush()

def ShowPercentage(x):#Display a percentage progress in console
    sys.stdout.write("\r%d%%" %x)    # or print >> sys.stdout, "\r%d%%" %i,
    sys.stdout.flush()

def ReportState(state):
    print state

ReportState("Collecting Properties URLs...")

Navigate(start_url)

ShowProgress("Properties Found.", len(propertyLst))

isThereNext = True
# while isThereNext:
#     try:
#         response1 = br.follow_link(text_regex=r"Next", nr=1)
#     except:
#         isThereNext = False
#         break
#
#     next_url = response1.geturl()
#     if next_url:
#         Navigate(next_url)
#         ShowProgress("Properties Found.", len(propertyLst))
#     else:
#         isThereNext = False

counter = 0
for propertyURL in propertyLst:
    counter = counter + 1
    dataDict = {'url': propertyURL}
    html = scraperwiki.scrape(propertyURL)
    print html
    #scraperwiki.sqlite.save(unique_keys=['url'], data=dataDict)

print('done')
