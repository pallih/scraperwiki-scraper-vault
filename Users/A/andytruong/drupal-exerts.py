import scraperwiki
from lxml import etree

# Blank Python

root = 'https://kippt.com/andytruong/drupalexperts/feed'
root = scraperwiki.scrape(root)
# print root
root = etree.XML(root)

experts = []
for item in root.iterfind(".//item"):
    name   = item.find('title').text.replace(' | drupal.org', '')
    uid    = item.find('link').text.replace('http://drupal.org/user/', '')
    expert = {'name': name, 'uid': int(uid)}
    experts.append(expert)

scraperwiki.sqlite.save(unique_keys=['uid'], data=experts)
import scraperwiki
from lxml import etree

# Blank Python

root = 'https://kippt.com/andytruong/drupalexperts/feed'
root = scraperwiki.scrape(root)
# print root
root = etree.XML(root)

experts = []
for item in root.iterfind(".//item"):
    name   = item.find('title').text.replace(' | drupal.org', '')
    uid    = item.find('link').text.replace('http://drupal.org/user/', '')
    expert = {'name': name, 'uid': int(uid)}
    experts.append(expert)

scraperwiki.sqlite.save(unique_keys=['uid'], data=experts)
