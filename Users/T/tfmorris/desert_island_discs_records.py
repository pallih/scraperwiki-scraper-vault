# Scrape BBC Desert Island Discs data including songs, books, and luxury item, if available, for the celebrity "castaways"
# based on original work by Francis Irving with the following changes by Tom Morris July 2012:
#  - updated to current BBC page format
#  - switched from BeautifulSoup to lxml
#  - updated deprecated database calls
#  - restructured to run as a single integrated process and not rescrape data it already extracted

import scraperwiki
import scraperwiki.apiwrapper
import lxml.html
from datetime import datetime

SITE = 'http://www.bbc.co.uk'
BASE = SITE + '/radio4/features/desert-island-discs/find-a-castaway'

if scraperwiki.sqlite.show_tables():
    past = [(i['date'],i['guest']) for i in scraperwiki.sqlite.select("* from swdata WHERE type == 'url'")]
else:
    past = []
print 'Database contains %d past entries' % len(past)

def process_guest(date, name, occupation, url):
    if (date,name) in past:
        # print 'Skipping %s %s' % (date,name)
        return False
    html = scraperwiki.scrape(url).decode("utf-8")
    root = lxml.html.fromstring(html)
    intro = root.cssselect('div#castaway_intro h1')

    # Check for unexpected page format
    if intro == None:
        print "skipping, no <div id='castaway_intro'>, page format has changed? ",url
        return

    # Denormalized schema, but that's a little easier for consumers
    # Old schema - Pass1: date date_scraped url guest
    # Pass2: date_scraped guest title url date type performer
    # old record types: record keep_record book luxury
    rec = {'date_scraped' : datetime.now(),
           'date':date,
           'guest':name,
           'type':'occupation',
           'title':occupation,
           }
    scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    castaway = intro[0].text_content()
    if not castaway == name:
        print 'Mismatched names between index (%s) and detail page (%s)' % (name,castaway)
        rec = {'date':date,
               'guest':name,
               'type':'alternate_name',
               'title':castaway,
               }
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    # TODO It would be more efficient to only fetch the page once for all broadcasts, 
    # but we sacrifice a small amount of efficiency for the rare cast to better fit with our control flow

    broadcast_id = url.split('#')[-1]
    broadcast = root.cssselect('div#'+broadcast_id)
    # The first broadcast doesn't appear to be tagged with an ID (even though the URL references it)
    # so default to using the first broadcast that we find
    if not broadcast:
        #print 'Failed to find broadcast by ID.  Using default'
        broadcast=root.cssselect('div.castaway-content')
    broadcast = broadcast[0]

    # Track choices
    for choice in broadcast.cssselect('div.castaway-choice'):
        text = choice.cssselect('div.text')[0]
        num = text.cssselect('p.number')[0].text_content()
        #print lxml.html.tostring(text)
        # Sanity check number?
        keep = text.cssselect('p.track_keep') # Only present if it's their favorite track
        artist = text.cssselect('h4')[0].text_content()
        # extract artist musicbrainz id if available
        link = text.cssselect('h4 a') # need to parse link attribute url
        if link:
            mb_id = link[0].attrib['href'].split('/')[-1]
        else:
            mb_id = None
        track = text.cssselect('p.track_choice')[0].text_content()
        composer = text.cssselect('p.composer')[0].text_content() # not necessarily the composer

        principal = 'artist'
        if composer:
            if composer.startswith('Composer: '):
                composer = composer.split('Composer: ')[1]
            else:
                principal = 'composer'
                tmp = composer
                composer = artist
                if tmp.startswith('Artist: '):
                    artist = tmp.split('Artist: ')[1]
                else:
                    artist = tmp

        rec.update({'type': 'record_keep' if keep else 'record',
                    'title' : track,
                    'performer' : artist,
                    'composer' : composer,
                    'principal' : principal,
                    'mb_id' : mb_id,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    # Clear music specific fields
    rec.update({'performer' : None,
                'composer' : None,
                'principal' : None,
                'mb_id' : None,
                 })

    book = broadcast.cssselect('div.book-item')
    if book:
        title = book[0].cssselect('h5.book_choice')[0].text_content()
        rec.update({'type': 'book',
                    'title' : title,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec)

    luxury = broadcast.cssselect('div.luxury-item')
    if luxury:
        item = luxury[0].cssselect('h5.luxury_item_choice')[0].text_content()
        rec.update({'type': 'luxury',
                    'title' : item,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec)

    # URL record must be written last because it's the key we use to determine record is complete
    rec = {'date':date,
           'guest':name,
           'type':'url',
           'title':url,
           }
    scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 
    return True

def process_index_page(pg):
    items = pg.cssselect('div.search-item')
    # print 'Index page has %d items' % len(items)
    count = 0
    for item in items:
        text = item.cssselect('div.text')
        if not text:
            print 'Unable to process item - no text div'
            continue
        text = text[0]
        guest = text.cssselect('h4 a')
        if not guest:
            print 'Unabled to find guest name'
            continue
        guest = guest[0]
        guest_url = SITE + guest.attrib['href']
        guest_name = guest.text_content()
        date = text.cssselect('p.date')
        if not date:
            print 'Unable to find broadcast date for guest "%s"' % guest_name
            continue
        date = date[0].text_content().split('|')[1].strip()
        # Convert date to ISO format
        date = datetime.strptime(date,'%d %b %Y').strftime('%Y-%m-%d')
        occupation = text.cssselect('p')
        if len(occupation) > 1:
            occupation = occupation[1].text_content()
        else:
            occupation = ''
        #print date, guest_name, occupation, guest_url
        if process_guest(date, guest_name, occupation, guest_url):
            count += 1
    print 'Processed %d of %d shows' % (count,len(items))
    return count

def fetch_index_page(page_num):
    print 'Fetching index page %d' % page_num
    page_html = scraperwiki.scrape(BASE + '/page/' + str(page_num))
    return lxml.html.fromstring(page_html)
        
def main():
    index_html = scraperwiki.scrape(BASE).decode("utf-8")
    index = lxml.html.fromstring(index_html)
    episode_count = int(index.cssselect('p#search-found span')[0].text_content().split(' ')[0])
    print '%d total episodes' % episode_count
    pages = index.cssselect('ul.pages li a')
    last_index_page = int(pages[-2].text_content())
    print '%d index pages' % last_index_page
    
    count = process_index_page(index) # handle the first page
    for page_num in range(2,last_index_page+1):
        page = fetch_index_page(page_num)
        count += process_index_page(page)
    print 'Processed %d new entries' % count

def test():
    # Test multiple appearances
    print process_guest('1980-12-20','Arthur Askey','Comedian, Music hall','http://www.bbc.co.uk/radio4/features/desert-island-discs/castaway/663e79cf#p009mvl6')
    print process_guest('1942-04-02','Arthur Askey','Comedian','http://www.bbc.co.uk/radio4/features/desert-island-discs/castaway/663e79cf#p009y0mc')
    # Test index pages without dates
    page = fetch_index_page(96)
    process_index_page(page)

main()
#test()# Scrape BBC Desert Island Discs data including songs, books, and luxury item, if available, for the celebrity "castaways"
# based on original work by Francis Irving with the following changes by Tom Morris July 2012:
#  - updated to current BBC page format
#  - switched from BeautifulSoup to lxml
#  - updated deprecated database calls
#  - restructured to run as a single integrated process and not rescrape data it already extracted

import scraperwiki
import scraperwiki.apiwrapper
import lxml.html
from datetime import datetime

SITE = 'http://www.bbc.co.uk'
BASE = SITE + '/radio4/features/desert-island-discs/find-a-castaway'

if scraperwiki.sqlite.show_tables():
    past = [(i['date'],i['guest']) for i in scraperwiki.sqlite.select("* from swdata WHERE type == 'url'")]
else:
    past = []
print 'Database contains %d past entries' % len(past)

def process_guest(date, name, occupation, url):
    if (date,name) in past:
        # print 'Skipping %s %s' % (date,name)
        return False
    html = scraperwiki.scrape(url).decode("utf-8")
    root = lxml.html.fromstring(html)
    intro = root.cssselect('div#castaway_intro h1')

    # Check for unexpected page format
    if intro == None:
        print "skipping, no <div id='castaway_intro'>, page format has changed? ",url
        return

    # Denormalized schema, but that's a little easier for consumers
    # Old schema - Pass1: date date_scraped url guest
    # Pass2: date_scraped guest title url date type performer
    # old record types: record keep_record book luxury
    rec = {'date_scraped' : datetime.now(),
           'date':date,
           'guest':name,
           'type':'occupation',
           'title':occupation,
           }
    scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    castaway = intro[0].text_content()
    if not castaway == name:
        print 'Mismatched names between index (%s) and detail page (%s)' % (name,castaway)
        rec = {'date':date,
               'guest':name,
               'type':'alternate_name',
               'title':castaway,
               }
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    # TODO It would be more efficient to only fetch the page once for all broadcasts, 
    # but we sacrifice a small amount of efficiency for the rare cast to better fit with our control flow

    broadcast_id = url.split('#')[-1]
    broadcast = root.cssselect('div#'+broadcast_id)
    # The first broadcast doesn't appear to be tagged with an ID (even though the URL references it)
    # so default to using the first broadcast that we find
    if not broadcast:
        #print 'Failed to find broadcast by ID.  Using default'
        broadcast=root.cssselect('div.castaway-content')
    broadcast = broadcast[0]

    # Track choices
    for choice in broadcast.cssselect('div.castaway-choice'):
        text = choice.cssselect('div.text')[0]
        num = text.cssselect('p.number')[0].text_content()
        #print lxml.html.tostring(text)
        # Sanity check number?
        keep = text.cssselect('p.track_keep') # Only present if it's their favorite track
        artist = text.cssselect('h4')[0].text_content()
        # extract artist musicbrainz id if available
        link = text.cssselect('h4 a') # need to parse link attribute url
        if link:
            mb_id = link[0].attrib['href'].split('/')[-1]
        else:
            mb_id = None
        track = text.cssselect('p.track_choice')[0].text_content()
        composer = text.cssselect('p.composer')[0].text_content() # not necessarily the composer

        principal = 'artist'
        if composer:
            if composer.startswith('Composer: '):
                composer = composer.split('Composer: ')[1]
            else:
                principal = 'composer'
                tmp = composer
                composer = artist
                if tmp.startswith('Artist: '):
                    artist = tmp.split('Artist: ')[1]
                else:
                    artist = tmp

        rec.update({'type': 'record_keep' if keep else 'record',
                    'title' : track,
                    'performer' : artist,
                    'composer' : composer,
                    'principal' : principal,
                    'mb_id' : mb_id,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 

    # Clear music specific fields
    rec.update({'performer' : None,
                'composer' : None,
                'principal' : None,
                'mb_id' : None,
                 })

    book = broadcast.cssselect('div.book-item')
    if book:
        title = book[0].cssselect('h5.book_choice')[0].text_content()
        rec.update({'type': 'book',
                    'title' : title,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec)

    luxury = broadcast.cssselect('div.luxury-item')
    if luxury:
        item = luxury[0].cssselect('h5.luxury_item_choice')[0].text_content()
        rec.update({'type': 'luxury',
                    'title' : item,
                    })
        scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec)

    # URL record must be written last because it's the key we use to determine record is complete
    rec = {'date':date,
           'guest':name,
           'type':'url',
           'title':url,
           }
    scraperwiki.sqlite.save(["date", "guest", "type", "title"], rec) 
    return True

def process_index_page(pg):
    items = pg.cssselect('div.search-item')
    # print 'Index page has %d items' % len(items)
    count = 0
    for item in items:
        text = item.cssselect('div.text')
        if not text:
            print 'Unable to process item - no text div'
            continue
        text = text[0]
        guest = text.cssselect('h4 a')
        if not guest:
            print 'Unabled to find guest name'
            continue
        guest = guest[0]
        guest_url = SITE + guest.attrib['href']
        guest_name = guest.text_content()
        date = text.cssselect('p.date')
        if not date:
            print 'Unable to find broadcast date for guest "%s"' % guest_name
            continue
        date = date[0].text_content().split('|')[1].strip()
        # Convert date to ISO format
        date = datetime.strptime(date,'%d %b %Y').strftime('%Y-%m-%d')
        occupation = text.cssselect('p')
        if len(occupation) > 1:
            occupation = occupation[1].text_content()
        else:
            occupation = ''
        #print date, guest_name, occupation, guest_url
        if process_guest(date, guest_name, occupation, guest_url):
            count += 1
    print 'Processed %d of %d shows' % (count,len(items))
    return count

def fetch_index_page(page_num):
    print 'Fetching index page %d' % page_num
    page_html = scraperwiki.scrape(BASE + '/page/' + str(page_num))
    return lxml.html.fromstring(page_html)
        
def main():
    index_html = scraperwiki.scrape(BASE).decode("utf-8")
    index = lxml.html.fromstring(index_html)
    episode_count = int(index.cssselect('p#search-found span')[0].text_content().split(' ')[0])
    print '%d total episodes' % episode_count
    pages = index.cssselect('ul.pages li a')
    last_index_page = int(pages[-2].text_content())
    print '%d index pages' % last_index_page
    
    count = process_index_page(index) # handle the first page
    for page_num in range(2,last_index_page+1):
        page = fetch_index_page(page_num)
        count += process_index_page(page)
    print 'Processed %d new entries' % count

def test():
    # Test multiple appearances
    print process_guest('1980-12-20','Arthur Askey','Comedian, Music hall','http://www.bbc.co.uk/radio4/features/desert-island-discs/castaway/663e79cf#p009mvl6')
    print process_guest('1942-04-02','Arthur Askey','Comedian','http://www.bbc.co.uk/radio4/features/desert-island-discs/castaway/663e79cf#p009y0mc')
    # Test index pages without dates
    page = fetch_index_page(96)
    process_index_page(page)

main()
#test()