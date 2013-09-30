import scraperwiki
import datetime
import lxml.html
from lxml.cssselect import CSSSelector
import mechanize
import random
import re
import sys

# randomize list
def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

# returns a randomly selected user agent strings
def get_random_ua_string():
    ua = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MRA 4.6 (build 01425))',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0'
    ]
    ua = shuffle(ua)
    return ua[0]

hrefPattern = re.compile(r'javascript:NeuFenster\(\'([^\']+)\'\)')
suffixPattern = re.compile(r'rb_id=(\d+)&land_abk=([a-z]+)')
courtPattern = re.compile(r'(.+?) Aktenzeichen: (.+)')
announcementTimePattern = re.compile(r'Bekannt gemacht am: (\d+)\.(\d+)\.(\d+) (\d+):(\d+).+Uhr')
datePattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
linkSelector = CSSSelector("li a[href^='javascript:NeuFenster']")
dateFormat = "%Y-%m-%d"

browser = mechanize.Browser()
browser.addheaders = [("User-agent", get_random_ua_string())]
browser.set_handle_robots(False)

url = "http://www.handelsregisterbekanntmachungen.de/?aktion=suche"
detailUrlPrefix = "http://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?"

todayDate = datetime.date.today()
maxPast = todayDate + datetime.timedelta(-28)
#scraperwiki.sqlite.save_var('lastDate', maxPast.strftime(dateFormat))
lastDateString = scraperwiki.sqlite.get_var('lastDate', maxPast.strftime(dateFormat))
currentDate = datetime.datetime.strptime(lastDateString, dateFormat).date()

#maxPast = todayDate + datetime.timedelta(-27)
while currentDate < todayDate:
    scraperwiki.sqlite.save_var('lastDate', currentDate.strftime(dateFormat))
    day = currentDate.day
    month = currentDate.month
    year = currentDate.year
    
    response = browser.open(url)
    browser.select_form("suche")
    forms = browser.forms()
    browser["suchart"] = [ 'uneingeschr' ]
    browser["anzv"] = [ 'alle' ]
    browser["vt"] = [ str(day) ]
    browser["vm"] = [ str(month) ]
    browser["vj"] = [ str(year) ]
    browser["bt"] = [ str(day) ]
    browser["bm"] = [ str(month) ]
    browser["bj"] = [ str(year) ]
    
    response = browser.submit()
    
    detailTableSelector = CSSSelector("font table")
    
    root = lxml.html.fromstring(response.read())
    #print "num of links: ", len(linkSelector(root))
    #for entry in [linkSelector(root)[0]]:
    for entry in linkSelector(root):
        suffixMatch = hrefPattern.search(entry.get('href'))
        if suffixMatch:
            suffix = suffixMatch.group(1)
            idMatch = suffixPattern.search(suffix)
            if idMatch:
                rowId = idMatch.group(1)
                stateCode = idMatch.group(2)
                
                if len(scraperwiki.sqlite.select("* from swdata where id=? and stateCode=? limit 1", data=[rowId, stateCode])) > 0:
                    print "ignoring existing row ", { 'id': rowId, 'state': stateCode }
                else:
                    detailUrl = detailUrlPrefix + suffix
                    html = scraperwiki.scrape(detailUrl)
                    detailDoc = lxml.html.fromstring(html)
                    if len(detailTableSelector(detailDoc)) > 0:
                        table = detailTableSelector(detailDoc)[0]
                        tr = table.find('tr')
                        head1 = tr.find('td').find('nobr').find('u').text_content()
                        head2 = tr.find('td').getnext().find('nobr').text_content()
                        tr = tr.getnext().getnext()
                        announcementType = tr.find('td').text_content().strip()
                        tr = tr.getnext()
                        if tr != None:
                            actionDateString = tr.find('td').text_content().strip()
                            tr = tr.getnext().getnext()
                            announcementContent = tr.find('td').text_content().strip()
                            courtMatch = courtPattern.search(head1)
                            announcementTimeMatch = announcementTimePattern.search(head2)
                            actionDateMatch = datePattern.search(actionDateString)
                
                            if courtMatch and announcementTimeMatch and actionDateMatch:
                                courtName = courtMatch.group(1)
                                courtRefNum = courtMatch.group(2)
                                #print courtName, courtRefNum
                                announcementTime = announcementTimeMatch.group(3) + '-' + announcementTimeMatch.group(2) + '-' + announcementTimeMatch.group(1) + ' ' + announcementTimeMatch.group(4) + ':' + announcementTimeMatch.group(5)
                                actionDate = actionDateMatch.group(3) + '-' + actionDateMatch.group(2) + '-' + actionDateMatch.group(1)
                                #print announcementTime
                                #print actionDate
                                #print announcementType
                                #print announcementContent
                                record = {
                                    'id': rowId,
                                    'stateCode': stateCode,
                                    'announcementTime': announcementTime,
                                    'actionDate': actionDate,
                                    'courtName': courtName,
                                    'courtRefNum': courtRefNum,
                                    'announcementType': announcementType,
                                    'announcementContent': announcementContent
                                }
                                try:
                                    scraperwiki.sqlite.save(unique_keys=["id", "stateCode"], data=record)
                                    print "SAVE: ", record
                                except:
                                    print "Could not write record", record

    currentDate += datetime.timedelta(1)

