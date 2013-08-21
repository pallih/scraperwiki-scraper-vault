import scraperwiki
import urlparse
import lxml.html
import dateutil.parser as dparser
import re

def scrape_table(root):
    items = root.cssselect("#content div.item")

    for item in items:
        record = {}

        h2 = item.cssselect("h2")[0]
        link = h2.cssselect("a")[0]
        link_text = re.sub(r' ze dne .*', '', link.text)

        id = record["id"] = int(link_text.split(' ')[-1])
        record["name"] = h2.text_content().split(" | ")[-1]
        record["text_url"] = urlparse.urljoin( base_url, link.get("href"))
        record["date"] = dparser.parse(str(h2.cssselect(".subh")[0].text.split("|")[0]), fuzzy=True, dayfirst=True)

        scraperwiki.sqlite.save(["id"], record, table_name="usneseni")

        # Prehled hlasovani
        voting = {}
        vote_page = get_voting(id)
        if not vote_page:
            return
        rows = vote_page.cssselect("#content .body-text table tbody tr")

        for row in rows:
            tds= row.cssselect("td")
            voting["councilor"] = row.cssselect("th")[0].text
            voting["party"] = tds[0].text
            voting["voted"] = tds[1].text
            voting["usneseni_id"] = id

            scraperwiki.sqlite.save(["usneseni_id","councilor"], voting, table_name="voting")            

        
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.link-next")
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        scrape_and_look_for_next_link(next_url)


def get_voting(id):
    root = False
    slug = "ZMC-" + current_year + "-" + str(id) + ".html"
    url = urlparse.urljoin(base_url, slug)
    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    except:
        pass
    
    return root

current_year = ""    
for year in ["2012","2013"]:
    current_year = year
    base_url = "http://www.praha3.cz/volene-organy/zastupitelstvo/usneseni/x" + year + "/"
    starting_url = urlparse.urljoin(base_url, 'index.html')
    scrape_and_look_for_next_link(starting_url)

#for year in ["2010","2011"]:
#    for month in ["leden","unor"]:
#        base_url = "http://www.praha3.cz/volene-organy/zastupitelstvo/usneseni/x" + year + "/" + month + "/"
#        starting_url = urlparse.urljoin(base_url, 'index.html')
#        scrape_and_look_for_next_link(starting_url)

