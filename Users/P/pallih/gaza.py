import scraperwiki
import json
import requests
import lxml.html
import itertools
import datetime

swutils=scraperwiki.swimport('swutils')
user_agent = swutils.get_user_agent()
    
requests.defaults.defaults['max_retries'] = 10

def main():
    
    print 'scraping November 2012 json feed'
    
    json_url = "http://ec2-46-51-135-144.eu-west-1.compute.amazonaws.com/gaza/Nov2012/json"
    json_response = requests.get(json_url).text
    json_dict = json.loads(json_response)
    
    batch = []
    alreadygot = []
    try:
        rows = scraperwiki.sqlite.select('id from features')
        for row in rows:
            alreadygot.append(row['id'])
    except:
        pass

    if len(json_dict['features']) - len(alreadygot) > 0:
        print 'scraping details for %s new features' % (len(json_dict['features']) - len(alreadygot))
    else:
        print 'no new features since last run'

    for feature in json_dict['features']:
        if feature['properties']['id'] not in alreadygot:
            batch.append({
                'lat': feature['geometry']['coordinates'][1],
                'lng': feature['geometry']['coordinates'][0],
                'type': feature['type'],
                'name': lxml.html.fromstring(feature['properties']['name']).cssselect('a')[0].text,
                'timestamp': feature['properties']['timestamp'],
                'iso8601-date' : datetime.datetime.fromtimestamp(int(feature['properties']['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                'link': feature['properties']['link'],
                'id': feature['properties']['id'],
                'description': get_description(feature['properties']['link'])
            })
            if len(batch) % 30 == 0:
                print 'saving %s new features' % len(batch)
                scraperwiki.sqlite.save(unique_keys=['id'], data=batch, table_name="features")
                batch = []
    
    if len(batch) > 0:
        print 'saving %s new features' % len(batch)
        scraperwiki.sqlite.save(unique_keys=['id'], data=batch, table_name="features")


def get_description(url):
    req = requests.get(url)
    dom = lxml.html.fromstring(req.text)
    desc = dom.cssselect('.report-description-text')[0]
    desc.cssselect('h5')[0].drop_tree()
    desc.cssselect('.credibility')[0].drop_tree()
    return desc.text_content()


main()



import scraperwiki
import json
import requests
import lxml.html
import itertools
import datetime

swutils=scraperwiki.swimport('swutils')
user_agent = swutils.get_user_agent()
    
requests.defaults.defaults['max_retries'] = 10

def main():
    
    print 'scraping November 2012 json feed'
    
    json_url = "http://ec2-46-51-135-144.eu-west-1.compute.amazonaws.com/gaza/Nov2012/json"
    json_response = requests.get(json_url).text
    json_dict = json.loads(json_response)
    
    batch = []
    alreadygot = []
    try:
        rows = scraperwiki.sqlite.select('id from features')
        for row in rows:
            alreadygot.append(row['id'])
    except:
        pass

    if len(json_dict['features']) - len(alreadygot) > 0:
        print 'scraping details for %s new features' % (len(json_dict['features']) - len(alreadygot))
    else:
        print 'no new features since last run'

    for feature in json_dict['features']:
        if feature['properties']['id'] not in alreadygot:
            batch.append({
                'lat': feature['geometry']['coordinates'][1],
                'lng': feature['geometry']['coordinates'][0],
                'type': feature['type'],
                'name': lxml.html.fromstring(feature['properties']['name']).cssselect('a')[0].text,
                'timestamp': feature['properties']['timestamp'],
                'iso8601-date' : datetime.datetime.fromtimestamp(int(feature['properties']['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                'link': feature['properties']['link'],
                'id': feature['properties']['id'],
                'description': get_description(feature['properties']['link'])
            })
            if len(batch) % 30 == 0:
                print 'saving %s new features' % len(batch)
                scraperwiki.sqlite.save(unique_keys=['id'], data=batch, table_name="features")
                batch = []
    
    if len(batch) > 0:
        print 'saving %s new features' % len(batch)
        scraperwiki.sqlite.save(unique_keys=['id'], data=batch, table_name="features")


def get_description(url):
    req = requests.get(url)
    dom = lxml.html.fromstring(req.text)
    desc = dom.cssselect('.report-description-text')[0]
    desc.cssselect('h5')[0].drop_tree()
    desc.cssselect('.credibility')[0].drop_tree()
    return desc.text_content()


main()



