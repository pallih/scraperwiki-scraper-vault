import scraperwiki
import lxml.html

server = "http://boston-iframe.r.mikatiming.de/2013/"
page = scraperwiki.sqlite.get_var("page");
page += 1
html = scraperwiki.scrape(server + "?pid=search&num_results=1000&page=" + str(page))
           
root = lxml.html.fromstring(html)

for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==9:
        td = tds[3].cssselect("a")[0]

        nameandcountry = td.text_content()
        nameandcountry = nameandcountry.replace(")","").split("(");
        name = nameandcountry[0]
        country = nameandcountry[1]

        query = td.get("href")
        querysplit = query.split("idp=")
        querysplit = querysplit[1].split("&");
        id = querysplit[0];

        scraperwiki.sqlite.save(unique_keys=["id"], data={'id' : id,'name' : name,'country' : country,'query' : query})

scraperwiki.sqlite.save_var("page",page);import scraperwiki
import lxml.html

server = "http://boston-iframe.r.mikatiming.de/2013/"
page = scraperwiki.sqlite.get_var("page");
page += 1
html = scraperwiki.scrape(server + "?pid=search&num_results=1000&page=" + str(page))
           
root = lxml.html.fromstring(html)

for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==9:
        td = tds[3].cssselect("a")[0]

        nameandcountry = td.text_content()
        nameandcountry = nameandcountry.replace(")","").split("(");
        name = nameandcountry[0]
        country = nameandcountry[1]

        query = td.get("href")
        querysplit = query.split("idp=")
        querysplit = querysplit[1].split("&");
        id = querysplit[0];

        scraperwiki.sqlite.save(unique_keys=["id"], data={'id' : id,'name' : name,'country' : country,'query' : query})

scraperwiki.sqlite.save_var("page",page);