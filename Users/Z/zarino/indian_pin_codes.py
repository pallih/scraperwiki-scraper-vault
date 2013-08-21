import scraperwiki
import requests
import lxml.html
import datetime

def main():
    # We create the tables up front because Zarino's anal about column order, 
    # and scraperwiki.sqlite.save doesn't guarantee column orders.
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS "pincodes" (pincode INT, area, district, state, scraped)')
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS "queue" (district_name, district_url, state_name, state_url)')
    scraperwiki.sqlite.commit()

    # Find out which districts we need to scrape.
    todo = scraperwiki.sqlite.select('* from "queue"')
    
    # If there are districts to scrape.
    if len(todo):
        print "%s districts to scrape..." % len(todo)
        for task in todo:
            # Scrape and save details for each area/pincode in this district.
            scrape_district(task)
            # Once all areas in this district have been scraped, remove district from queue.
            complete(task)
        
    # No districts to scrape – rebuild the queue.
    else:
        # Scrape states and districts, save them *all* to queue.
        populate_queue()
        # Now we've filled the queue, start over again.
        main()


def populate_queue():
    districts = []
    print "Rebuilding queue..."

    # Scrape homepage for listing of states.
    base_url = 'http://www.xombom.com/pincode/'
    r = requests.get(base_url)
    dom = lxml.html.fromstring(r.text)

    for link in dom.cssselect('#pincodemaindiv a'):
        state_name = link.text.replace(r' Pincodes', '')
        state_url = link.get('href')

        # Scrape each state's page for a list of districts.
        r2 = requests.get(base_url + state_url)
        dom2 = lxml.html.fromstring(r2.text)

        for link2 in dom2.cssselect('#pincodemaindiv a'):
            district_name = link2.text.replace(r' District Pincodes', '')
            district_url = link2.get('href')

            districts.append({
                'district_name': district_name,
                'state_name': state_name,
                'district_url': base_url + state_url + district_url,
                'state_url': base_url + state_url
            })

    scraperwiki.sqlite.save(['district_url'], districts, 'queue')
    print "Queue rebuilt! %s districts to scrape on next run." % len(districts)


def scrape_district(d):
    areas = []
    print "%s, %s - %s" % (d['district_name'], d['state_name'], d['district_url'])

    r = requests.get(d['district_url'])
    dom = lxml.html.fromstring(r.text)

    for i, link in enumerate(dom.cssselect('#pincodemaindiv a')):
        # The HTML markup on this page is particularly crap.
        # All we have is a bucket of <a> elements.
        # So, we have to rely on their index (even/odd),
        # which we find out using the modulus operator, '%'
        if i%2==0:
            # Even. This link is an area's name.
            areas.append({
                'area': link.text,
                'district': d['district_name'],
                'state': d['state_name'],
                'scraped': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            # Odd. This link is an area's pincode
            areas[(i-1)/2]['pincode'] = link.text

    scraperwiki.sqlite.save(['pincode'], areas, 'pincodes')

    if len(dom.xpath('//a[text()="Next Page"]')):
        # There is another page in this district.
        # Scrape it before moving on.
        # Recursive functions FTW.
        d['district_url'] = 'http://www.xombom.com' + dom.xpath('//a[text()="Next Page"]')[0].get('href')
        scrape_district(d)


def complete(d):
    scraperwiki.sqlite.execute('DELETE FROM "queue" WHERE district_name=? AND state_name=?', (d['district_name'], d['state_name']))
    scraperwiki.sqlite.commit()
    print "COMPLETED: %s, %s" % (d['district_name'], d['state_name'])


main()

