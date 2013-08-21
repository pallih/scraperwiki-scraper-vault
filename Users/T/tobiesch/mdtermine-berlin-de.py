import scraperwiki

from datetime import datetime, date, time, timedelta
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

import re
import sys

# from to day
date_start = datetime.now()
date_stop = date_start + timedelta(weeks=4)
date_start = date_start.strftime('%d.%m.%Y')
date_stop = date_stop.strftime('%d.%m.%Y')

print "Retrieving events from " + date_start + " to " + date_stop

# retrieve rss
offset = 0
resultcount=10

#offset <=x is just a max depth condition to additional guard against an endless loop
while resultcount >=10 and offset <=100:
    #check for stuff up to one month in advance
    starting_url = 'http://www.berlin.de/land/kalender/index.php?rss&c=22&kategorie[8]=7&ls=' + str(offset) + '&date_start=' + date_start + '&date_stop=' + date_stop
    #nur Bürgersprechstunden
    #starting_url  =  'http://www.berlin.de/land/kalender/index.php?rss&c=22&kategorie[8]=7&stichwort=bürgersprechstunde&ls='  + str(offset) + '&date_start=' + date_start
    
    print "query " + starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulStoneSoup(html)
    
    # use BeautifulStoneSoup to get all <item> tags
    items = soup.findAll('item')
    # for item in items:
    resultcount = len(items)
    offset+=10
    
    print "Found " + str(resultcount) + "  item(s)"
    total_rows = count = 0
    
    for item in items:
        category1=""
        tag1=""
        tag2=""
        mytitle = item.title.text.encode('utf-8')
    
        if mytitle.find('Bürgersprechstunde') >= 0:
            pass
        else:
            continue
             
        count = count + 1 
        link = item.link.text.encode('utf-8')
        #we want the shortest link and get rid of all useless parameters as entries are uniquely identified via the link
        baselink = re.search('^.*\?',link)
        detailpara = re.search('detail=\d+',link)
        #check we actually found sth
        if detailpara == None or baselink == None:
            print "PROBLEM, could not find a suitable link in " + link
            print "die ..."
            raise(UserWarning)
        else:
            link = baselink.group() + detailpara.group()

        # scrape additional data from the detail page
        print "scraping " + link;
        detail_page = BeautifulSoup( scraperwiki.scrape(link) );
        
        # the details are wrapped in <dd>s, sigh
        #dds = detail_page.findAll('dd');
        #dds = detail_page.findAll('td');

        #check suchdetails first!
        dds = detail_page.findAll('div','event_detail_content');
        #print "dds is:" + str(dds)
        categories = dds[0].contents[0].text
        #print "categories: " + categories
        bezirk = dds[1].contents[0].text
        #print "Bezirk: " + bezirk
        datum = dds[2].renderContents()
        #print "Datum: " + datum

        #address_node = dds[3].contents[0].text
        address_node = dds[3]
        address_node=address_node.font.renderContents()
        #print "address: " + address_node + "\n";


        # description
        description = detail_page.find("div", { "class" : "suchdetails" })
        description = description.find("div")
        title = description.find("h1").renderContents()
        description = description.findAll('p')
        descriptiontext = str(title) + '<br />' + str(description[1])

        #print "descriptiontext is " + str(descriptiontext)

        # split the arrays
        category_list = categories.split(', ')

        #tag and category creation
        if mytitle.find('Bürgersprechstunde') >= 0:
            category1="Abgeordnete"
            tag1='Bürgersprechstunde'
            if mytitle.find('Bezirksbürgermeister') >= 0 or descriptiontext.find('Bezirksbürgermeister') >= 0:
               tag2='Bezirksbürgermeister/in'
            elif mytitle.find('Bezirksstadtr') >= 0 or descriptiontext.find('Bezirksstadtr') >= 0:
                tag2='Bezirksstadtrat/rätin'
            
        
        

        #save all dates as one individual record - if multiple dates are mentioned
        datums=datum.split('<br />')
        
        for d in datums:
            print "now it is " + d
            total_rows = total_rows + 1
            #datum_text = d
            tempdate=d.split(', ', 1)
            datum_text = tempdate[0]
        
      
            t = datetime.strptime( datum_text, '%d.%m.%Y' );
            tend = datetime.strptime( datum_text + " 23:59:59", '%d.%m.%Y %H:%M:%S' );                                      
            if ( len(tempdate)>1 ):
                hour = tempdate[1]
                s = hour.split(' - ', 1)
                start = s[0].replace('Uhr', '').strip()
                #works at least for Buergersprechstunden I think
                end = s[1].replace('Uhr', '').strip()                
                t = datetime.strptime( datum_text + " " + start, "%d.%m.%Y %H:%M" )
                tend = datetime.strptime( datum_text + " " + end, "%d.%m.%Y %H:%M" )
                # @todo handle start - end stuff, it's normally just a few hours ...
            else:
                t = datetime.strptime( datum_text, '%d.%m.%Y' );                   
        #i = i + 1
            #print str(count) + ": " + item.title.text + ' ' + t.isoformat() + ' (#'+str(total_rows)+')'
            # the guid is the link plus the isoformat date as an anchor (multiple events on one page)
     
            record = { 
                      'title' : item.title.text, 
                      'link': link, 
                      'guid': link+'#'+t.isoformat(), 
                      'date_scraped': item.pubdate.text,
                      'category1': category1,
                      'md_address': bezirk + ' Berlin', 
                      #'md:stadtteil': bezirk, 
                      'md_zuordnung': 'Bezirk/Ortschaft', 
                      'description': descriptiontext + "(" + address_node + ")", 
                      # we assume that start and end day are on the same day
                      'md_start_date':  t.isoformat(), 
                      'md_expiration_date': tend.isoformat(), 
                      'md_author': 'berlin.de', 
                      #'md:source_query_date': datetime.now().isoformat(),
                      'md_tag1': tag1,
                      'md_tag2': tag2
                      }
            print record
            scraperwiki.sqlite.save(["guid"], record)



