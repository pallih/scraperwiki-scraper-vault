import scraperwiki
import scraperwiki.apiwrapper
import lxml.html

def do_day(rec):    
    html = scraperwiki.scrape(rec['url']).decode("iso-8859-1")
    root = lxml.html.fromstring(html)
    intro = root.cssselect('div#castaway_intro h1')

    # Check for unexpected page format
    if intro == None:
        print "skipping, no <div id='castaway_intro'>, page format has changed?"
        return
    castaway = intro[0].text_content()
    print 'Castaway: ',castaway


    #div.castaway-choice

    for choice in root.cssselect('div.castaway-choice'):
        text = choice.cssselect('div.text')[0]
        num = text.cssselect('p.number')[0].text_content()
        #print lxml.html.tostring(text)
        # Sanity check number?
        artist = text.cssselect('h4')[0].text_content()
        # extract artist musicbrainz id if available
        link = text.cssselect('h4 a') # need to parse link attribute url
        if link:
            mb_id = link[0].attrib['href'].split('/')[-1]
        track = text.cssselect('p.track_choice')[0].text_content()
        composer = text.cssselect('p.composer')[0].text_content() # really the artist! 

        if composer:
            tmp = composer
            composer = artist
            artist = tmp
            # need to swap MB id too

        newrec = rec.copy()
        newrec['type'] = 'record'
        newrec['title'] = track
        newrec['performer'] = artist

        print newrec
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], newrec) 

    book = root.cssselect('div.book-item')
    if book:
        title = book[0].cssselect('h5.book_choice')[0].text_content()
        newrec = rec.copy()
        newrec['type'] = 'book'
        newrec['title'] = title
        print title
        newrec['performer'] = None
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], newrec)

    luxury = root.cssselect('div.luxury-item')
    if luxury:
        item = luxury[0].cssselect('h5.luxury_item_choice')[0].text_content()
        newrec = rec.copy()
        newrec['type'] = 'luxury'
        print item
        newrec['title'] = item
        newrec['performer'] = None
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], newrec)

# Not sure what this section was extracting
#        found = re.search('Record:\s*([^<]+)<', s)
#        if found:
#            bookrec = rec.copy()
#            bookrec['type'] = 'keep_record'
#            bookrec['title'] = str(found.groups(1)[0]).strip()
#            bookrec['performer'] = None
#            scraperwiki.sqlite.save(["date", "guest", "type", "title"], bookrec)

        #print s
    
#scraperwiki.sqlite.save(["td"], record) wi

#data = scraperwiki.apiwrapper.getData('desert-island-disc-broadcasts', limit=-1, offset=0)
scraperwiki.sqlite.attach('desert-island-disc-broadcasts') 
data = scraperwiki.sqlite.select('* from `desert-island-disc-broadcasts`.swdata')

for rec in data:
    print "-----------------------------------"
    print rec['url']
    do_day(rec)

# Test record:
#rec = {'guest': 'Anne Scott-James', 'url': 'http://www.bbc.co.uk/radio4/factual/desertislanddiscs_20041010.shtml', 'date': '2004-10-10'}
#do_day(rec)

