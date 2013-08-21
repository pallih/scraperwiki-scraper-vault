import scraperwiki, lxml.html

# Get text content with markup
# From: https://scraperwiki.com/docs/python/python_css_guide/
def ctext(el):           
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        result.append("<%s>" % sel.tag)
        result.append(ctext(sel))
        result.append("</%s>" % sel.tag)
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)

# Get list of embassies
html = scraperwiki.scrape("http://fco.innovate.direct.gov.uk/embassies")
root = lxml.html.fromstring(html)

for link in root.cssselect(".embassies a"):
    embassy = {}
    embassy['url']  = link.attrib["href"]
    embassy['name'] = link.text_content()

    print "Fetching %s" % embassy["name"]

    # Get embassy information
    html = scraperwiki.scrape(embassy['url'])
    root = lxml.html.fromstring(html)

    elems = root.cssselect('#locality')
    if len(elems) > 0 : embassy['locality'] = elems[0].text_content() 

    elems = root.cssselect("span[property='vcard:latitude']")
    if len(elems) > 0 : embassy['latitude'] = elems[0].text_content() 

    elems = root.cssselect("span[property='vcard:longitude']")
    if len(elems) > 0 : embassy['longitude'] = elems[0].text_content() 

    elems = root.cssselect("#address")
    if len(elems) > 0 : embassy['address'] = ctext(elems[0]).replace('</br>', '')

    elems = root.cssselect("a[rel='vcard:tel']")
    if len(elems) > 0 : embassy['phone'] = elems[0].text_content().replace('<br>', '')

    elems = root.cssselect("a[rel='vcard:email']")
    if len(elems) > 0 : embassy['email'] = elems[0].text_content()

    elems = root.cssselect("#office-hours")
    if len(elems) > 0 : embassy['office_hours'] = elems[0].text_content()

    elems = root.cssselect("#web a")
    if len(elems) > 0 : embassy['web'] = elems[0].attrib['href']

    # Save
    scraperwiki.sqlite.save(unique_keys=['url'], data=embassy)



