"""
Logs the popularity of entries in the Knight News Challenge.
http://newschallenge.tumblr.com/

Based on a gist published by Samuel Clay.
https://gist.github.com/2151484
"""
import scraperwiki
from BeautifulSoup import BeautifulSoup

page = 1
while True:
    print "Scraping page %s" % ( page)
    # Fetch the URLs, page by page
    page_url = "http://newschallenge.tumblr.com/page/%s" % (page)
    html = scraperwiki.scrape(page_url)
    soup = BeautifulSoup(html)
    postboxes = soup.findAll("div", "postbox")
    # Done if only sticky entry is left.
    if len(postboxes) <= 1:
        break
    # Up the page count after a fetch
    page += 1

    # 15 entries per page, plus a sticky throwaway entry
    for entry in postboxes:

        # Skip the sticky entries
        if 'stickyPost' in entry.get('class'):
            continue
        # Get the title
        title = entry.find("h2")
        if title:
            title = title.text
        # Get the URL
        url = entry.find('a', "home-view")
        if url:
            url = url.get('href')
            entryHTML = scraperwiki.scrape(url)
            entrySoup = BeautifulSoup(entryHTML)
            likes = len(entrySoup.findAll("li","like"))
            reblogs = len(entrySoup.findAll("li","reblog"))
            try:
                # the number of comments is disqus javascript?
                comments = float(entrySoup.findAll("span","dsq-num-posts")[0].contents) 
            except IndexError:
                comments = 0
            
        if url == 'http://newschallenge.tumblr.com/post/24130238607/knight-news-challenge-data-is-now-open':
            continue
        # Only record active entries
        data = {
            'likes': likes,
            'comments': comments,
            "reblogs": reblogs,
            'total': likes + reblogs + comments,
            'title': title,
            'url': url,
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
