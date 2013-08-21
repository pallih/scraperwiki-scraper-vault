# Blank Python

import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

p = re.compile(r'senator=([0-9a-f]+)')

for page in [1,2,3,4]:
    html = scraperwiki.scrape("http://www.senate.go.th/profile/main.php?url=home&keyword=&page="+str(page))
    soup = BeautifulSoup(html, fromEncoding='cp874')
    table = soup.find("table", { "class" : "textnormal" })
    trs = table.findAll("tr")

    for tr in trs[3:]:
        print "------"
        td = tr.findAll("td")
        print td[0].text
        print td[1].find("b").string.replace("&nbsp;","")
        print td[2].text
        detail_id = p.findall(td[3].find("a")['href'])[0]

        detail_html = scraperwiki.scrape("http://www.senate.go.th/profile/main.php?url=history&senator="+detail_id)
        detail_soup = BeautifulSoup(detail_html, fromEncoding='cp874')
        detail_table = detail_soup.findAll("table", {"class" : "textnormal" })
        detail_trs = detail_soup.findAll("tr")
        for detail_tr in detail_trs:
            detail_td = detail_tr.findAll("div", { "class" : "picture" } )
            print detail_td

