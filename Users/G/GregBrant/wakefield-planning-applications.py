import mechanize 
import urllib
import lxml.etree
import lxml.html
import re
import scraperwiki
import urlparse
import datetime

scraperwiki.cache(True)


def ParseLI(li, url):
    print li, lxml.etree.tostring(li)
    lks = li.cssselect('a')
    assert len(lks) == 1
    lk = lks[0]
    data = { }
    data['url'] = urlparse.urljoin(url, lk.attrib.get('href'))
    data['title'] = lk.text.strip()
    
    ps = li.cssselect('p')
    assert len(ps) == 2 and ps[0].attrib.get('class') == 'address' and ps[1].attrib.get('class') == 'metaInfo'
    data['address'] = ps[0].text.strip()
    mpostcode = re.search('\s*([A-Z]+\d+(?:\s*\d[A-Z]+)?)$', data['address'])
    assert mpostcode, data['address']
    data['postcode'] = mpostcode.group(1)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(data['postcode'])
    print data
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
    scraperwiki.datastore.save(unique_keys=['RefNo'], data=data, latlng=latlng)

    
def Main():
    url = "http://planning.wakefield.gov.uk/online-applications/search.do?action=monthlyList"
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    
    br.select_form('searchCriteriaForm')
    #print br.form.find_control('searchCriteria.ward').items
    #br['searchCriteria.ward'] = ['HORSFN']
    #br['dates(applicationDecisionStart)'] = '21/06/2008'
    #br['dates(applicationDecisionEnd)'] = '10/07/2008'

    response = br.submit()
    root = lxml.html.parse(response).getroot()
    for li in root.cssselect('li.searchresult'):
        try:
            ParseLI(li, br.geturl())
        except AssertionError:
            print lxml.etree.tostring(li)
        
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def ConvDate(d):
    md = re.match('\w\w\w (\d+) (\w\w\w) (\d\d\d\d)$', d)
    assert md, d
    return datetime.date(int(md.group(3)), months.index(md.group(2))+1, int(md.group(1)))

        
Main()
