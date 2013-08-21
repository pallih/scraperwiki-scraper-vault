import scraperwiki
import urllib
import re
import urlparse
import sys
import lxml.etree
import lxml.html

def ParseCatchment(curl):
    root = lxml.html.parse(curl).getroot()
    #print lxml.etree.tostring(root)
    trs = root.cssselect('table.river-levels-table tr')
    headings = [ th.text  for th in trs[0].cssselect('th') ]
    assert headings == ['River', 'Town', 'River level station']
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        data = {'River':tds[0].text, 'Town':tds[1].text}
        assert tds[2][0].tag == 'a', tds
        data['station'] = tds[2][0].text
        data['url'] = urlparse.urljoin(curl, tds[2][0].attrib['href'])
        scraperwiki.datastore.save(unique_keys=["url"], data=data)
        

#ParseCatchment('http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120580.aspx?RegionId=1&AreaId=13&CatchmentId=75')

def GetLinks(url, idprep, hrefprep):
    result = [ ]    
    print idprep
    html = urllib.urlopen(url).read()
    r = '<a id="%s.*?" href="(%s\?.*?)">(.*?)</a>' % (idprep, hrefprep)
    print r
    reglist = re.findall(r, html)
    for regurl, reg in reglist:
        rurl = urlparse.urljoin(url, re.sub('&amp;', '&', regurl))
        print reg, rurl
        result.append(rurl)
    return result
            

def Main():
    # text only version of http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/default.aspx
    url = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120485.aspx'
    for rurl in GetLinks(url, 'RegionList1_', '/homeandleisure/floods/riverlevels/120506.aspx'):
        for aurl in GetLinks(rurl, 'AreaList1_', '/homeandleisure/floods/riverlevels/120537.aspx'):
            for curl in GetLinks(aurl, 'CatchmentList1_', '/homeandleisure/floods/riverlevels/120580.aspx'):
                ParseCatchment(curl)

Main()
import scraperwiki
import urllib
import re
import urlparse
import sys
import lxml.etree
import lxml.html

def ParseCatchment(curl):
    root = lxml.html.parse(curl).getroot()
    #print lxml.etree.tostring(root)
    trs = root.cssselect('table.river-levels-table tr')
    headings = [ th.text  for th in trs[0].cssselect('th') ]
    assert headings == ['River', 'Town', 'River level station']
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        data = {'River':tds[0].text, 'Town':tds[1].text}
        assert tds[2][0].tag == 'a', tds
        data['station'] = tds[2][0].text
        data['url'] = urlparse.urljoin(curl, tds[2][0].attrib['href'])
        scraperwiki.datastore.save(unique_keys=["url"], data=data)
        

#ParseCatchment('http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120580.aspx?RegionId=1&AreaId=13&CatchmentId=75')

def GetLinks(url, idprep, hrefprep):
    result = [ ]    
    print idprep
    html = urllib.urlopen(url).read()
    r = '<a id="%s.*?" href="(%s\?.*?)">(.*?)</a>' % (idprep, hrefprep)
    print r
    reglist = re.findall(r, html)
    for regurl, reg in reglist:
        rurl = urlparse.urljoin(url, re.sub('&amp;', '&', regurl))
        print reg, rurl
        result.append(rurl)
    return result
            

def Main():
    # text only version of http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/default.aspx
    url = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120485.aspx'
    for rurl in GetLinks(url, 'RegionList1_', '/homeandleisure/floods/riverlevels/120506.aspx'):
        for aurl in GetLinks(rurl, 'AreaList1_', '/homeandleisure/floods/riverlevels/120537.aspx'):
            for curl in GetLinks(aurl, 'CatchmentList1_', '/homeandleisure/floods/riverlevels/120580.aspx'):
                ParseCatchment(curl)

Main()
import scraperwiki
import urllib
import re
import urlparse
import sys
import lxml.etree
import lxml.html

def ParseCatchment(curl):
    root = lxml.html.parse(curl).getroot()
    #print lxml.etree.tostring(root)
    trs = root.cssselect('table.river-levels-table tr')
    headings = [ th.text  for th in trs[0].cssselect('th') ]
    assert headings == ['River', 'Town', 'River level station']
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        data = {'River':tds[0].text, 'Town':tds[1].text}
        assert tds[2][0].tag == 'a', tds
        data['station'] = tds[2][0].text
        data['url'] = urlparse.urljoin(curl, tds[2][0].attrib['href'])
        scraperwiki.datastore.save(unique_keys=["url"], data=data)
        

#ParseCatchment('http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120580.aspx?RegionId=1&AreaId=13&CatchmentId=75')

