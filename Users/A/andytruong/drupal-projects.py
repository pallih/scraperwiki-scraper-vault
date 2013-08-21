import scraperwiki
import json
import lxml.html

def find_projects(uid, username):
    html = 'http://drupal.org/user/' + uid
    html = scraperwiki.scrape(html)
    html = lxml.html.fromstring(html)
    projects = []
    for item in html.cssselect('.versioncontrol-project-user-commits dd ul li a'):
        projects.append({
            'uid':   int(uid),
            'name':  item.text,
            'label': item.get('href').replace('/project/', ''),
            'username': username,
        })
    return projects

# https://scraperwiki.com/docs/api?name=drupal-exerts#sqlite
# Query: select * from `swdata` order by RANDOM() LIMIT 100
data  = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?'
data += 'format=jsonlist&name=drupal-exerts&attach=drupal-exerts'
data += '&query=select%20*%20from%20%60swdata%60%20order%20by%20RANDOM()%20LIMIT%20100'
data  = scraperwiki.scrape(data)
data  = json.loads(data)

projects = []
for expert in data['data']:
    projects += find_projects(str(expert[1]), expert[0])

scraperwiki.sqlite.save(unique_keys=['name'], data=projects)
