import scraperwiki
import re

sourcescraper = 'bbc_news_japan_live_blog'

scraperwiki.sqlite.attach(sourcescraper) 

lines = scraperwiki.sqlite.select('* from `bbc_news_japan_live_blog`.swdata')

print "<ol id='bbc-news-japan-live-blog-lines'>"

for line in lines:
    if (line['text']):
        time = re.sub("[^\d]", "", line['time'])
        print "<li class='bbc-news-japan-live-blog-line'><time>" + time + "</time> " + line['text'] + "</li>"

print "</ol>"

