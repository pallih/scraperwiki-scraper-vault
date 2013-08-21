# A collection of images from mens' style tumblogs
# For chaps thoroughly bored of their wardrobes

import scraperwiki
import lxml.html
import re

try:
    tumblogs = scraperwiki.sqlite.select('blog, max(timestamp) as latest from `images` group by blog')
except:
    tumblogs = [
        {'blog':'aapcg','latest':0}, 
        {'blog':'beurrenoisette','latest':0}, 
        {'blog':'filup','latest':0}, 
        {'blog':'glennswardrobe','latest':0}, 
        {'blog':'indiomoda','latest':0}, 
        {'blog':'it-boys','latest':0}, 
        {'blog':'lazyastronaut','latest':0}, 
        {'blog':'lookingsmart','latest':0}, 
        {'blog':'mensfashionworld','latest':0}, 
        {'blog':'sharpmagazine','latest':0}, 
        {'blog':'simpleisthenewblack','latest':0}, 
        {'blog':'styleguy','latest':0}, 
        {'blog':'thestyleiwant','latest':0}
    ]

for t in tumblogs:
    print 'Scraping ' + t['blog'] + '.tumblr.com'
    data = []
    html = scraperwiki.scrape('http://' + t['blog'] + '.tumblr.com/archive')
    dom = lxml.html.fromstring(html)
    for a in dom.cssselect('a.photo'):
        if int(re.compile('\d+').findall(a.get('class'))[0]) > t['latest']:
            row = {}
            row['url'] = a.get('href')
            row['id'] = int(re.compile('\d+').findall(row['url'])[0])
            row['thumbnail'] = a.cssselect('img')[1].get('src')
            row['fullsize'] = row['thumbnail'].replace('_250', '_500')
            row['blog'] = t['blog']
            row['timestamp'] = int(re.compile('\d+').findall(a.get('class'))[0])
            data.append(row)
        else:
            break
    if data:
        scraperwiki.sqlite.save(['id'], data, 'images')
        print '-- ' + str(len(data)) + ' images saved'
    else:
        print '-- no new images since last scrape'

