import scraperwiki
import mechanize
import urllib, urlparse
import lxml.etree, lxml.html
import re
import urlparse
import datetime

#scraperwiki.cache(True)

def Main():
    purl = 'http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/'
    root = lxml.html.parse(purl).getroot()
    urls = [ a.get('href')  for a in root.cssselect('ul.QuickNav li a')  if re.match("Published", a.text) ]
    for i, url in enumerate(urls):
        if i >= 1:  # skip all but the first
            continue
        print i, url
        parsesession(url)


def cleanup(data):
    assert data.get('Judge') == data.get('Author'), data
    author = data.pop('Author')
    judge = data.pop('Judge')
    mjudge = re.match('(.*?)\s+([LCJ]+)$', judge)
    if mjudge:
        data['judgename'] = mjudge.group(1)
        data['judgetitle'] = mjudge.group(2)
    else:
        data['judgename'] = judge

    for dkey in ['Date Created', 'Date Modified', 'Date Issued' ]:
        if data.get(dkey):
            mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', data.get(dkey))
            data[dkey] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    mdate = re.match('(\d+) (\w\w\w) (\d\d\d\d)', data.get('Date'))
    #print mdate.groups()
    imonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(mdate.group(2))
    data['Date'] = datetime.datetime(int(mdate.group(3)), imonth+1, int(mdate.group(1)))


