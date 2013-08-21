import lxml.html
import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_downloader', 'src')

input = scraperwiki.sqlite.select("* from src.swdata");
for rd in input:
    page = lxml.html.fromstring(rd['html'])
    for a in page.xpath("//a[starts-with(@href, 'mailto:')]"):
        name = a.text_content().strip()
        if name: # extra e-mails on the page have pictures
            email_ref = a.xpath("@href")[0]

            party = ""
            party_list = a.xpath("following-sibling::text()")
            if party_list:
                match = re.search(r'\(([^\(\)]+)\)', party_list[0])
                if match:
                    party = match.group(1).strip()

            data = { 'name': name,
                    'email': email_ref[7:],
                    'party': party
                }
            scraperwiki.sqlite.save(unique_keys=['email'], data=data)

