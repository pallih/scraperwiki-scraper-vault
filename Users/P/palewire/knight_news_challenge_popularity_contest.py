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
        # Get the total number of likes
        likes = entry.find("", "home-likes")
        if likes and likes.text:
            likes = int(likes.text)
        else:
            likes = 0
        # Get the total number of comments (which is not currently working)
        comments = entry.find("", "home-comments")
        if comments and comments.text:
            comments = int(comments.text)
        else:
            comments = 0
        # Get the title
        title = entry.find("h2")
        if title:
            title = title.text
        # Get the URL
        url = entry.find('a', "home-view")
        if url:
            url = url.get('href')
        if url == 'http://newschallenge.tumblr.com/post/30409290920/knight-news-challenge-on-mobile-now-open-for-apps':
            continue
        # Only record active entries
        data = {
            'likes': likes,
            'comments': comments,
            'total': likes + comments,
            'title': title,
            'url': url,
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
