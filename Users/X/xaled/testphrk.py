import scraperwiki


# Blank Python



html = scraperwiki.scrape("http://www.phrack.org/issues.html")


print html
for i in range(1,1000):
    url = "issues.html?issue="+str(i)
    if url in html:
        print url
        data = {"id": str(i), "link" : "http://www.phrack.org/"+url}
        scraperwiki.sqlite.save(data=data, unique_keys=['id'])
    else:
        break
import scraperwiki


# Blank Python



html = scraperwiki.scrape("http://www.phrack.org/issues.html")


print html
for i in range(1,1000):
    url = "issues.html?issue="+str(i)
    if url in html:
        print url
        data = {"id": str(i), "link" : "http://www.phrack.org/"+url}
        scraperwiki.sqlite.save(data=data, unique_keys=['id'])
    else:
        break
