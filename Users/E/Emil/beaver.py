import scraperwiki
import requests
import lxml.html


def scrape_people():

    # Let's start blindly scraping each results page…
    for i in range(1,100):
        r = requests.get('http://www.hyperisland.com/people?filter=true&role=%s&page=%s' % (role,i))
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

            if len(dom.cssselect('div.community_list')):
                # Great! This page contains people to scrape.
                people = []
                for td in dom.cssselect('div.community_list td'):
                    person = {
                        'role': role,
                        'name': get_element_or_none(td, 'h6'),
                        'course': get_element_or_none(td, '.subtitle')[:-5],
                        'year': int(get_element_or_none(td, '.subtitle')[-4:]),
                        'bio': get_element_or_none(td, '.links a'),
                        'url': 'http://www.hyperisland.com' + get_element_or_none(td, 'a', 'href')
                    }
                    print person['name']

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
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text



scrape_people('student')
import scraperwiki
import requests
import lxml.html


def scrape_people():

    # Let's start blindly scraping each results page…
    for i in range(1,100):
        r = requests.get('http://www.hyperisland.com/people?filter=true&role=%s&page=%s' % (role,i))
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

            if len(dom.cssselect('div.community_list')):
                # Great! This page contains people to scrape.
                people = []
                for td in dom.cssselect('div.community_list td'):
                    person = {
                        'role': role,
                        'name': get_element_or_none(td, 'h6'),
                        'course': get_element_or_none(td, '.subtitle')[:-5],
                        'year': int(get_element_or_none(td, '.subtitle')[-4:]),
                        'bio': get_element_or_none(td, '.links a'),
                        'url': 'http://www.hyperisland.com' + get_element_or_none(td, 'a', 'href')
                    }
                    print person['name']

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
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text



scrape_people('student')
