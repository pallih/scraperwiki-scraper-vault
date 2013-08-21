import scraperwiki
import lxml.html
import mechanize
import urlparse

def absolute_url(_netloc, url):
    """Canonicalize a relative url to an absolute one."""
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    if not scheme:
        scheme = 'http'
    if not netloc:
        netloc = _netloc
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

def open_and_parse_categories_page():
    """Open the initial (all) categories page, and follow relevant links."""
    html = scraperwiki.scrape("http://www.topcashback.co.uk/Categories")

    root = lxml.html.fromstring(html)
    for url in root.xpath("//div[@id='categories']/ul/li/a/@href"):
        open_and_parse_category_page(absolute_url('www.topcashback.co.uk', url))

def open_and_parse_category_page(url):
    """Open individual category page, get 'All' items, parse contents"""
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)
    br.select_form(nr=0)
    br.set_all_readonly(False)
    br["__EVENTTARGET"] = "ctl00$TwoColMain$ddlPageSize"
    br["ctl00$TwoColMain$ddlPageSize"] = ["All"]
    response = br.submit()

    #encoding=response.headers['content-type'].split('charset=')[-1]
    #br.encoding()
    #uhtml = unicode(response.read(), encoding)
    parse_category_merchants(response.read().decode(br.encoding()))

def parse_category_merchants(html):
    """Parse category page for merchant details"""
    table_exists = scraperwiki.sqlite.select("name FROM sqlite_master WHERE name='swdata'")
    root = lxml.html.fromstring(html)
    for merchant in root.xpath("//div[@class='retailer']"):
        a = merchant.xpath("div[@class='retailerDescription']/a")
        #print "*"+a[0].text+"*"
        #print(repr(a[0].text))
        #print(repr(a[0].text.strip()))
        name = a[0].text.strip()
        # Strip 'Cashback' suffix
        if name.endswith(' Cashback'):
            name = name[:-len(' Cashback')].strip()
        #print(repr(name))
        #print(repr(name.strip()))
        href = a[0].attrib['href']
        id = href.strip('/')
        href = absolute_url('www.topcashback.co.uk', href)
        desc = merchant.xpath("p[@class='retailerThirdCol']/span[@class='retailerCashbackDescription']/a")
        offer_detail = desc[0].text.strip()
        print name, href, offer_detail#, len(a[0].text), len(a[0].text.strip()), len(name)

        # check for existing entry for merchant
        #print 'checking for ' + name
        #data = scraperwiki.sqlite.select("* from swdata where name = '" + name + "'")
        data = None
        if table_exists:
            data = scraperwiki.sqlite.select("* from swdata where (`name` = ?)", (name,))

        if data:
            data = data[0]
        else:
            data = dict()
            data['domain'] = ''

        # fetch domain if not already known
        if(not data['domain']):
            data['domain'] = fetch_domain_for_id(id)

        # reset rest of data
        data['name'] = name
        data['tcb_href'] = href
        data['offer_detail'] = offer_detail

        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        table_exists = True

def fetch_domain_for_id(id):
    """Fetch domain for TopCashback merchant ID"""
    print 'fetching domain for ' + id
    url = 'https://www.topcashback.co.uk/earncashback.aspx?mpurl=' + id + '&continue=1'
    return get_target_domain(get_tcb_redirect_target(url))

def get_tcb_redirect_target(url):
    """Fetch URL to follow from Top Cashback page for merchant."""
    # Load redirect page
    try:
        html = scraperwiki.scrape(url)
    except Exception, e:
        print e
        return url

    # TopCashback brings up a banner page with Javascript redirect - find the manual redirect
    root = lxml.html.fromstring(html)
    links = root.xpath("//a[text()='here']")
    if links:
        url = links[0].attrib['href']
    else:
        print 'missing url link'
        url = ''
    # Handle the missing http:// prefix on the Canon redirect
    if url and not url.startswith('http://'):
        url = 'http://' + url

    return url

def get_target_domain(url):
    """Get target domain at the end of a series of redirecting URLs."""
    # TODO: follow links to grab domain
    # TODO: grab extra detail on merchant page

    try:
        target_url = scraperwiki.utils.urllib2.urlopen(url).url
    except scraperwiki.utils.urllib2.HTTPError as e:
        # errors such as 500 or 404 errors are PROBABLY still on the right domain
        target_url = e.url
    except Exception, e:
        print e
        target_url = ''

    return stripwww(url2domain(target_url))

def url2domain(url):
    return urlparse.urlparse(url).netloc

def stripwww(domain):
    if domain.startswith('www.'):
        return domain[4:]
    else:
        return domain

#print fetch_domain_for_id('active24')

open_and_parse_categories_page()

#html = scraperwiki.scrape('http://www.topcashback.co.uk/electricals/cashback/')
#html = scraperwiki.scrape('http://www.topcashback.co.uk/gambling/cashback/')
#parse_category_merchants(html)

#print get_target_domain('https://www.topcashback.co.uk/earncashback.aspx?mpurl=a-coombs-pet-centre&continue=1')
#print get_target_domain('https://www.topcashback.co.uk/earncashback.aspx?mpurl=currys&continue=1')

#print fetch_domain_for_id('canon')

#print scraperwiki.sqlite.show_tables()   
#data = scraperwiki.sqlite.select("* from swdata where name = 'Amazon.co.uk'")
#print data
#if data[0]['domain']:
#    print 'yes'

#data = scraperwiki.sqlite.select("* from swdata where (`name` = ?)", ("Sainsbury's",))
#print data
#name = 'Ladbrokes'
#data = scraperwiki.sqlite.select("* from swdata where (`name` = ?)", (name,))
#print data
#if not data:
#    print 'yes'
