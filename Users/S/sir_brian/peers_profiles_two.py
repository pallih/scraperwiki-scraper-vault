import scraperwiki
from bs4 import BeautifulSoup

search_page = "http://news.bbc.co.uk/democracylive/hi/representatives/search?type=representatives&institution=House%20of%20Lords&start="

html = scraperwiki.scrape(search_page)

soup = BeautifulSoup(html)

for n in range (1, 91):
    page = search_page +  str(n)
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)

    all_on_page = soup.find_all("a", "name")

    for each in all_on_page:
        link = each["href"]
        from lxml import html
        from urllib import urlopen
        fh = urlopen(link)
        document = html.parse(fh).getroot()
        if document.cssselect('span.fn'):
            title = document.cssselect('span.fn')[0].text.strip()
            list_check_1 = ["lord", "baroness"]
            if any(word in title.lower() for word in list_check_1):
                data = { "Name": title, "URL": link }
                rest = document.cssselect('li.li-c span, li.li-e span')           
                if (len(rest) > 0):
                    for j in range(0, len(rest)):
                        data['%d' % (j+2)] = rest[j].text.strip()
                scraperwiki.sqlite.save(["Name"], data)
