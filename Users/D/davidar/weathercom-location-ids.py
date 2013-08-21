import string
import itertools
import re
import scraperwiki

path = {
    'region':   '/outlook/weatherbyregion/',
    'country':  '/outlook/weatherbycountry/',
    'city':     '/weather/today/',
    'us_state': '/outlook/weatherbystate/',
    'us_city':  '/weather/local/',
}

path_regex = {}
for k,v in path.iteritems():
    path_regex[k] = re.compile('<a [^>]*href="' + v + '([^"]+)"[^>]*>([^<]+)</a>')

def scrape(path, regex):
    html = scraperwiki.scrape('http://www.weather.com' + path)
    while html is None: html = scraperwiki.scrape('http://www.weather.com' + path)
    for match in regex.finditer(html):
        yield match.groups()

def scrape_index(path, regex):
    return itertools.chain(*[scrape(path + '-' + letter, regex) for letter in string.lowercase])

def store(data_type, data_id, data_name, data_parent=None):
    data = {'type':data_type, 'id':data_id, 'name':data_name}
    if data_parent:
        data['parent'] = data_parent
    scraperwiki.sqlite.save(['type','id'], data)

for region_code,region_name in scrape(path['region'], path_regex['region']):
    store('region', region_code, region_name)
    for country_code,country_name in scrape(path['region'] + region_code, path_regex['country']):
        store('country', country_code, country_name, region_code)
        for city_code,city_name in scrape_index(path['country'] + country_code, path_regex['city']):
            store('city', city_code, city_name, country_code)


