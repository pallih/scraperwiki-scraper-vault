import scraperwiki
from scrapemark import scrape


for page in range(1,30):
    html = scraperwiki.scrape("http://www.ebay.in/sch/Laptops-/16159/i.html?_trkparms=65%253A12%257C66%253A1%257C39%253A1%257C72%253A3276&rt=nc&_catref=1&_dmpt=IN_PC_Laptops&_trksid=p3286.c0.m2000018.l2552&_pgn="+str(page))

    scrape_data = scrape("""
{*
<a href='{{ link.link1 }}'>{{ link.name }}</a>

*}
""", html=html);

    data = [{'url':p['link1'][0],} for p in scrape_data['link']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

import scraperwiki
from scrapemark import scrape


for page in range(1,30):
    html = scraperwiki.scrape("http://www.ebay.in/sch/Laptops-/16159/i.html?_trkparms=65%253A12%257C66%253A1%257C39%253A1%257C72%253A3276&rt=nc&_catref=1&_dmpt=IN_PC_Laptops&_trksid=p3286.c0.m2000018.l2552&_pgn="+str(page))

    scrape_data = scrape("""
{*
<a href='{{ link.link1 }}'>{{ link.name }}</a>

*}
""", html=html);

    data = [{'url':p['link1'][0],} for p in scrape_data['link']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

