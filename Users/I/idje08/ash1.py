from pprint import pformat
import requests

import lxml.html

import scraperwiki

session = requests.session()


data = {
    'pinf_uio_app%252Fstructure%252Fpublic%252Flogin_login__username_value': 'malfrid',
    'pinf_uio_app%252Fstructure%252Fpublic%252Flogin_login__password_value': 'dodo01',
}

session.post('https://secure.ashleymadison.com/app/public/loginaction.p', data=data, verify=False)
data = {
    'sid': 'ENCODED:O3WQOKAW5AHTTLODQA2710313730AE1570CAAAAA3NNVQ',
    'pinf_action_UXVpY2tTZWFyY2g%3D_YXBwL3N0cnVjdHVyZS9wcml2YXRlL2hlYWRlci9tZW51':'0',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__age_min_value':'30',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__age_max_value':'40',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__location_value':'455',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__loginstatus_value':'0',
}

r = session.post('http://www.ashleymadison.com/app/private/header/menu.p', data=data, verify=False)
start = 0-200
base_url = 'http://www.ashleymadison.com/app/private/member/search/result.p?o=%s&geoFilter=0&loginStatus=0&ageFilter=30-40'
print "Starting to scrape"
while True:
    url = base_url % start
    r = session.get(url)
    
    root = lxml.html.fromstring(r.text)
    
    profiles = root.cssselect('#resultsTable .hiliteRow')
    
    if len(profiles) == 0:
        print "Oh noes! No profiles! lol!"
        raise SystemExit
    print "Did I get any profiles?? lol"
    for profile in profiles:
    
        [summary] = profile.cssselect('.profileDetails')
        print "number of summaries: %s" % len(summary)
    
        summary = summary.text_content()
    
        # print summary
        # continue
    
        data = {'id': start, 'summary': summary,}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        start += 1
    print "yeah!!!!!! this many profiles found: %s" % len(profiles)from pprint import pformat
import requests

import lxml.html

import scraperwiki

session = requests.session()


data = {
    'pinf_uio_app%252Fstructure%252Fpublic%252Flogin_login__username_value': 'malfrid',
    'pinf_uio_app%252Fstructure%252Fpublic%252Flogin_login__password_value': 'dodo01',
}

session.post('https://secure.ashleymadison.com/app/public/loginaction.p', data=data, verify=False)
data = {
    'sid': 'ENCODED:O3WQOKAW5AHTTLODQA2710313730AE1570CAAAAA3NNVQ',
    'pinf_action_UXVpY2tTZWFyY2g%3D_YXBwL3N0cnVjdHVyZS9wcml2YXRlL2hlYWRlci9tZW51':'0',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__age_min_value':'30',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__age_max_value':'40',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__location_value':'455',
    'pinf_uio_app%2Fstructure%2Fprivate%2Fheader%2Fmenu_main__loginstatus_value':'0',
}

r = session.post('http://www.ashleymadison.com/app/private/header/menu.p', data=data, verify=False)
start = 0-200
base_url = 'http://www.ashleymadison.com/app/private/member/search/result.p?o=%s&geoFilter=0&loginStatus=0&ageFilter=30-40'
print "Starting to scrape"
while True:
    url = base_url % start
    r = session.get(url)
    
    root = lxml.html.fromstring(r.text)
    
    profiles = root.cssselect('#resultsTable .hiliteRow')
    
    if len(profiles) == 0:
        print "Oh noes! No profiles! lol!"
        raise SystemExit
    print "Did I get any profiles?? lol"
    for profile in profiles:
    
        [summary] = profile.cssselect('.profileDetails')
        print "number of summaries: %s" % len(summary)
    
        summary = summary.text_content()
    
        # print summary
        # continue
    
        data = {'id': start, 'summary': summary,}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        start += 1
    print "yeah!!!!!! this many profiles found: %s" % len(profiles)