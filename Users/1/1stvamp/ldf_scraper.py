import scraperwiki
from BeautifulSoup import BeautifulSoup as soup

urls = (
('event', 'http://www.leedsdigitalfestival.com/'),
('about', 'http://www.leedsdigitalfestival.com/about/'),
('news', 'http://www.leedsdigitalfestival.com/news/'),
('video', 'http://www.leedsdigitalfestival.com/video/'),
('location', 'http://www.leedsdigitalfestival.com/locations/'),
('resource', 'http://www.leedsdigitalfestival.com/resources/'),
)

data = []
for content_type, url in urls:
    s = soup(scraperwiki.scrape(url))
    page = s.find('div', 'page')
    for block in page.findAll('div', 'block'):
        if 'small_footer' in block['class'].split(' '):
            continue
        title = block.find('div', {'class': 'post-title'})
        title = title and title.h2.text
        ps = block.findAll('p')
        dt = ''
        venue = ''
        by = ''
        if hasattr(ps[0], 'span') and ps[0].span:
            dt = ps[0].span.text
            _venue = ps[0].text.replace(dt, '')
            if _venue.startswith('by '):
                by = _venue
            else:
                venue = _venue 
        summary = ''
        if len(ps) > 1:
            summary = str(ps[1].p)
        if not title and not summary:
            continue
        more_link = block.find('a', 'more')
        content = ''
        if more_link:
            more_page = soup(scraperwiki.scrape("%s%s" % (url, more_link['href'],)))
            ps = more_page.find('div', 'page').find('div', 'block').findAll('p')
            content = "\n".join(str(p) for p in ps[1:])
        data.append({'type': content_type, 'title': title, 'dt': dt, 'venue': venue, 'summary': summary, 'content': content, 'by': by})
scraperwiki.sqlite.save(['type', 'title'], data)