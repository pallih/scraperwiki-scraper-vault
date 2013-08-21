# -*- encoding: utf8 -*-

import scraperwiki
import lxml.html
import json

index_html = scraperwiki.scrape('http://www.politicsresources.net/area/uk/ge10/candidates.htm')

mapit_wmcs = json.loads(scraperwiki.scrape('http://mapit.mysociety.org/areas/WMC'))
areas_by_name = {
    c['name']: c for c in mapit_wmcs.itervalues()
}

print areas_by_name

index = lxml.html.fromstring(index_html)

cand_links = index.cssselect("table a")

def scrape_data(cand_links):
    done_paths = set()
    for link in cand_links:
        print lxml.html.tostring(link)
        party = link.text_content().strip()
        path = link.attrib['href'].split('#',1)[0]
    
        if path not in done_paths:
            done_paths.add(path)
            url = 'http://www.politicsresources.net/area/uk/ge10/' + path
            print url
            cand_html = scraperwiki.scrape(url)
            cand = lxml.html.fromstring(cand_html)
            lis = cand.cssselect('li')
            block = []
            for l in lis:
                b = l.cssselect('b')
                if b:
                    party = l.text_content()
                    party = party[:party.rfind('[')].strip()
                else:
                    text = l.text_content().strip()
                    if text:
                        candidate, place = text.rsplit(',', 1)
                        area_id, place = fix_place(place)
                        block.append({'place': place, 'mapit_area_id': area_id,
                                      'candidate': candidate, 'party': party})
    
            scraperwiki.sqlite.save(
                ['mapit_area_id', 'place', 'candidate', 'party'],
                block
            )

def fix_place(place):
    place = place.strip().replace(' & ', ' and ')

    lower = ('Of', 'On', 'Upon')
    for w in lower:
        place = place.replace(' %s ' % w, ' %s ' % w.lower())
        place = place.replace('-%s-' % w, '-%s-' % w.lower())
    place = place.replace(' Under ', '-under-')
    place = place.replace('-Under-', '-under-')

    place = place.replace('Inverness Nairn ', 'Inverness, Nairn, ')
    place = place.replace(' Kent Mid', ' Mid Kent')
    place = place.replace('Hull ', 'Kingston upon Hull ')
    place = place.replace('Suffolk Central ', 'Central Suffolk ')
    place = place.replace('Devon West and Torridge', 'Torridge and West Devon')
    place = place.replace('Durham City Of', 'City of Durham')
    place = place.replace('Chester City Of', 'City of Chester')
    place = place.replace('Aberdeenshire West and Kincardine', 'West Aberdeenshire and Kincardine')
    place = place.replace('Basildon South and Thurrock East', 'South Basildon and East Thurrock')
    place = place.replace('Ynys Mon', u'Ynys Môn')
    place = place.replace('Richmond (yorksI', 'Richmond (Yorks)')
    place = place.replace('Dorset Mid and Poole North', 'Mid Dorset and North Poole')
    place = place.replace('Ayrshire North and Arran', 'North Ayrshire and Arran')
    place = place.replace('Worthing East and Shoreham', 'East Worthing and Shoreham')
    place = place.replace('Na H-Eileanan An Iar', 'Na h-Eileanan an Iar')
    place = place.replace('East Kilbride Strathaven and Lesmahagow', 'East Kilbride, Strathaven and Lesmahagow')

    if place.endswith(' The'):
        place = 'The ' + place[:-4]

    try:
        area_id = areas_by_name[place]['id']
        new_place = place
    except KeyError:
        dirs = ('South', 'North', 'East', 'West', 'Mid', 'Central')
        area_id = None
        # try cardinals at the front
        for dirstr in dirs:
            cardinal = place.rfind(' ' + dirstr)
            if cardinal != -1:
                new_place = (place[cardinal+1:] + ' ' + place[:cardinal]).strip()
                area_id = areas_by_name.get(new_place, {}).get('id')
                if area_id:
                    break

        # try cardinals before the last word
        if area_id is None:
            for dirstr in dirs:
                cardinal = place.rfind(' ' + dirstr)
                if cardinal != -1:
                    words = place.split(' ')
                    new_place = (' '.join(words[:-2]) + place[cardinal:] + ' ' + words[-2]).strip()
                    area_id = areas_by_name.get(new_place, {}).get('id')
                    if area_id:
                        break

        # try  a comma after the first word
        if area_id is None:
            new_place = ', '.join(place.split(None, 1))
            area_id = areas_by_name[new_place]['id']

    return area_id, new_place


scrape_data(cand_links)

