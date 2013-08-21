import scraperwiki
html = scraperwiki.scrape("http://www.monitor-nhsft.gov.uk/about-nhs-foundation-trusts/nhs-foundation-trust-directory?letter=AllFT")

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS swdata')
scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`name` text, `nhsft-url` text)')

import lxml.html
root = lxml.html.fromstring(html)
for a in root.cssselect("#ftListing a"):
    name=a.text_content().strip()
    href=a.attrib['href']
    scraperwiki.sqlite.execute('INSERT INTO swdata(name, `nhsft-url`) VALUES (?, ?)',
        [name, href])

scraperwiki.sqlite.commit()
