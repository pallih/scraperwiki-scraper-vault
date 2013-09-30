import scraperwiki
import lxml.html

BASE_URL = "http://www.tdcj.state.tx.us/death_row/"
IMG_URL = "http://www.tdcj.state.tx.us/death_row/dr_info/"

def scrape_img_urls():
    iteration = 0
    html = scraperwiki.scrape(BASE_URL + "dr_executed_offenders.html")
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#start_main_content table tr"):
        tds = tr.cssselect("td")
        if not tds:
            continue
        info_link = tds[1].cssselect("a")
        if info_link:
            info_url = info_link[0].get("href")
            info_url_match = info_url[len(info_url)-4:]
            if info_url_match == ".jpg":
                data = {
                    'execution_no': tds[0].text_content(),
                    'tdcj_no': tds[5].text_content(),
                    'img_link': info_url
                }
                print data
                iteration += 1
                scraperwiki.sqlite.save(unique_keys=['execution_no'], data=data)
    print iteration

scrape_img_urls()import scraperwiki
import lxml.html

BASE_URL = "http://www.tdcj.state.tx.us/death_row/"
IMG_URL = "http://www.tdcj.state.tx.us/death_row/dr_info/"

def scrape_img_urls():
    iteration = 0
    html = scraperwiki.scrape(BASE_URL + "dr_executed_offenders.html")
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#start_main_content table tr"):
        tds = tr.cssselect("td")
        if not tds:
            continue
        info_link = tds[1].cssselect("a")
        if info_link:
            info_url = info_link[0].get("href")
            info_url_match = info_url[len(info_url)-4:]
            if info_url_match == ".jpg":
                data = {
                    'execution_no': tds[0].text_content(),
                    'tdcj_no': tds[5].text_content(),
                    'img_link': info_url
                }
                print data
                iteration += 1
                scraperwiki.sqlite.save(unique_keys=['execution_no'], data=data)
    print iteration

scrape_img_urls()