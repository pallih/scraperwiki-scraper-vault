import scraperwiki
import BeautifulSoup
import urllib2
import urllib
import cookielib
import datetime
import re

from scraperwiki import datastore

urlopen = urllib2.urlopen

cj = cookielib.LWPCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

Request = urllib2.Request

def post_form():
    url = "http://www.sendist.gov.uk/Public/search_decisions.aspx"
    reqdata = {}
    reqdata = urllib.urlencode(reqdata)
    req = Request(url, reqdata)
    handle = urlopen(req)

    soup = BeautifulSoup.BeautifulSoup(handle.read())
    viewstate = soup.find('input', {'name' : '__VIEWSTATE'})['value']
    return viewstate

def get_results(viewstate, page=0):
    if int(page) == 1:
        url = "http://www.sendist.gov.uk/Public/search_decisions.aspx"
        reqdata = {
               '__VIEWSTATE' : viewstate,
               'ddlGender' : '-',
               'ddlAgeRange' : '-',
               'ddlAppealType' : '-',
               'ddlDifficult' : '-',
               'ddlSchool=' : '-',
               'txtStart' : '',
               'txtEnd' : '',
               'txtKeyWords' : '',
               'cmdOk' : 'Search decisions',
               }
    else:
        url = "http://www.sendist.gov.uk/Public/search_results.aspx"        
        reqdata = {}
        reqdata['__EVENTTARGET'] = 'pager1'
        reqdata['__EVENTARGUMENT'] = int(page)
        reqdata['__VIEWSTATE'] = viewstate
    reqdata = urllib.urlencode(reqdata)
    req = Request(url, reqdata)
    handle = urlopen(req)

    soup = BeautifulSoup.BeautifulSoup(handle.read())
    
    viewstate = soup.find('input', {'name' : '__VIEWSTATE'})['value']
                
    #Work out if we're on the last page or not
    try:
        soup.findAll('a', {'id' : 'pager1', }, text=re.compile(u'Next'))[0].parent['href']        
        more = True
    except:
        more = False

    #Get each row and shove them in a list of dicts.
    rows = []
    headings = ['date', 'age', 'gender', 'appeal-type', 'learning-difficulty', 'school-type', 'document-url']
    for row in soup.findAll('table', {'class' : 'search-results-table percent90'})[0].findAll('tr'):
        row_dict = {}
        for i, td in enumerate(row.findAll('td')):
            row_dict[headings[i]] = td.string
        if 'date' in row_dict:
            try:
                row_dict['date'] = datetime.datetime.strptime(row_dict['date'], "%d/%m/%Y")
            except:
                pass
        if 'document-url' in row_dict:
            row_dict['document-url'] = "http://www.sendist.gov.uk/Public/" + td.find('a')['href']
        
        if len(row_dict) > 0:
            rows.append(row_dict)

    return (more, rows, viewstate)

viewstate = post_form()
more = True
page = 1
while more:
    print "Scraping page %s" % page
    (more, items, viewstate) = get_results(viewstate, page)
    page += 1
    for item in items:
        datastore.save(unique_keys=['date', 'age', 'document-url'], data=item)


