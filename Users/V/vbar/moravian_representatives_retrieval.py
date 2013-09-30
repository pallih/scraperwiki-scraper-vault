import lxml.html
import scraperwiki

scraperwiki.sqlite.attach('moravian_representatives_downloader', 'src')

input = scraperwiki.sqlite.select("* from src.swdata");
for rd in input:
    base_url = rd['url']
    page = lxml.html.fromstring(rd['html'])

    party = page.xpath("//h1/text()")[0]
    for td in page.xpath("//table/tbody/tr/td"):
        name_list = td.xpath("a/text()")
        if name_list:
            name = name_list[0]
            email_ref = td.xpath("a[starts-with(@href, 'mailto:')]/@href")[0]
            data = { 'name': name,
                'email': email_ref[7:],
                'party': party
            }
            scraperwiki.sqlite.save(unique_keys=['email'], data=data)

import lxml.html
import scraperwiki

scraperwiki.sqlite.attach('moravian_representatives_downloader', 'src')

input = scraperwiki.sqlite.select("* from src.swdata");
for rd in input:
    base_url = rd['url']
    page = lxml.html.fromstring(rd['html'])

    party = page.xpath("//h1/text()")[0]
    for td in page.xpath("//table/tbody/tr/td"):
        name_list = td.xpath("a/text()")
        if name_list:
            name = name_list[0]
            email_ref = td.xpath("a[starts-with(@href, 'mailto:')]/@href")[0]
            data = { 'name': name,
                'email': email_ref[7:],
                'party': party
            }
            scraperwiki.sqlite.save(unique_keys=['email'], data=data)

