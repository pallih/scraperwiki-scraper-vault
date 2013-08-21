import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    tds = soup.findAll('tr')
    i = 0
    for tr in tds:
        record = {}
        tdr = tr.findAll('td')    # get all the <td> tags
        k = 0
        val = 0
        if i == 0:
            record["desc"] = "bid"
        if i == 1:
            record["desc"] = "bidvolume"
        if i == 2:
            record["desc"] = "ask"
        if i == 3:
            record["desc"] = "askvolume"
        for td in tdr:
            k = k + 1
            if k == 2:
                if td.text == "-":
                    record["value"] = 0
                else:
                    record["value"] = td.text
                scraperwiki.sqlite.save(["desc"], record)
        i = i + 1

def scrape_for_info(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)

starting_url = 'http://www.profiledata.co.za/moneyweb/sharedata/data/010023/TradingData_DRN.htm'
#starting_url = 'http://www.profiledata.co.za/moneyweb/sharedata/data/009406/TradingData_HUG.htm'
scrape_for_info(starting_url)