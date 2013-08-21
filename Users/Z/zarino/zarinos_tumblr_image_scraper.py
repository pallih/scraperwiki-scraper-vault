import scraperwiki
import lxml.html
import requests
import base64
import re
import os

def ls(dir=''):
    print '$ ls ' + os.getcwd() + '/' + dir
    print os.system('ls -lAh ' + os.getcwd() + '/' + dir)

def rm(f):
    os.remove(os.getcwd() + '/' + f)

def get_image_from_brick(lxml_brick):
    thumb_url = a.cssselect('img')[1].get('src')
    url = thumb_url.replace('_250', '_500')
    r = requests.get(url)
    if r.status_code == 200:
        bin = base64.b64encode(r.content)
    elif r.status_code == 403:
        url = thumb_url.replace('_250', '_400')
        bin = base64.b64encode(requests.get(url).content)
    else:
        url = None
        bin = None
    return {
        'post_id': re.sub(r'[^0-9]+', '', a.get('href')),
        'timestamp': re.sub(r'[^0-9]+', '', a.get('class')),
        'post_url': a.get('href'),
        'url': url, 
        'thumb_url': thumb_url,
        'bin': bin
    }

base_url = 'http://zarinozappia.tumblr.com'
html = requests.get(base_url + '/archive')
dom = lxml.html.fromstring(html.text)

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `photos` ( `post_id` INT PRIMARY KEY, `timestamp` INT, `post_url` TEXT, `url` TEXT, `thumb_url` TEXT, `bin` TEXT)')

months = []
photos = []
carryon = True

for month in dom.cssselect('#browse_months_widget .month.active'):
    months.append(month.cssselect('a')[0].get('href'))

for month_url in months:
    # get first page of this month's photos
    html = requests.get(base_url + month_url)
    dom = lxml.html.fromstring(html.text)
    
    for a in dom.cssselect('a.brick.photo'):
        photos.append(get_image_from_brick(a))

    # save first page of this month's photos
    scraperwiki.sqlite.save(['post_id'], photos, 'photos')
    last_timestamp = photos[-1]['timestamp']
    photos = []

    # get more pages of this month's photos
    while carryon:
        html = requests.get(base_url + month_url + '?before_time=' + last_timestamp + '&lite')
        dom = lxml.html.fromstring(html.text)

        if len(dom.cssselect('a.brick.photo')) > 0:
            for a in dom.cssselect('a.brick.photo'):
                photos.append(get_image_from_brick(a))

            # save this page's photos
            scraperwiki.sqlite.save(['post_id'], photos, 'photos')
            last_timestamp = photos[-1]['timestamp']
            photos = []

        else:
            carryon = False

exit()

"""
os.mkdir(os.getcwd() + '/images')

for photo in photos:
    try:
        f = open('tmp/' + re.sub(r'.+/', '', photo['url']), 'w')
        f.write(scraperwiki.scrape(photo['url']))
        f.close()
    except:
        try:
            f = open('tmp/' + re.sub(r'.+/', '', photo['url'].replace('_500', '_400')), 'w')
            f.write(scraperwiki.scrape(photo['url'].replace('_500', '_400')))
            f.close()
        except:
            print 'Could not save', photo

os.system('zip -r images tmp')

ls()

print base64.b64encode(open('images.zip', 'r').read())

"""
