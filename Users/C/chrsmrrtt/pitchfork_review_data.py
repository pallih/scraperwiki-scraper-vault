import scraperwiki, lxml.html, re, datetime

page = 1

def getReviewIndexUrl():
    return 'http://pitchfork.com/reviews/albums/{0}/'.format(page)

def scrapePage(url):
    html = None
    attempts = 0

    while html == None and attempts < 3:
        try: html = scraperwiki.scrape(url)
        except:
            attempts += 1
            continue

        if html == None and attempts == 3:
            print 'Unable to scrape ' + review_href
    
    return html

while page < 3:
    print page

    review_index_html = scrapePage(getReviewIndexUrl())

    if review_index_html is None: continue

    review_index_tree = lxml.html.fromstring(review_index_html)
    
    review_links = review_index_tree.cssselect('div#main ul.object-grid a[href^="/reviews/albums/"]')
    
    for review_link in review_links:
        review_href = 'http://pitchfork.com' + review_link.attrib['href']

        review_html = scrapePage(review_href)

        if review_html is None: continue
        
        review_tree = lxml.html.fromstring(review_html)
        
        if len(review_tree.cssselect('div#main div.info h1')) == 0: continue
        
        artist = review_tree.cssselect('div#main div.info h1')[0].text_content()
        album = review_tree.cssselect('div#main div.info h2')[0].text_content()
        reviewer = review_tree.cssselect('div#main div.info h4 address')[0].text_content()
        score = review_tree.cssselect('div#main div.info span.score')[0].text_content()
        
        publish_date = review_tree.cssselect('div#main div.info span.pub-date')[0].text_content()
        publish_date = datetime.datetime.strptime(publish_date, '%B %d, %Y')
        publish_date = publish_date.strftime('%Y-%m-%d')
        
        accolade = None
        if len(review_tree.cssselect('div.bnm-label')) > 0:
            accolade = review_tree.cssselect('div.bnm-label')[0].text_content()

        label, release_year = None, None
        label_and_release_year = review_tree.cssselect('div#main div.info h3')[0].text_content()
        label_and_release_year_regex = re.search(r'(.*); (\d{4})', label_and_release_year)
        if label_and_release_year_regex:
            label, release_year = label_and_release_year_regex.group(1, 2)
    
        data = {
            'artist': artist,
            'album': album,
            'label': label,
            'release_year': release_year,
            'reviewer': reviewer,
            'score': score,
            'accolade': accolade,
            'publish_date': publish_date,
            'url': review_href
        }

        scraperwiki.sqlite.save(['url'], data)
    
    page += 1
