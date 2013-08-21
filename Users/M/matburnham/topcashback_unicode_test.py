import scraperwiki
import lxml.html
import mechanize
import urlparse
import urllib2

def absolute_url(_netloc, url):
    """Canonicalize a relative url to an absolute one."""
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    if not scheme:
        scheme = 'http'
    if not netloc:
        netloc = _netloc
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

#def open_and_parse_category_page(url):
#    """Open individual category page, get 'All' items, parse contents"""
#    br = mechanize.Browser()
#    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#    response = br.open(url)
#    br.select_form(nr=0)
#    br.set_all_readonly(False)
#    br["__EVENTTARGET"] = "ctl00$TwoColMain$ddlPageSize"
#    br["ctl00$TwoColMain$ddlPageSize"] = ["All"]
#    response = br.submit()
#    parse_category_merchants(response.read())

def parse_category_merchants(html):
    """Parse category page for merchant details"""
    root = lxml.html.fromstring(html)
    for merchant in root.xpath("//div[@class='retailer']"):
        a = merchant.xpath("div[@class='retailerDescription']/a")
        name = a[0].text.strip()
        # Strip 'Cashback' suffix
        if name.endswith(' Cashback'):
            name = name[:-len(' Cashback')].strip()
        href = a[0].attrib['href']
        id = href.strip('/')
        href = absolute_url('www.topcashback.co.uk', href)
        desc = merchant.xpath("p[@class='retailerThirdCol']/span[@class='retailerCashbackDescription']/a")
        offer_detail = desc[0].text.strip()
        print name, href, offer_detail

        # reset rest of data
        data = dict()
        data['name'] = name
        data['tcb_href'] = href
        data['offer_detail'] = offer_detail

        print repr(offer_detail)

        scraperwiki.sqlite.save(unique_keys=['name'], data=data)


resp = urllib2.urlopen('http://www.topcashback.co.uk/electricals/cashback/')
encoding=resp.headers['content-type'].split('charset=')[-1]
html = resp.read()
uhtml = unicode(html, encoding)
parse_category_merchants(uhtml)

