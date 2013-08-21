
def get_ons_resources_for_url(root):
    from lxml.html import fromstring
    import scraperwiki
    import urlparse

    html = scraperwiki.scrape(root)
    page = fromstring(html)

    results = []
    outerdivs = page.cssselect('.table-info')
    for odiv in outerdivs:
        url, title, description = None, None, None

        # URL
        dldiv = odiv.cssselect('.download-options ul li a')[0]
        url = urlparse.urljoin(root, dldiv.get('href'))

        dlinfo = odiv.cssselect('.download-info')[0]
        title = dlinfo.cssselect('h3')[0].text_content()

        description = dlinfo.cssselect('div')[2].text_content()
        description = description.strip()[len('Description: '):]

        results.append((title, url, description,))
    return results

root = 'http://www.ons.gov.uk/ons/publications/re-reference-tables.html?edition=tcm%3A77-237934'
results = get_ons_resources_for_url(root)
print results
