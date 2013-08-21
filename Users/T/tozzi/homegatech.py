import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    i = 0
    tds = soup.findAll('tr') # get all the <td> tags
    for tr in tds:
        k = 0
        record = {}
        tdr = tr.findAll('td') # get all the <td> tags
        i = i + 1
        record["i"] = i
        for td in tdr:
            k = k + 1
            if k == 4:
                record["address"] = td.text
            if k == 5:
                record["detail"] = td.text
            if k == 6:
                record["price"] = td.text
        print record
        scraperwiki.datastore.save(["i"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("a", { "class" : "forward iconLink" })
    #if next_link:
    #    next_url = next_link['href']
    #    scrape_and_look_for_next_link(next_url)

starting_url = 'http://www.homegate.ch/kaufen/wohnung/bezirk-zuerich/trefferliste?a=default&tab=list&l=default&cid=3032967&aj=900000&ep=1&incsubs=default&tid=1&fromItem=ctn_zh'
scrape_and_look_for_next_link(starting_url)
