import scraperwiki
import lxml.html

items = [
"http://www.stadtbranchenbuch.com/ludwigsburg/S/393.html",
"http://www.stadtbranchenbuch.com/flensburg/S/393.html",
"http://www.stadtbranchenbuch.com/cottbus/S/393.html",
"http://www.stadtbranchenbuch.com/wilhelmshaven/S/393.html",
"http://www.stadtbranchenbuch.com/tuebingen/S/393.html",
"http://www.stadtbranchenbuch.com/minden/S/393.html"
]

def store_data(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for div in root.cssselect("ul.rLi li"):

        company= div.cssselect("div.rLiTop h3 a")
        if company:
            company= company[0].text
        else:
            company= ""

        phone= div.cssselect("div.rLiTop address span.tel")
        if phone:
            phone= phone[0].text
        else:
            phone= ""

        address= div.cssselect("div.rLiTop address span")
        if address:
            address= address[0].text
        else:
            address= ""

        branch= div.cssselect("div h4")
        if branch:
            branch= branch[0].text
        else:
            branch= ""

        website= div.cssselect("li ul li a.fh")
        if website:
            website= website[0].attrib['href'][7:]
        else:
            website= ""

        if phone:
            data = {
                "company": company,
                "phone": phone,
                "address": address,
                "branch": branch,
                "website": website
            }
            scraperwiki.sqlite.save(unique_keys=['phone'], data=data)


for item in items:
    store_data(item)