def parsepage(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            break
        except IOError:
            pass
        
    rows = root.cssselect('table.MetaGrid_Display tr')
    data = { }
    for row in rows:
        td1, td2 = list(row)
        data[td1.text.strip(': ')] = td2.text
    a = root.cssselect('#MSCMSAttachmentCustom6_PresentationModeControlsContainer_presHyperLink')[0]
    #print data.keys()
    data['Judgment'] = urlparse.urljoin(url, a.get('href'))
    return data


def parsecontentspage(response):
    root = lxml.html.parse(response).getroot()

    rows = root.cssselect('table#DynamicControlDataGrid1_MSCSDataListXML_Document_Dynamic1 tr')
    headers = [ th[0].text  for th in rows.pop(0) ]
    assert headers == ['Date', 'Title', 'Identifier', 'Judge'], headers
    numdocs = int(root.cssselect("span#DynamicControlDataGrid1_lblDocCount")[0].text)

    lrt = ''
    if len(list(rows[-1])) == 1:
        lr = rows.pop()
        lrt = lxml.etree.tostring(lr)

    for tr in rows:
        data = dict(zip(headers, [tr[0].text, tr[1][0].text, tr[2].text, tr[3].text]))
        data['url'] = tr[1][0].get('href')
        fdata = parsepage(data['url'])
        assert data.get('Identifier') == fdata.get('Identifier'), (data, fdata)
        assert data.get('Title') == fdata.get('Title'), (data, fdata)
        data.update(fdata)
        cleanup(data)
        #print data
        scraperwiki.datastore.save(unique_keys=['Identifier'], data=data, date=data.get('Date Issued'))

    return lrt, numdocs, len(rows)
        

def parsesession(url):
    br = mechanize.Browser()
    response = br.open(url)
    lrt, numdocs, count = parsecontentspage(response)

    ipage = 2    
    while lrt:
        plinks = re.findall("\"javascript:__doPostBack\('(.*?)','(.*?)'\)\">(\d+|\.\.\.)</a>", lrt)
        lklook = dict([ (int(x[2]), x)  for x in plinks  if x[2] != '...' ])
        nx = lklook.get(ipage)
        if not nx:
            if plinks and plinks[-1][2] == '...':
                assert (ipage % 10) == 1, lklook
                nx = plinks[-1]
            else:
                return

        print "Page", ipage

        br.select_form('DynamicTable')
        br.form.set_all_readonly(False)
        #print br.form.controls
        br['__EVENTTARGET'] = nx[0]
        br['__EVENTARGUMENT'] = nx[1]
        #print br.form.controls[-1].name
        br.form.find_control('DynamicControlDataGrid1:SearchButton').disabled=True
        response = br.submit()
    
        lrt, lnumdocs, lcount = parsecontentspage(response)
        ipage += 1
        assert numdocs == lnumdocs
        count += lcount
    assert count == lcount

Main()

                        

import scraperwiki
import mechanize
import urllib, urlparse
import lxml.etree, lxml.html
import re
import urlparse
import datetime

#scraperwiki.cache(True)

def Main():
    purl = 'http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/'
    root = lxml.html.parse(purl).getroot()
    urls = [ a.get('href')  for a in root.cssselect('ul.QuickNav li a')  if re.match("Published", a.text) ]
    for i, url in enumerate(urls):
        if i >= 1:  # skip all but the first
            continue
        print i, url
        parsesession(url)


def cleanup(data):
    assert data.get('Judge') == data.get('Author'), data
    author = data.pop('Author')
    judge = data.pop('Judge')
    mjudge = re.match('(.*?)\s+([LCJ]+)$', judge)
    if mjudge:
        data['judgename'] = mjudge.group(1)
        data['judgetitle'] = mjudge.group(2)
    else:
        data['judgename'] = judge

    for dkey in ['Date Created', 'Date Modified', 'Date Issued' ]:
        if data.get(dkey):
            mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', data.get(dkey))
            data[dkey] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    mdate = re.match('(\d+) (\w\w\w) (\d\d\d\d)', data.get('Date'))
    #print mdate.groups()
    imonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(mdate.group(2))
    data['Date'] = datetime.datetime(int(mdate.group(3)), imonth+1, int(mdate.group(1)))


def parsepage(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            break
        except IOError:
            pass
        
    rows = root.cssselect('table.MetaGrid_Display tr')
    data = { }
    for row in rows:
        td1, td2 = list(row)
        data[td1.text.strip(': ')] = td2.text
    a = root.cssselect('#MSCMSAttachmentCustom6_PresentationModeControlsContainer_presHyperLink')[0]
    #print data.keys()
    data['Judgment'] = urlparse.urljoin(url, a.get('href'))
    return data


def parsecontentspage(response):
    root = lxml.html.parse(response).getroot()

    rows = root.cssselect('table#DynamicControlDataGrid1_MSCSDataListXML_Document_Dynamic1 tr')
    headers = [ th[0].text  for th in rows.pop(0) ]
    assert headers == ['Date', 'Title', 'Identifier', 'Judge'], headers
    numdocs = int(root.cssselect("span#DynamicControlDataGrid1_lblDocCount")[0].text)

    lrt = ''
    if len(list(rows[-1])) == 1:
        lr = rows.pop()
        lrt = lxml.etree.tostring(lr)

    for tr in rows:
        data = dict(zip(headers, [tr[0].text, tr[1][0].text, tr[2].text, tr[3].text]))
        data['url'] = tr[1][0].get('href')
        fdata = parsepage(data['url'])
        assert data.get('Identifier') == fdata.get('Identifier'), (data, fdata)
        assert data.get('Title') == fdata.get('Title'), (data, fdata)
        data.update(fdata)
        cleanup(data)
        #print data
        scraperwiki.datastore.save(unique_keys=['Identifier'], data=data, date=data.get('Date Issued'))

    return lrt, numdocs, len(rows)
        

def parsesession(url):
    br = mechanize.Browser()
    response = br.open(url)
    lrt, numdocs, count = parsecontentspage(response)

    ipage = 2    
    while lrt:
        plinks = re.findall("\"javascript:__doPostBack\('(.*?)','(.*?)'\)\">(\d+|\.\.\.)</a>", lrt)
        lklook = dict([ (int(x[2]), x)  for x in plinks  if x[2] != '...' ])
        nx = lklook.get(ipage)
        if not nx:
            if plinks and plinks[-1][2] == '...':
                assert (ipage % 10) == 1, lklook
                nx = plinks[-1]
            else:
                return

        print "Page", ipage

        br.select_form('DynamicTable')
        br.form.set_all_readonly(False)
        #print br.form.controls
        br['__EVENTTARGET'] = nx[0]
        br['__EVENTARGUMENT'] = nx[1]
        #print br.form.controls[-1].name
        br.form.find_control('DynamicControlDataGrid1:SearchButton').disabled=True
        response = br.submit()
    
        lrt, lnumdocs, lcount = parsecontentspage(response)
        ipage += 1
        assert numdocs == lnumdocs
        count += lcount
    assert count == lcount

Main()

                        

import scraperwiki
import mechanize
import urllib, urlparse
import lxml.etree, lxml.html
import re
import urlparse
import datetime

#scraperwiki.cache(True)

def Main():
    purl = 'http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/'
    root = lxml.html.parse(purl).getroot()
    urls = [ a.get('href')  for a in root.cssselect('ul.QuickNav li a')  if re.match("Published", a.text) ]
    for i, url in enumerate(urls):
        if i >= 1:  # skip all but the first
            continue
        print i, url
        parsesession(url)


def cleanup(data):
    assert data.get('Judge') == data.get('Author'), data
    author = data.pop('Author')
    judge = data.pop('Judge')
    mjudge = re.match('(.*?)\s+([LCJ]+)$', judge)
    if mjudge:
        data['judgename'] = mjudge.group(1)
        data['judgetitle'] = mjudge.group(2)
    else:
        data['judgename'] = judge

    for dkey in ['Date Created', 'Date Modified', 'Date Issued' ]:
        if data.get(dkey):
            mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', data.get(dkey))
            data[dkey] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    mdate = re.match('(\d+) (\w\w\w) (\d\d\d\d)', data.get('Date'))
    #print mdate.groups()
    imonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(mdate.group(2))
    data['Date'] = datetime.datetime(int(mdate.group(3)), imonth+1, int(mdate.group(1)))


def parsepage(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            break
        except IOError:
            pass
        
    rows = root.cssselect('table.MetaGrid_Display tr')
    data = { }
    for row in rows:
        td1, td2 = list(row)
        data[td1.text.strip(': ')] = td2.text
    a = root.cssselect('#MSCMSAttachmentCustom6_PresentationModeControlsContainer_presHyperLink')[0]
    #print data.keys()
    data['Judgment'] = urlparse.urljoin(url, a.get('href'))
    return data


def parsecontentspage(response):
    root = lxml.html.parse(response).getroot()

    rows = root.cssselect('table#DynamicControlDataGrid1_MSCSDataListXML_Document_Dynamic1 tr')
    headers = [ th[0].text  for th in rows.pop(0) ]
    assert headers == ['Date', 'Title', 'Identifier', 'Judge'], headers
    numdocs = int(root.cssselect("span#DynamicControlDataGrid1_lblDocCount")[0].text)

    lrt = ''
    if len(list(rows[-1])) == 1:
        lr = rows.pop()
        lrt = lxml.etree.tostring(lr)

    for tr in rows:
        data = dict(zip(headers, [tr[0].text, tr[1][0].text, tr[2].text, tr[3].text]))
        data['url'] = tr[1][0].get('href')
        fdata = parsepage(data['url'])
        assert data.get('Identifier') == fdata.get('Identifier'), (data, fdata)
        assert data.get('Title') == fdata.get('Title'), (data, fdata)
        data.update(fdata)
        cleanup(data)
        #print data
        scraperwiki.datastore.save(unique_keys=['Identifier'], data=data, date=data.get('Date Issued'))

    return lrt, numdocs, len(rows)
        

def parsesession(url):
    br = mechanize.Browser()
    response = br.open(url)
    lrt, numdocs, count = parsecontentspage(response)

    ipage = 2    
    while lrt:
        plinks = re.findall("\"javascript:__doPostBack\('(.*?)','(.*?)'\)\">(\d+|\.\.\.)</a>", lrt)
        lklook = dict([ (int(x[2]), x)  for x in plinks  if x[2] != '...' ])
        nx = lklook.get(ipage)
        if not nx:
            if plinks and plinks[-1][2] == '...':
                assert (ipage % 10) == 1, lklook
                nx = plinks[-1]
            else:
                return

        print "Page", ipage

        br.select_form('DynamicTable')
        br.form.set_all_readonly(False)
        #print br.form.controls
        br['__EVENTTARGET'] = nx[0]
        br['__EVENTARGUMENT'] = nx[1]
        #print br.form.controls[-1].name
        br.form.find_control('DynamicControlDataGrid1:SearchButton').disabled=True
        response = br.submit()
    
        lrt, lnumdocs, lcount = parsecontentspage(response)
        ipage += 1
        assert numdocs == lnumdocs
        count += lcount
    assert count == lcount

Main()

                        

import scraperwiki
import mechanize
import urllib, urlparse
import lxml.etree, lxml.html
import re
import urlparse
import datetime

#scraperwiki.cache(True)

def Main():
    purl = 'http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/'
    root = lxml.html.parse(purl).getroot()
    urls = [ a.get('href')  for a in root.cssselect('ul.QuickNav li a')  if re.match("Published", a.text) ]
    for i, url in enumerate(urls):
        if i >= 1:  # skip all but the first
            continue
        print i, url
        parsesession(url)


def cleanup(data):
    assert data.get('Judge') == data.get('Author'), data
    author = data.pop('Author')
    judge = data.pop('Judge')
    mjudge = re.match('(.*?)\s+([LCJ]+)$', judge)
    if mjudge:
        data['judgename'] = mjudge.group(1)
        data['judgetitle'] = mjudge.group(2)
    else:
        data['judgename'] = judge

    for dkey in ['Date Created', 'Date Modified', 'Date Issued' ]:
        if data.get(dkey):
            mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', data.get(dkey))
            data[dkey] = datetime.datetime(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    mdate = re.match('(\d+) (\w\w\w) (\d\d\d\d)', data.get('Date'))
    #print mdate.groups()
    imonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(mdate.group(2))
    data['Date'] = datetime.datetime(int(mdate.group(3)), imonth+1, int(mdate.group(1)))


def parsepage(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            break
        except IOError:
            pass
        
    rows = root.cssselect('table.MetaGrid_Display tr')
    data = { }
    for row in rows:
        td1, td2 = list(row)
        data[td1.text.strip(': ')] = td2.text
    a = root.cssselect('#MSCMSAttachmentCustom6_PresentationModeControlsContainer_presHyperLink')[0]
    #print data.keys()
    data['Judgment'] = urlparse.urljoin(url, a.get('href'))
    return data


def parsecontentspage(response):
    root = lxml.html.parse(response).getroot()

    rows = root.cssselect('table#DynamicControlDataGrid1_MSCSDataListXML_Document_Dynamic1 tr')
    headers = [ th[0].text  for th in rows.pop(0) ]
    assert headers == ['Date', 'Title', 'Identifier', 'Judge'], headers
    numdocs = int(root.cssselect("span#DynamicControlDataGrid1_lblDocCount")[0].text)

    lrt = ''
    if len(list(rows[-1])) == 1:
        lr = rows.pop()
        lrt = lxml.etree.tostring(lr)

    for tr in rows:
        data = dict(zip(headers, [tr[0].text, tr[1][0].text, tr[2].text, tr[3].text]))
        data['url'] = tr[1][0].get('href')
        fdata = parsepage(data['url'])
        assert data.get('Identifier') == fdata.get('Identifier'), (data, fdata)
        assert data.get('Title') == fdata.get('Title'), (data, fdata)
        data.update(fdata)
        cleanup(data)
        #print data
        scraperwiki.datastore.save(unique_keys=['Identifier'], data=data, date=data.get('Date Issued'))

    return lrt, numdocs, len(rows)
        

def parsesession(url):
    br = mechanize.Browser()
    response = br.open(url)
    lrt, numdocs, count = parsecontentspage(response)

    ipage = 2    
    while lrt:
        plinks = re.findall("\"javascript:__doPostBack\('(.*?)','(.*?)'\)\">(\d+|\.\.\.)</a>", lrt)
        lklook = dict([ (int(x[2]), x)  for x in plinks  if x[2] != '...' ])
        nx = lklook.get(ipage)
        if not nx:
            if plinks and plinks[-1][2] == '...':
                assert (ipage % 10) == 1, lklook
                nx = plinks[-1]
            else:
                return

        print "Page", ipage

        br.select_form('DynamicTable')
        br.form.set_all_readonly(False)
        #print br.form.controls
        br['__EVENTTARGET'] = nx[0]
        br['__EVENTARGUMENT'] = nx[1]
        #print br.form.controls[-1].name
        br.form.find_control('DynamicControlDataGrid1:SearchButton').disabled=True
        response = br.submit()
    
        lrt, lnumdocs, lcount = parsecontentspage(response)
        ipage += 1
        assert numdocs == lnumdocs
        count += lcount
    assert count == lcount

Main()

                        

