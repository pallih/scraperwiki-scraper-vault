import scraperwiki
from datetime import datetime, date, time
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

# from to day
date_start = datetime.now().strftime('%d.%m.%Y')
print "Retrieving from " + date_start

# retrieve rss
starting_url = 'http://www.berlin.de/land/kalender/index.php?rss&c=22&kategorie[8]=7&date_start=' + date_start
html = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(html)

# use BeautifulStoneSoup to get all <item> tags
items = soup.findAll('item')
# for item in items:

print "Found " + str(len(items)) + "  item(s)"
total_rows = count = 0
for item in items:         
    count = count + 1 
    link = item.link.text
    # scrape additional data from the detail page
    detail_page = BeautifulSoup( scraperwiki.scrape(link) );

    # the details are wrapped in <dd>s, sigh
    dds = detail_page.findAll('dd');
    categories = dds[0].text
    bezirk = dds[1].text
    datum = dds[2]
    address_node = dds[3]
    # remove <a>-node with a garbage stadtplandienst link 
    stadtplanlink = address_node.a
    stadtplanlink.extract()
    # description
    description = detail_page.find("div", { "class" : "suchdetails" })
    # split the arrays
    category_list = categories.split(', ')
        
    
    
    # datums are wrapped in <b>, potential hours in <small>
    datums = datum.findAll('b');
    hrs = datum.findAll('small');
    i = 0;
    print item
    for d in datums:
        total_rows = total_rows + 1
        datum_text = d.text
        print i;
        if ( len(hrs) > i ):
            hour = hrs[i].text
            s = hour.split(' - ', 1)
            start = s[0].replace('Uhr', '').strip()
            t = datetime.strptime( datum_text + " " + start, "%d.%m.%Y %H:%M" )
            # @todo handle start - end stuff, it's normally just a few hours ...
        else:
            t = datetime.strptime( datum_text, '%d.%m.%Y' );                   
        i = i + 1
        print str(count) + ": " + item.title.text + ' ' + t.isoformat() + ' (#'+str(total_rows)+')'
        # the guid is the link plus the isoformat date as an anchor (multiple events on one page)
        
        record = { 
                  'title' : item.title.text, 
                  'link': link, 'guid': link+'#'+t.isoformat(), 
                  'pubDate': item.pubdate.text,
                  'category': category_list,
                  'md:address': 'Berlin, ' + bezirk, 
                  'md:stadtteil': bezirk, 
                  'md:zuordnung': 'bezirk', 
                  'md:description': description.text + " (" + address_node.text + ")", 
                  # we assume that start and end day are on the same day
                  'md:start_date':  t.isoformat(), 
                  'md:end_date': t.isoformat(), 
                  'md:author': 'berlin.de', 
                  'md:source_query_date': datetime.now().isoformat()
                  }
        print record
        scraperwiki.datastore.save(["guid"], record)

        
