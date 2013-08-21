# Blank Python
import scraperwiki
import BeautifulSoup
import re
import urllib
import dateutil.parser

''' Are MP names expected to change or can we hardcode
    possible matches to find via regex?

    The target page uses a table to hold speeches, so it
    should be possible to figure out the table structure
    to find the MP name and their matching speeches. 
    However, it's easier to just find the matching MP name 
    out of the speech, assuming the MP's term is greater 
    than the skraper's lifetime. 

    Or should the names be pulled from the department in parlparse?
'''
    
    

RE_TM = re.compile('Theresa May')
RE_LF = re.compile('Lynne Featherstone')
TM = 'Rt Hon Theresa May MP'
LF = 'Lynne Featherstone MP'

baseurl = 'http://www.equalities.gov.uk'
baselink = '/ministers/speeches-1.aspx'

# get speeches

speechlinks = []

html = scraperwiki.scrape(baseurl + baselink)
soup = BeautifulSoup.BeautifulSoup(html)
table = soup.find('table', {'summary':'Speeches'})
data = table.findAll('td')
for contents in data:
    a = contents.find('a')
    if a: speechlinks.append(a['href'])


for link in speechlinks:
    if link.split('.')[-1] == 'doc':
        continue
    record = {}
    link =  link.replace(u'\u2019', u'%92')
    link = baseurl + link
    print link
    record['department'] = 'Government Equalities Office'
    record['permalink'] = link
    try:
        page = scraperwiki.scrape(link)
    except:
        print "Page not found"
        continue
    soup = BeautifulSoup.BeautifulSoup(page)
    speech = soup.find('div', {'class' : 'contentinnerfullwidth'})
    title = speech.find('h1')
    record['title'] = title.text
    title.extract()
    date = speech.find('h2')
    record['given_on'] = date.text
    dateobj = dateutil.parser.parse(date.text)
    date.extract()
    header = soup.find('strong')

    if re.search(RE_TM, header.text):
        record['minister_name'] = TM
    elif re.search(RE_LF, header.text):
        record['minister_name'] = LF
    else:
        record['minister_name'] = "None Found"
    header.extract()
    record['where'] = ''
    record['body'] = speech.renderContents()

    scraperwiki.sqlite.save(['permalink'], record, date=dateobj)
    print record


