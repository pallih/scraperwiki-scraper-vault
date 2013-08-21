import lxml.html
import scraperwiki
import urlparse

scraperwiki.sqlite.attach('prague_councillors_downloader', 'src')
input = scraperwiki.sqlite.select("* from src.swdata");
for rd in input:
    base_url = rd['url']
    page = lxml.html.fromstring(rd['html'])

    for tr in page.xpath("//table/tbody/tr"):
        tds = tr.xpath("td")

        name_col = tds[0]
        name = name_col.text_content().strip()
        href = name_col.xpath("a/@href")[0]

        email = tds[2].xpath("a[starts-with(@href, 'mailto:')]/text()")[0] # FIXME: convert case

        data = { 'name': name,
            'detail': urlparse.urljoin(base_url, href),
            'party': tds[1].text_content().strip(),
            'email': email
        }
        scraperwiki.sqlite.save(unique_keys=['email'], data=data)

