'''
  Extracting machine readable address data of German "Ausländerbehörden".
  Version, 4 June 2013.

'''

import scraperwiki
import lxml.html


def parse_page_navi(root):
    print "Parsing navigation links"
    nav_items = root.cssselect(".grid_bottom a")
    for nav_item in nav_items:
        title = nav_item.attrib['title']
        if title == "Letzte Seite":
            path = nav_item.attrib['href']
            return path


def parse_navi_string(last_page_string):
    separator = "="
    pair = last_page_string.split(separator)
    base = pair[0].split("/")[2]
    last = pair[1]
    urls = []
    for page_count in range(1, int(last) + 1):
        url = base + separator + str(page_count)
        urls.append(url)
    return urls


def sanitize(string):
    string = string.replace("Tel.:", "")
    string = string.replace(" ", "")
    string = string.replace("-", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("/", "")
    return string


def parse_service_entries(content, page_url):
    table_top = content.cssselect(".service_entries_table_top")[0]
    name = table_top.cssselect("h1")[0].text
    address = table_top.cssselect("h2")[0].text

    tds = content.cssselect(".service_entries_table_content table table tr td")
    td_pos = 0
    phone = None
    fax = None
    email = None
    while td_pos < len(tds):
        td = tds[td_pos].text
        if td == "Telefon:":
            phone = tds[td_pos + 1].text
            phone = sanitize(phone)
            # print phone
        if td == "Fax:":
            fax = tds[td_pos + 1].text
            fax = sanitize(fax)
            # print fax
        if td == "E-Mail:":
            email = str(tds[td_pos + 1].cssselect("a")[0].text).lower()
            # print email
        td_pos += 1

    # Extract location information from url path
    page_url_components = page_url.split("/")
    state = page_url_components[4]
    city = page_url_components[len(page_url_components)-4]

    data = { 
        'name': name, 
        'address': address, 
        'phone': phone,
        'fax': fax,
        'email': email,
        'state': state, 
        'city': city,
        'source': page_url 
    }
    # print data
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)


def parse_detail_page(page_url):
    # print "Parsing detail page: %s" % page_url
    html = scraperwiki.scrape(page_url)
    root = lxml.html.fromstring(html)
    for content in root.cssselect(".service_entries_table"):
        parse_service_entries(content, page_url)


def parse_main_page(url, main_page_url):
    # print "Parsing main page: %s" % main_page_url
    main_page_html = scraperwiki.scrape(main_page_url)
    main_page_root = lxml.html.fromstring(main_page_html)
    
    detail_pages = []
    for service_entry in main_page_root.cssselect(".service_entries_table"):
        for a in service_entry.cssselect("h3 a"):
            path = a.attrib['href']
            detail_page = url + path
            detail_pages.append(detail_page)
            # print detail_page
            
    return detail_pages


def parse_breadcrump_path(page_url):
    # print "Parsing breadcrump navigation: %s" % page_url
    html = scraperwiki.scrape(page_url)
    root = lxml.html.fromstring(html)
    breadcrumps = root.cssselect(".header_breadcrumb_left")
    last_breadcrump = breadcrumps[len(breadcrumps)-1]
    breadcrump_path = last_breadcrump.attrib['href']
    return breadcrump_path


def main(domain, url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    path = parse_page_navi(root)
    navi_paths = parse_navi_string(path)

    print "Found %i pages with regards to the navigation at the bottom." % len(navi_paths)

    all_detail_pages = []
    for navi_path in navi_paths:
        full_path = url + "/" + navi_path
        detail_pages = parse_main_page(url, full_path)
        all_detail_pages += detail_pages

    print "Found %i detail pages when expanding the navigation pages." % len(all_detail_pages)

    breadcrump_paths = []
    for detail_page in all_detail_pages:
        breadcrump_path = parse_breadcrump_path(detail_page)
        full_breadcrump_path = domain + breadcrump_path
        breadcrump_paths.append(full_breadcrump_path)

    print "Found %i breadcrump paths in those %i detail pages" % (len(breadcrump_paths), len(all_detail_pages))

    all_expanded_breadcrump_paths = []
    for breadcrump_path in breadcrump_paths:
        expanded_breadcrump_paths = parse_main_page(url, breadcrump_path)
        all_expanded_breadcrump_paths += expanded_breadcrump_paths

    print "Found %i pages when expanding the breadcrump paths." % len(all_expanded_breadcrump_paths)

    for breadcrump_path in all_expanded_breadcrump_paths:
        parse_detail_page(breadcrump_path)


domain = "http://www.ortsdienst.de"
url = "http://www.ortsdienst.de/Auslaenderbehoerde"
detail_test_url = "http://www.ortsdienst.de/Thueringen/Gotha/Gotha/Auslaenderbehoerde/Auslaenderbehoerde-des-Landkreises-inst96222/"


# parse_detail_page(detail_test_url)
# parse_main_page(url)
# path = parse_page_navi(url)
# print path

# urls = parse_navi_string("/Auslaenderbehoerde/?Seite=5")
# print urls

main(domain, url)