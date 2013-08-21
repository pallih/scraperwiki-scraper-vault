import mechanize 
import urllib, urllib2
import lxml.etree
import lxml.html
import re
import scraperwiki
import urlparse
import datetime


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def ConvDate(d):
    md = re.match('\w\w\w (\d+) (\w\w\w) (\d\d\d\d)$', d)
    assert md, d
    return datetime.date(int(md.group(3)), months.index(md.group(2))+1, int(md.group(1)))


def ParseApplicationPage(data):
    durl = re.sub('summary', 'details', data['url'])
    #print durl
    for i in range(3):
        try:
            root = lxml.html.parse(urllib.urlopen(durl)).getroot()
            break
        except IOError, e:
            print "Try", i, e
    for tr in root.cssselect('table#applicationDetails tr'):
        #print lxml.etree.tostring(tr)
        assert [ t.tag  for t in tr ] == ['th', 'td']
        key = re.sub(":|\s", "", tr[0].text)
        if tr[1].text:
            data[key] = tr[1].text.strip()
        
    aurl = re.sub('summary', 'dates', data['url'])
    root = lxml.html.parse(urllib.urlopen(aurl)).getroot()
    for tr in root.cssselect('table#primaryDates tr'):
        #print lxml.etree.tostring(tr)
        assert [ t.tag  for t in tr ] == ['th', 'td']
        key = re.sub(":|\s", "", tr[0].text)
        v = (tr[1].text and "").strip()
        if v:
            md = re.match('(\d+) (\w\w\w) (\d\d\d\d)$', v)
            assert md, (key, tr[1].text, md)
            data[key] = datetime.date(int(md.group(3)), months.index(md.group(2))+1, int(md.group(1)))

            
def ParseLI(li, baseurl):
    lks = li.cssselect('a')
    assert len(lks) == 1
    lk = lks[0]
    data = { }
    data['url'] = urlparse.urljoin(baseurl, lk.attrib.get('href'))
    data['title'] = lk.text.strip()
    
    ps = li.cssselect('p')
    assert len(ps) == 2 and ps[0].attrib.get('class') == 'address' and ps[1].attrib.get('class') == 'metaInfo'
    data['address'] = ps[0].text.strip()
    mpostcode = re.search('\s*([A-Z]+\d+(?:\s*\d[A-Z]+)?)$', data['address'])
    assert mpostcode, data['address']
    data['postcode'] = mpostcode.group(1)
    mi = ps[1]
    assert len(mi) == 3 and mi[0].tag == 'span' and mi[0].text == '|', lxml.etree.tostring(mi)

    ses = [mi.text, mi[0].tail, mi[1].tail, mi[2].tail] 
    for se in ses:
        i = se.index(':')
        key = re.sub("\.\s", "", se[:i].strip())
        data[key] = se[i+1:].strip()
    assert data.keys() == ['Status', 'Received', 'title', 'url', 'RefNo', 'postcode', 'address', 'Validated']
    data['Received'] = ConvDate(data['Received'])
    data['Validated'] = ConvDate(data['Validated'])

    return data

    
def ParsePage(response, baseurl):
    root = lxml.html.parse(response).getroot()
    for li in root.cssselect('li.searchresult'):
        try:
            data = ParseLI(li, baseurl)
        except AssertionError:
            print lxml.etree.tostring(li)
            continue

        ParseApplicationPage(data)
        latlng = scraperwiki.geo.gb_postcode_to_latlng(data['postcode'])
        scraperwiki.datastore.save(unique_keys=['RefNo'], data=data, latlng=latlng)

    
def MainDate(sdate):
    url = "https://publicaccess.leeds.gov.uk/online-applications/search.do?action=advanced"
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    
    br.select_form('searchCriteriaForm')
    #print br.form.find_control('searchCriteria.ward').items
    #br['searchCriteria.ward'] = ['HORSFN']

    ldatestart = "%02d/%02d/%d" % (sdate.day, sdate.month, sdate.year)
    sdate1 = sdate + datetime.timedelta(0)
    print "DATE", ldatestart
    ldateend = "%02d/%02d/%d" % (sdate1.day, sdate1.month, sdate1.year)
    br['dates(applicationValidatedStart)'] = ldatestart 
    br['dates(applicationValidatedEnd)'] = ldateend

    try:
        response = br.submit()
    except urllib2.HTTPError:
        print "oops"
        return

    ParsePage(response, br.geturl())
    while True:
        nextlink = None
        for link in br.links():
            if link.text == 'Next[IMG]':
                nextlink = link
        if not nextlink:
            break
        print "LLLL", nextlink
        response = br.follow_link(nextlink)
        ParsePage(response, br.geturl())

        
def Main():
    datefrom = scraperwiki.metadata.get("datefrom", "1980-01-01")
    dateto = scraperwiki.metadata.get("dateto", "1980-01-01")
    
    dayfrom = datetime.date(int(datefrom [:4]), int(datefrom [5:7]), int(datefrom [8:]))
    dayto = datetime.date(int(dateto [:4]), int(dateto [5:7]), int(dateto [8:]))

    for i in range(200):
        dayfrom = dayfrom - datetime.timedelta(1)
        MainDate(dayfrom)
        scraperwiki.metadata.save("datefrom", dayfrom.isoformat())
        scraperwiki.metadata.save("dateto", dayto.isoformat())
        
Main()
