import lxml.html
import scraperwiki

# Parses the hard parts, i.e. name & party (others, i.e. phone,
# should be added here when needed). Doesn't do e-mail,
# because e-mail is probably better found by mailto anchor
# than by label meant for human readers.
def parse_row(tr):
    lbl = tr.xpath("td//strong")
    name = None
    party = None
    for l in lbl:
        label_text = l.xpath("text()")
        for t0 in label_text:
            t = t0.strip()
            if not name:
                name = t
                if name.endswith(","):
                    name = name[:-1].strip()
                if not name:
                    raise Exception("name not found")
            elif t.endswith("strana (koalice):"):
                val = l.xpath("following-sibling::text()")
                if val:
                    party = val[0].strip()
                    # no party considered OK (although it may still
                    # blow on the previous line, but solving that can
                    # wait until we get such input)
                    return (name, party)

    if not name:
        raise Exception("name not found")
    else:
        raise Exception("party not found")

scraperwiki.sqlite.attach('ostrava_councillors_downloader', 'src')

input = scraperwiki.sqlite.select("* from src.swdata");
for rd in input:
    page = lxml.html.fromstring(rd['html'])
    for tr in page.xpath("//table/tbody/tr"):
        name, party = parse_row(tr)
        for email in tr.xpath(".//a[starts-with(@href, 'mailto:')]/text()"):
            data = { 'name': name,
                'party': party,
                'email': email
            }
            scraperwiki.sqlite.save(unique_keys=['email'], data=data)

