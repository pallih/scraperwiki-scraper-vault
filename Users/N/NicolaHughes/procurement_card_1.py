import requests
import json

data = requests.get("http://data.gov.uk/api/action/package_search?q=procurement+card").content
data = json.loads(data)

urls = []

for package in data['result']['results']:
    title = package['notes']
    if "Government Procurement Card" or "GPC" in title:
        publisher = package['groups'][0]['title']
        link = "http://data.gov.uk/dataset/" +  package['name']
    
        for resource in package['resources']:
            print resource
            u = resource.get('cache_url') or resource['url']
            if not u.endswith('.ashx'):
                urls.append(resource['cache_url'])



#print urls