from pprint import pformat
import requests

import lxml.html

import scraperwiki

data = {
    'logins_ident': 'ilovebicykles',
    'logins_password': 'fantafantafanta',
}

session = requests.session()

session.post('https://www.victoriamilan.se/login', data=data, verify=False)

start = 0
base_url = 'http://www.victoriamilan.se/profiles/quick?_rs=sex-male--age_from-32--age_to-32--country-176--state-2891--city-42368'

while True:
    r = session.get("%s&_start=%s" % (base_url, start))
    
    root = lxml.html.fromstring(r.text)

    profiles = root.cssselect('.search_container ul#tmpl_user_list li a.bold')

    if len(profiles) == 0:
        raise SystemExit
    
    for profile in profiles:
        try:
            profile_link = profile.attrib.get('href')
            r = session.get(profile_link)
            profile_root = lxml.html.fromstring(r.text)
            [summary] = profile_root.cssselect('.prfh_title span.small')
            [title] = profile_root.cssselect('h1')
        
            summary, title = summary.text_content(), title.text_content()
        
            properties = profile_root.cssselect('#id_qu p.smaller')
            for p in properties:
                if 'Etnisk bakgrund' in p.text_content():
                    data = {
                        'summary': summary,
                        'title': title,
                        'ethnicity': p.text_content(),
                    }
                    scraperwiki.sqlite.save(unique_keys=['title'], data=data)
        except ValueError:
            print "Skipping due to error"
    start += 20