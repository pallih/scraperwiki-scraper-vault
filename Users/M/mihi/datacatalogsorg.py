import scraperwiki
import time,datetime
import json,urllib

geonames_username='mihi'
geonames_baseurl = 'http://api.geonames.org/searchJSON?maxRows=1&username=%s&q=' % geonames_username


# Blank Python
special_cases = {
        'allerdale': 'Allerdale',
        'bordeaux_fr': 'Bordeaux',
        'dati-lombardia': 'Lombardia, Italy',
        'dnv_org': 'North Vancouver',
        'dublinked-datastore': 'Dublin',
        'gironde-aquitaine_fr': 'Gironde',
        'go-geo': 'United Kingdom',
        'montpellier_fr': 'Montpellier',
        'mosman-council-datastore': 'Mosman',
        'nantes_fr': 'Nantes',
        'new-orleans-louisiana': 'New-Orleans',
        'opendata-lv': 'Latvia',
        'openstreetmap': 'Earth',
        'portal-de-datos-abiertos-de-jccm': 'Castilla-La Mancha',
        'provincia-roma': 'Rome',
        'region-of-waterloo-ontario': 'Waterloo, Ontario',
        'rennes_fr': 'Rennes',
        'salford': 'Salford',
        'saone-et-loire_fr': 'Saone-et-Loire',
        'toulouse_fr': 'Toulouse',
        'us-department-of-labor-enforcement-data': 'USA',
        'victoria-australian-state-open-data-catalogue': 'Victoria, Australia',
        'picandmix_org_uk':'Kent, UK',
        'open-kent':'Kent, UK',
        'andalusia-data-portal':'Andalusia, Spain',
        'cordoba':'Cordoba, Spain',
        'piemonte_it':'Piemonte, Italy',
        'trafford_gov_uk':'Trafford, UK',
        'data_vic_gov_au':'Victoria, Australia',
        'datos-gub-uy':'Uruguay',

        }
time_of_last_geonames_request=datetime.datetime.now()

def geonames_lookup(spatial_text):
    '''
    Return the lat. and long. from a geonames search for the given text.

    Results from geonames are cached in a local file.

    :param spatial_text: the text to search for, e.g. "Albania:
    :type spatial_text: string

    :rtype: a dictionary with keys 'lat' and 'long', or None if the geonames
        search fails

    '''
    global time_of_last_geonames_request
    if spatial_text.lower() in ('global', 'earth', 'globe', 'world',
            'worldwide'):
        return None

    
    cache = {}

    if spatial_text in cache:
        return cache[spatial_text]
    else:

        # Don't send requests to geonames too fast.
        if (datetime.datetime.now() - time_of_last_geonames_request).total_seconds() < 0.5:
            time.sleep(0.5)
            time_of_last_geonames_request = datetime.datetime.now()

        url = geonames_baseurl + urllib.quote(spatial_text)
        fo = urllib.urlopen(url)
        res = fo.read()
        res = json.loads(res)
        if res['geonames']:
            result = {
                    'lat': res['geonames'][0]['lat'],
                    'lon': res['geonames'][0]['lng']
                    }
            cache[spatial_text] = result
            return result
        else:
            return None



jsn=scraperwiki.scrape("http://datacatalogs.org/api/search/dataset?q=&limit=500&all_fields=1")
datasets=json.loads(jsn)

for dataset in datasets['results']:
   if dataset['name'] in special_cases:
       dataset['extras']['spatial_text'] = special_cases[dataset['name']]

   spatial_text = dataset['extras']['spatial_text']
   spatial_text = spatial_text.encode('utf8', 'ignore')
   location = geonames_lookup(spatial_text)
   if location:
      dataset['lon'] = location['lon']
      dataset['lat'] = location['lat']
   
   else:
      dataset['lat'] = None
      dataset['lon'] = None
   if "groups" in dataset.keys():
       dataset['groups']=" ".join(dataset['groups'])
   if "tags" in dataset.keys():
       dataset['tags'] = " ".join(dataset['tags'])


   # Promote the dataset's extras to top-level keys.
   dataset['spatial_code'] = dataset['extras']['spatial']
   del dataset['extras']['spatial']
   dataset.update(dataset['extras'])
   del dataset['extras']

   # Delete any empty values.
   for key in dataset.keys():
       if not dataset[key]:
          del dataset[key]

   scraperwiki.sqlite.save(unique_keys=['name','id'], data=dataset)
    
