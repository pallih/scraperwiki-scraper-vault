import dateutil.parser, lxml.html, re, scraperwiki

base_url = "http://www.marbuch-verlag.de/okaz/anzlesen2010.asp?Rubrik=63&show="
parse_html = lambda url: lxml.html.fromstring(scraperwiki.scrape(url))
re_email = re.compile("mailto:")
re_web = re.compile("http://")
re_kontakt = re.compile("Kontakt:(.*)")

n = int(re.search("([1-9][0-9]*)$", parse_html(base_url + "1").cssselect('*[class="okaz-header-rubrik-right"]')[0].text).group(1))
for root in (parse_html(page_url) for page_url in (base_url + str(i) for i in xrange(1, n + 1))):
    for item in root.cssselect('*[class="okaz-table"]'):
        contact = item.cssselect('*[class="okaz-footer"]')[0]
        data = { "timestamp" : dateutil.parser.parse(item.cssselect('*[class="okaz-header-left"]')[0].text, dayfirst=True),
                 "number" : int(item.cssselect('*[class="okaz-header-right"] a')[0].text),            
                 "title" : item.cssselect('*[class="okaz-titel"]')[0].text,
                 "text" : item.cssselect('*[class="okaz-text"] br')[0].tail,
                 "email" : False, "web" : False, "kontakt" : False,
                 "gewerblich" : True if contact.cssselect('b') else None }
        links = contact.cssselect("a[href]")
        if links:
            for link in links:
                href = link.attrib["href"]
                if re_email.match(href):
                    data["email"] = link.text
                elif re_web.match(href):
                    data["web"] = link.text
            kontakt = re_kontakt.match(link.tail)
            if kontakt:
                data["kontakt"] = kontakt.group(1) 
        else:
            kontakt = re_kontakt.match(contact.text)
            if kontakt:
                data["kontakt"] = kontakt.group(1)
        scraperwiki.sqlite.save(unique_keys=['number'], data=data)
        