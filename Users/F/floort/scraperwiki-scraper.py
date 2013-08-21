import scraperwiki
import lxml.html

page_num = 1
max_page = 1
while True:
    html = scraperwiki.scrape("https://scraperwiki.com/browse/scrapers/?page=%d" % (page_num))
    page = lxml.html.fromstring(html) 
        
    navAnchors = page.cssselect("div.pagination a")
    max_page = int(navAnchors[len(navAnchors) - 2].text)
    for project in page.cssselect("li.code_object_line"):
        proj = project.cssselect("h3 a")[1]
        proj_name = proj.text
        proj_id = proj.attrib["href"].split("/")[-2]
    
        author = project.cssselect("h3 a.owner")[0].text
        status = project.cssselect("tr.status td.link")[0].text
        proj_lang = project.cssselect("tr.language td.link a")[0].text
        #code_page = BeautifulSoup(scraperwiki.scrape("http://scraperwiki.com/scrapers/%s/edit/" % (proj_id)))
        #proj_code = code_page.find("textarea", {"id":"id_code"}).string
        proj_code = scraperwiki.scrape("https://scraperwiki.com/editor/raw/%s" % (proj_id))
        record = {
            "id" : proj_id,
            "name" : proj_name,
            "lang" : proj_lang,
            "code" : proj_code,
            "author" : author,
            "status" : status 
        }
        scraperwiki.sqlite.save(["id"], record)
    if max_page == page_num: break
    page_num += 1 
        