def GetLinks(url, idprep, hrefprep):
    result = [ ]    
    print idprep
    html = urllib.urlopen(url).read()
    r = '<a id="%s.*?" href="(%s\?.*?)">(.*?)</a>' % (idprep, hrefprep)
    print r
    reglist = re.findall(r, html)
    for regurl, reg in reglist:
        rurl = urlparse.urljoin(url, re.sub('&amp;', '&', regurl))
        print reg, rurl
        result.append(rurl)
    return result
            

def Main():
    # text only version of http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/default.aspx
    url = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120485.aspx'
    for rurl in GetLinks(url, 'RegionList1_', '/homeandleisure/floods/riverlevels/120506.aspx'):
        for aurl in GetLinks(rurl, 'AreaList1_', '/homeandleisure/floods/riverlevels/120537.aspx'):
            for curl in GetLinks(aurl, 'CatchmentList1_', '/homeandleisure/floods/riverlevels/120580.aspx'):
                ParseCatchment(curl)

Main()
import scraperwiki
import urllib
import re
import urlparse
import sys
import lxml.etree
import lxml.html

def ParseCatchment(curl):
    root = lxml.html.parse(curl).getroot()
    #print lxml.etree.tostring(root)
    trs = root.cssselect('table.river-levels-table tr')
    headings = [ th.text  for th in trs[0].cssselect('th') ]
    assert headings == ['River', 'Town', 'River level station']
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        data = {'River':tds[0].text, 'Town':tds[1].text}
        assert tds[2][0].tag == 'a', tds
        data['station'] = tds[2][0].text
        data['url'] = urlparse.urljoin(curl, tds[2][0].attrib['href'])
        scraperwiki.datastore.save(unique_keys=["url"], data=data)
        

#ParseCatchment('http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120580.aspx?RegionId=1&AreaId=13&CatchmentId=75')

def GetLinks(url, idprep, hrefprep):
    result = [ ]    
    print idprep
    html = urllib.urlopen(url).read()
    r = '<a id="%s.*?" href="(%s\?.*?)">(.*?)</a>' % (idprep, hrefprep)
    print r
    reglist = re.findall(r, html)
    for regurl, reg in reglist:
        rurl = urlparse.urljoin(url, re.sub('&amp;', '&', regurl))
        print reg, rurl
        result.append(rurl)
    return result
            

def Main():
    # text only version of http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/default.aspx
    url = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120485.aspx'
    for rurl in GetLinks(url, 'RegionList1_', '/homeandleisure/floods/riverlevels/120506.aspx'):
        for aurl in GetLinks(rurl, 'AreaList1_', '/homeandleisure/floods/riverlevels/120537.aspx'):
            for curl in GetLinks(aurl, 'CatchmentList1_', '/homeandleisure/floods/riverlevels/120580.aspx'):
                ParseCatchment(curl)

Main()
import scraperwiki
import urllib
import re
import urlparse
import sys
import lxml.etree
import lxml.html

def ParseCatchment(curl):
    root = lxml.html.parse(curl).getroot()
    #print lxml.etree.tostring(root)
    trs = root.cssselect('table.river-levels-table tr')
    headings = [ th.text  for th in trs[0].cssselect('th') ]
    assert headings == ['River', 'Town', 'River level station']
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        data = {'River':tds[0].text, 'Town':tds[1].text}
        assert tds[2][0].tag == 'a', tds
        data['station'] = tds[2][0].text
        data['url'] = urlparse.urljoin(curl, tds[2][0].attrib['href'])
        scraperwiki.datastore.save(unique_keys=["url"], data=data)
        

#ParseCatchment('http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120580.aspx?RegionId=1&AreaId=13&CatchmentId=75')

def GetLinks(url, idprep, hrefprep):
    result = [ ]    
    print idprep
    html = urllib.urlopen(url).read()
    r = '<a id="%s.*?" href="(%s\?.*?)">(.*?)</a>' % (idprep, hrefprep)
    print r
    reglist = re.findall(r, html)
    for regurl, reg in reglist:
        rurl = urlparse.urljoin(url, re.sub('&amp;', '&', regurl))
        print reg, rurl
        result.append(rurl)
    return result
            

def Main():
    # text only version of http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/default.aspx
    url = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120485.aspx'
    for rurl in GetLinks(url, 'RegionList1_', '/homeandleisure/floods/riverlevels/120506.aspx'):
        for aurl in GetLinks(rurl, 'AreaList1_', '/homeandleisure/floods/riverlevels/120537.aspx'):
            for curl in GetLinks(aurl, 'CatchmentList1_', '/homeandleisure/floods/riverlevels/120580.aspx'):
                ParseCatchment(curl)

Main()
