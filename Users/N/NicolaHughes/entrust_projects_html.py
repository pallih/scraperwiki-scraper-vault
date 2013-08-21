import scraperwiki

scraperwiki.sqlite.attach("entrust")

all = scraperwiki.sqlite.select("URL from entrust.swdata")
all_urls = [row["URL"] for row in all]

done = scraperwiki.sqlite.select("URL from swdata")
done_urls = [row["url"] for row in done]

todo_urls = set(all_urls) - set(done_urls)

for url in todo_urls:
    html = scraperwiki.scrape(url)
    data = {"url": url, "html": html}
    scraperwiki.sqlite.save(["url"], data)

