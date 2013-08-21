import scraperwiki
import datetime
import lxml.html
import re


# set up the datastore


#print 'Resetting datastore...'
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `colours`')
#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS `shots`')
#scraperwiki.sqlite.execute('DROP VIEW `shots_by_date`')
#scraperwiki.sqlite.commit()

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `colours` (`colour` text, `row_created` text)')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `shots` (`shot_id` text, `shot_title` text, `image_url` text, `author_name` text, `author_username` text, `colour` text, `row_created` text)')
scraperwiki.sqlite.execute('CREATE VIEW IF NOT EXISTS `shots_by_date` AS select * from shots order by row_created desc')
scraperwiki.sqlite.commit()



# these functions do the heavy lifting

def get_colours():
    print 'Scraping the primary colours from Dribbble colours page...'
    colour_index = lxml.html.fromstring(scraperwiki.scrape('http://dribbble.com/colors'))
    colours = colour_index.cssselect("ul.color-chips a")
    i = 1
    for el in colours:
        print str(i) + '/' + str(len(colours)) + ' Saving colour ' + el.text_content() + '...'        
        scraperwiki.sqlite.save(unique_keys=['colour'], data={'colour': el.text_content(), 'row_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, table_name='colours')
        i += 1

def get_shots(arr):
    i = 1
    for a in arr:
        hex = a['colour'].replace('#','')
        done = False
        print 'Scraping colour ' + str(i) + ' of ' + str(len(arr)) + ': #' + hex + '...';
        
        for page_no in range(1,6):
            if not done:
                page = lxml.html.fromstring(scraperwiki.scrape('http://dribbble.com/colors/' + hex + '?page=' + str(page_no)))
                shots = page.cssselect('ol.dribbbles>li')
                for shot in shots:
                    id = re.sub('\D', '', shot.get('id'))
                    if id == most_recent_shots[a['colour']]:
                        print 'Colour ' + a['colour'] + ' is up to date';
                        done = True
                        break
                    else:
                        get_shot_details(id, '#' + hex)
        
        i += 1

def get_shot_details(id, colour):
    print '    Scraping details for shot ' + str(id) + '...'
    record = {}
    record['shot_id'] = id
    page = lxml.html.fromstring(scraperwiki.scrape('http://dribbble.com/shots/' + str(id)))
    record['image_url'] = re.sub('\?.+', '', page.cssselect('#the-shot img')[0].get('src'))
    record['shot_title'] = page.cssselect('#screenshot-title')[0].text
    record['author_name'] = page.cssselect('.shot-byline-user a')[0].text
    record['author_username'] = page.cssselect('.shot-byline-user a')[0].get('href').replace('/','')
    record['colour'] = colour
    record['row_created'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scraperwiki.sqlite.save(unique_keys=['shot_id'], data=record, table_name='shots')




# start working!

colours_in_db = scraperwiki.sqlite.select('colour from colours order by colour')

if len(colours_in_db):
    print 'Fetching most recent shots in the database'
    most_recent = scraperwiki.sqlite.select('colour, shot_id from `shots_by_date` group by colour')
    most_recent_shots = {}
    for a in most_recent:
        most_recent_shots[a['colour']] = a['shot_id']
    print most_recent_shots
    get_shots(colours_in_db)
else:
    get_colours()
    print 'Colour categories fetched - run again to scrape shots'
