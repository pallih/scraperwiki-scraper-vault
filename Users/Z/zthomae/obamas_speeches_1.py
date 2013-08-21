import scraperwiki
import lxml.html
import mechanize

BASE_URL = 'http://www.whitehouse.gov/briefing-room/speeches-and-remarks'
PAGE_STRIDE = 20

def scrape(last_page):
    has_page = True
    old_first = scraperwiki.sqlite.get_var('first_link')
    br = mechanize.Browser()
    response = br.open("%s?page=%d" % (BASE_URL, last_page))
    # TODO: This breaks if there are more than twenty pages between new_first and old_first
    if not last_page:
        new_first = br.links(url_regex='/the-press-office/').next().url # HACKETY HACK HACK
        scraperwiki.sqlite.save_var('first_link', new_first)
    pages_left = PAGE_STRIDE
    while has_page and pages_left:
        links = []
        for l in br.links(url_regex='/the-press-office/'):
            links.append(l) # HACKETY HACK HACK
        for l in links:
            if l.url == old_first:
                return -1
            page = br.follow_link(l)
            html = page.read()
            root = lxml.html.fromstring(html)
            # Things we've already seen will be pushed onto later pages. Just overwrite them.
            record = {'url': page.geturl(), 'text': root.cssselect('#content')[0].text_content()}
            scraperwiki.sqlite.save(unique_keys=['url'], data=record)
            back = br.back()
        try:
            link = br.find_link(text_regex='next')
            br.follow_link(link)
            pages_left -= 1
        except mechanize.LinkNotFoundError:
            has_page = False
            pages_left = -1
    return pages_left

def main():
    last_page = scraperwiki.sqlite.get_var('last_page')
    if not last_page:
        last_page = 0
    pages_left = scrape(last_page)
    if pages_left == -1:
        scraperwiki.sqlite.save_var('last_page', 0)
    else:
        scraperwiki.sqlite.save_var('last_page', last_page+(PAGE_STRIDE-pages_left))

main()