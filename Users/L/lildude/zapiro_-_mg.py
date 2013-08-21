import scraperwiki
import lxml.html 
import datetime


html = scraperwiki.scrape("http://mg.co.za/zapiro/")
root = lxml.html.fromstring(html)

title = root.cssselect("li.last_crumb a")[0].text_content()
link = root.cssselect("div#cartoon a")[0].attrib['href']
cartoon = root.cssselect("div#cartoon_full_size img")[0].attrib['src']

now = datetime.datetime.now()

data = {
    'link': link,
    'title': "Zapiro:" + title,
    'description': '<img src="'+cartoon+'" border="0" /><br /><br />Like Zapiro? Then check out my <a href="http://feeds.feedburner.com/MadamEve">Unofficial Madam &amp; Eve Feed</a>. All Madam &amp; Eve cartoons are taken directly from the <a href="http://www.madamandeve.co.za">official website</a> as it is updated.',
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)