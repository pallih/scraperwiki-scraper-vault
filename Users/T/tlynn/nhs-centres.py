import lxml.html

from scraperwiki.datastore import save


def first(list, default=None):
    """Returns the first item in list or default if the list is empty."""
    if list:
        return list[0]
    else:
        return default

def upto_n(n, sequence, default=None):
    """Returns a list of n items from sequence.  If there are 
       less than n available, pads the list to n with default.
       Raises a ValueError if there are more than n items."""
    items = list(sequence)
    if len(items)<=n:
        return items + [default]*(n - len(items))
    else:
        raise ValueError("Got a list of length %d: %r" % (len(items), items))

def only(sequence, default=None):
    """Returns the only item in sequence, if there is exactly one.
       Returns default if the sequence is empty.
       Otherwise, raises a ValueError."""
    items = list(sequence)
    if len(items)==1:
        return items[0]
    elif len(items)==0:
        return None
    else:
        raise ValueError("Got a list of length %d: %r" % (len(items), items))

def gettext(node, default=None):
    """Gets the text of node and its children, compressing whitespace,
       or returns default if there is no node or no text."""
    if node is None:
        return default
    text = node.text_content()
    if text is None:
        return default
    return ' '.join(text.split())

def get_tag_pattern(tagpattern, node_sequence):
    """Returns patterns of consecutive nodes from node_sequence having 
       tags matching tagpattern."""
    got = []
    result = []
    for node in node_sequence:
        if node.tag==tagpattern[len(got)]:
            got.append(node)
            if len(got)==len(tagpattern):
                result.append(got)
                got = []
        else:
            got = []
    return result

def scrape_index():
    url = 'http://www.nhs.uk/servicedirectories/pages/primarycaretrustlisting.aspx'
    page = lxml.html.parse(url).getroot()

    links = page.cssselect('a')
    urls = [link.attrib['href'] for link in links]
    pct_urls = ['http://www.nhs.uk' + url
                for url in urls
                    if url.startswith('/ServiceDirectories/Pages/Trust.aspx?id=')]
    return pct_urls


def scrape_pct_page(source_url):
    """Scrape a single PCT (Primary Care Trust) page and save the results."""
    page = lxml.html.parse(source_url).getroot()
    results = []

    also_provide = upto_n(2, page.cssselect('div[class~="also-provide"]'))

    listview_box = only(also_provide[0].cssselect('ul[class="results"]'))
    if listview_box is not None:
        for li in listview_box:
            ul, tick_list_ul = li.getchildren()
            name_node = only(li for li in ul.cssselect('li')
                                 if li.cssselect('a'))
            name = gettext(name_node)
            link = only(name_node.cssselect('a'))
            more_info_url = 'http://www.nhs.uk' + link.attrib['href']
            address_node = only(ul.cssselect('li[class="address"]'))
            li_nodes = ul.cssselect('li')
            assert address_node in li_nodes[-2:]
            address = gettext(address_node)
            if address_node is li_nodes[-1]:
                tel = None
            else:
                tel = gettext(li_nodes[-1]).lstrip('Tel: ')
            results.append(('hospital', name, more_info_url, address, tel, None))

    if also_provide[1] is not None:
        p = only(also_provide[1].cssselect('p'))
        if p is not None:
            assert gettext(p)=='No Results'
            dts_and_dds = []
        else:
            dts_and_dds = [node for node in only(also_provide[1].cssselect('dl'))
                             if node.tag in ('dt', 'dd')]
        for dt, dd, dd2 in get_tag_pattern(('dt', 'dd', 'dd'), dts_and_dds):
            name = gettext(dt)
            aliases = None
            link = only(dt.cssselect('a'))
            more_info_url = None
            if link is not None:
                more_info_url = 'http://www.nhs.uk' + link.attrib['href']
                if link.attrib['title']!='Also known as : ' + name:
                    aliases = link.attrib['title'].lstrip('Also known as : ')
            address = gettext(dd)
            tel = gettext(dd2).lstrip('tel: ')
            results.append(('other', name, more_info_url, address, tel, aliases))

    for result in results:
        pct_type, name, more_info_url, address, tel, aliases = result
        assert None not in (pct_type, name, address), result

    for result in results:
        pct_type, name, more_info_url, address, tel, aliases = result
        data = {'pct-type': pct_type,
                'name': name,
                'info-url': more_info_url,
                'address': address,
                'tel': tel,
                'aliases': aliases,
                'source-url': source_url,
                }
        unique_keys = ['name', 'address']
        save(unique_keys, data)

#scrape_pct_page('http://www.nhs.uk/ServiceDirectories/Pages/Trust.aspx?id=5A9')
#scrape_pct_page('http://www.nhs.uk/ServiceDirectories/Pages/Trust.aspx?id=5JX')

pct_urls = scrape_index()
for i, url in enumerate(pct_urls):
    if '?id=TAC' in url: continue  #FIXME: Northumberland Care Trust, different format
    print "Scraping PCT page %d of %d: %s" % (i+1, len(pct_urls), url)
    scrape_pct_page(url)
