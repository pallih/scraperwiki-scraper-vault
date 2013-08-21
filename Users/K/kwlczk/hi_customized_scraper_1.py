import scraperwiki
import requests
import lxml.html


def scrape_people(role='students'):

    # We can scrape different types of people!
    roles = ['students']

    # Zarino <3 error handling.
    if role not in roles:
        raise ValueError('scrape_people() takes one argument, which can be any of these roles: %s' % ', '.join(roles))

    # Let's start blindly scraping each results page…
    for i in range(1,100):
        r = requests.get('http://www.hyperisland.com/people?filter=true&role=%s&page=%s' % (role,i))
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

            if len(dom.cssselect('div.community_list')):
                # Great! This page contains people to scrape.
                people = []
                for td in dom.cssselect('div.community_list td'):
                    try:
                        course = get_element_or_none(td, '.subtitle')[:-5]
                    except:
                        course = ""                       
                    try:
                        year = int(get_element_or_none(td, '.subtitle')[-4:])
                    except:
                        year = ""

                    person = {
                        'role': role,
                        'name': get_element_or_none(td, 'h6'),
                        'course': course,
                        'year': year,
                        'bio': get_element_or_none(td, '.links a'),
                        'url': 'http://www.hyperisland.com' + get_element_or_none(td, 'a', 'href')
                    }
                    print person['name']

                    # Why stop there? Let's scrape more!!
                    r2 = requests.get(person['url'])
                    dom2 = lxml.html.fromstring(r2.text)

                    if get_element_or_none(dom2, '.avatar img', 'src'):
                        person['avatar'] = 'http:' + get_element_or_none(dom2, '.avatar img', 'src')
                    
                    if get_element_or_none(dom2, '.about_profile a[data-latitude]'):
                        # this is the most complicated line in this whole scraper – take a deep breath…
                        person['location'] = dom2.xpath("//div[contains(@class, 'about_profile')]//a[@data-latitude]//span/following-sibling::text()")[0].strip()
                        # got that?
                        person['lat'] = float(get_element_or_none(dom2, '.about_profile a[data-latitude]', 'data-latitude'))
                        person['lng'] = float(get_element_or_none(dom2, '.about_profile a[data-latitude]', 'data-longitude'))

                    person['nationality'] = get_element_or_none(dom2, '.about_profile span[itemprop=nationality]')
                    person['website'] = get_element_or_none(dom2, '.about_profile span[itemprop=url]')

                    person['facebook'] = get_element_or_none(dom2, '.about_profile a[href*="facebook.com"]', 'href')
                    person['twitter'] = get_element_or_none(dom2, '.about_profile a[href*="twitter.com"]', 'href')
                    person['linkedin'] = get_element_or_none(dom2, '.about_profile a[href*="linkedin.com"]', 'href')
                    person['vimeo'] = get_element_or_none(dom2, 'section[data-vimeo-username]', 'data-vimeo-username')

                    # add this person to the list
                    people.append(person)

                # we've done all the people on this page… let's save.
                print 'saving page %s' % i
                scraperwiki.sqlite.save(['url'], people, role + 's')

            elif len(dom.cssselect('h5.no_result')):
                # Yay! We've reached the end.
                break


# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        #print e
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text


# Some people don't supply a location.
# This function geocodes their nationality instead.
def geocode_nationalities(role='students'):
    import json
    print 'geocoding nationalities'
    people = scraperwiki.sqlite.select('url, name, nationality from `%ss` where lat is null and nationality is not null' % role)
    for person in people:
        print person['name']
        r = requests.get('http://api.geonames.org/search', params={'q': person['nationality'], 'username': 'scraperwiki', 'maxRows': 1, 'type': 'json'}).text
        obj = json.loads(r)
        if len(obj['geonames']):
            lat = obj['geonames'][0]['lat']
            lng = obj['geonames'][0]['lng']
            scraperwiki.sqlite.execute("UPDATE `%ss` SET lat=%s, lng=%s WHERE url='%s'" % (role, lat, lng, person['nationality']))
            scraperwiki.sqlite.commit()
        else:
            print 'location', person['nationality'], 'returned no results! :-('


scrape_people('students')
geocode_nationalities('students')