from pprint import pformat
import requests

import lxml.html

import scraperwiki

data = {
    'logins_ident': 'jegzyd@yahoo.com',
    'logins_password': 'Olawaled1',
}

session = requests.session()

session.post('https://www.facebook.se/login', data=data, verify=False)

start = 0
base_url = 'http://www.facebook.com/jegzyd'

while True:
    r = session.get("%s&_start=%s" % (base_url, start))
    
    root = lxml.html.fromstring(r.text)

    profiles = root.cssselect('.static.ak.fbcdn.net/rsrc.php/v2/ym/r/MoSR2pussUR.js:22')

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