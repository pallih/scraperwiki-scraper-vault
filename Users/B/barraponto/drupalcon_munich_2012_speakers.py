import scraperwiki
from lxml.html import parse

speakers = {}
sdata = []
schedule_urls = [
    'http://munich2012.drupal.org/program/schedule/2012-08-20',
    'http://munich2012.drupal.org/program/schedule/2012-08-21',
    'http://munich2012.drupal.org/program/schedule/2012-08-22',
    'http://munich2012.drupal.org/program/schedule/2012-08-23'
]

for schedule in schedule_urls:
    dom = parse(schedule).getroot()
    dom.make_links_absolute()
    for speaker in dom.cssselect('.session-instructor a'):
        url = speaker.get('href')
        speakers[url.split('/')[-1]] = {
            'username': url.split('/')[-1],
            'name': speaker.text_content(),
            'url': url
        }

for key, speaker in speakers.iteritems():
    try:
        dom = parse(speaker['url']).getroot()
        if dom.cssselect('.profile dl a'):
            speakers[key]['do_url'] = dom.cssselect('.profile dl a')[0].get('href')
    except (IOError): # some urls return 403 :/
        print speaker['url']

for speaker in speakers.itervalues():
    if 'do_url' in speaker:
        try:
            dom = parse(speaker['do_url']).getroot()
            gender_selection = dom.cssselect('dd.profile-profile_gender')
            speaker['gender'] = gender_selection[0].text_content().strip() if gender_selection else 'Undefined'
            scraperwiki.sqlite.save(unique_keys=['username'], data=speaker)
        except (IOError): # some other urls are returning 403 :/
            print speaker['do_url']