import scraperwiki
import datetime
import lxml.html
from lxml.cssselect import CSSSelector
import mechanize
import random
import re
import sys

# randomize list
def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

# returns a randomly selected user agent strings
def get_random_ua_string():
    ua = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MRA 4.6 (build 01425))',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0'
    ]
    ua = shuffle(ua)
    return ua[0]

hrefPattern = re.compile(r'javascript:NeuFenster\(\'([^\']+)\'\)')
suffixPattern = re.compile(r'rb_id=(\d+)&land_abk=([a-z]+)')
courtPattern = re.compile(r'(.+?) Aktenzeichen: (.+)')
announcementTimePattern = re.compile(r'Bekannt gemacht am: (\d+)\.(\d+)\.(\d+) (\d+):(\d+).+Uhr')
datePattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
linkSelector = CSSSelector("li a[href^='javascript:NeuFenster']")
dateFormat = "%Y-%m-%d"

browser = mechanize.Browser()
browser.addheaders = [("User-agent", get_random_ua_string())]
browser.set_handle_robots(False)

url = "http://www.handelsregisterbekanntmachungen.de/?aktion=suche"
detailUrlPrefix = "http://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?"

todayDate = datetime.date.today()
maxPast = todayDate + datetime.timedelta(-28)
#scraperwiki.sqlite.save_var('lastDate', maxPast.strftime(dateFormat))
lastDateString = scraperwiki.sqlite.get_var('lastDate', maxPast.strftime(dateFormat))
currentDate = datetime.datetime.strptime(lastDateString, dateFormat).date()

#maxPast = todayDate + datetime.timedelta(-27)
while currentDate < todayDate:
    scraperwiki.sqlite.save_var('lastDate', currentDate.strftime(dateFormat))
    day = currentDate.day
    month = currentDate.month
    year = currentDate.year
    
    response = browser.open(url)
    browser.select_form("suche")
    forms = browser.forms()
    browser["suchart"] = [ 'uneingeschr' ]
    browser["anzv"] = [ 'alle' ]
    browser["vt"] = [ str(day) ]
    browser["vm"] = [ str(month) ]
    browser["vj"] = [ str(year) ]
    browser["bt"] = [ str(day) ]
    browser["bm"] = [ str(month) ]
    browser["bj"] = [ str(year) ]
    
    response = browser.submit()
    
    detailTableSelector = CSSSelector("font table")
    
    root = lxml.html.fromstring(response.read())
    #print "num of links: ", len(linkSelector(root))
    #for entry in [linkSelector(root)[0]]:
    for entry in linkSelector(root):
        suffixMatch = hrefPattern.search(entry.get('href'))
        if suffixMatch:
            suffix = suffixMatch.group(1)
            idMatch = suffixPattern.search(suffix)
            if idMatch:
                rowId = idMatch.group(1)
                stateCode = idMatch.group(2)
                
                if len(scraperwiki.sqlite.select("* from swdata where id=? and stateCode=? limit 1", data=[rowId, stateCode])) > 0:
                    print "ignoring existing row ", { 'id': rowId, 'state': stateCode }
                else:
                    detailUrl = detailUrlPrefix + suffix
                    html = scraperwiki.scrape(detailUrl)
                    detailDoc = lxml.html.fromstring(html)
                    if len(detailTableSelector(detailDoc)) > 0:
                        table = detailTableSelector(detailDoc)[0]
                        tr = table.find('tr')
                        head1 = tr.find('td').find('nobr').find('u').text_content()
                        head2 = tr.find('td').getnext().find('nobr').text_content()
                        tr = tr.getnext().getnext()
                        announcementType = tr.find('td').text_content().strip()
                        tr = tr.getnext()
                        if tr != None:
                            actionDateString = tr.find('td').text_content().strip()
                            tr = tr.getnext().getnext()
                            announcementContent = tr.find('td').text_content().strip()
                            courtMatch = courtPattern.search(head1)
                            announcementTimeMatch = announcementTimePattern.search(head2)
                            actionDateMatch = datePattern.search(actionDateString)
                
                            if courtMatch and announcementTimeMatch and actionDateMatch:
                                courtName = courtMatch.group(1)
                                courtRefNum = courtMatch.group(2)
                                #print courtName, courtRefNum
                                announcementTime = announcementTimeMatch.group(3) + '-' + announcementTimeMatch.group(2) + '-' + announcementTimeMatch.group(1) + ' ' + announcementTimeMatch.group(4) + ':' + announcementTimeMatch.group(5)
                                actionDate = actionDateMatch.group(3) + '-' + actionDateMatch.group(2) + '-' + actionDateMatch.group(1)
                                #print announcementTime
                                #print actionDate
                                #print announcementType
                                #print announcementContent
                                record = {
                                    'id': rowId,
                                    'stateCode': stateCode,
                                    'announcementTime': announcementTime,
                                    'actionDate': actionDate,
                                    'courtName': courtName,
                                    'courtRefNum': courtRefNum,
                                    'announcementType': announcementType,
                                    'announcementContent': announcementContent
                                }
                                try:
                                    scraperwiki.sqlite.save(unique_keys=["id", "stateCode"], data=record)
                                    print "SAVE: ", record
                                except:
                                    print "Could not write record", record

    currentDate += datetime.timedelta(1)

