import scraperwiki
import requests
import lxml.html


def scrape_people(role='male'):

    # We can scrape different types of people!
    roles = ['male', 'female']

    # Zarino <3 error handling.
    if role not in roles:
        raise ValueError('scrape_people() takes one argument, which can be any of these roles: %s' % ', '.join(roles))

    # Let's start blindly scraping each results page…
    for i in range(1,200000):
        r = requests.get('http://www.victoriamilan.se/profiles/quick?_rs=sex-%s--age_from-18--age_to-99&_start=%s' % (role,i))
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

            if len(dom.cssselect('ul#tmpl_user_list.mb_1')):
                # Great! This page contains people to scrape.
                people = []
                for td in dom.cssselect('ul#tmpl_user_list.mb_1 div.mg_1px.src_pr_bg.pad_05'):
                    person = {
                        'role': role,
                        'name': get_element_or_none(div.mg_1px.src_pr_bg.pad_05, '.bold'),
                        'age': get_element_or_none(div.mg_1px.src_pr_bg.pad_05, 'span'),
                        'url': 'http://www.victoriamilan.se/' + get_element_or_none(td, '.bold')
                    }
                    print person['name']


scrape_people('male')