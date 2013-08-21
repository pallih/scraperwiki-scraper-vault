import requests
import json

data = requests.get("http://data.gov.uk/api/action/package_search?q=procurement+card").content
data = json.loads(data)

urls = []

for package in data['result']['results']:
    print package['groups'][0]['title']
    print package['name']
    print package['notes']
    for resource in package['resources']:
        print resource
        u = resource.get('cache_url') or resource['url']
        if not u.endswith('.ashx'):
            urls.append(resource['cache_url'])



#print urls