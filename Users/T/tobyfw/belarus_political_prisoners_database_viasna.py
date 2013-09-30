import scraperwiki
import lxml.etree
import urllib
import re

def convertArray(str):
    m = re.search(ur'\"value\";s:[^:]+:\"([^"]+)\";', str)
    if m:
        return m.groups(1)[0]
    return ""

url = "http://www.pakalennie.de/wp_postmeta.xml"
tree = lxml.etree.parse(urllib.urlopen(url))
tables = tree.xpath('//database[@name="viazni"]/table')

posts = {}

for table in tables:
    id = table.xpath('column[@name="post_id"]')[0].text
    if not id in posts:
        posts[id] = { 'id' : id };
        print 'New post ', id

    key = table.xpath('column[@name="meta_key"]')[0].text.strip()
    value = table.xpath('column[@name="meta_value"]')[0].text.strip()
    
    if key == "_article" or key == "_sanction":
        value = convertArray(value)

    posts[id][key] = value

print 'Done reading ', len(posts), 'posts'

for id in posts:
    if "_name" in posts[id] and posts[id]["_name"] != "":
        scraperwiki.sqlite.save(unique_keys=['id'], data=posts[id])


import scraperwiki
import lxml.etree
import urllib
import re

def convertArray(str):
    m = re.search(ur'\"value\";s:[^:]+:\"([^"]+)\";', str)
    if m:
        return m.groups(1)[0]
    return ""

url = "http://www.pakalennie.de/wp_postmeta.xml"
tree = lxml.etree.parse(urllib.urlopen(url))
tables = tree.xpath('//database[@name="viazni"]/table')

posts = {}

for table in tables:
    id = table.xpath('column[@name="post_id"]')[0].text
    if not id in posts:
        posts[id] = { 'id' : id };
        print 'New post ', id

    key = table.xpath('column[@name="meta_key"]')[0].text.strip()
    value = table.xpath('column[@name="meta_value"]')[0].text.strip()
    
    if key == "_article" or key == "_sanction":
        value = convertArray(value)

    posts[id][key] = value

print 'Done reading ', len(posts), 'posts'

for id in posts:
    if "_name" in posts[id] and posts[id]["_name"] != "":
        scraperwiki.sqlite.save(unique_keys=['id'], data=posts[id])


