#!/usr/bin/python
"""
    Grabs page content for pages with a 1280 px size img, skips if none exists

"""
import scraperwiki
import re
from random import randint
from time import sleep
import urllib
import urllib2
from bs4 import BeautifulSoup

# currently we are counting down to 1..
page_min = 1
page_max = 90

base_url = 'http://hirise.lpl.arizona.edu/releases/all_captions.php'
base_url_wallpapers = 'http://hirise.lpl.arizona.edu/'
local_img_dir = '/Users/lballard/projects/marsfromspace/images/'
published_url = 'https://s3.amazonaws.com/marsfromspace/published.txt'


class Scrape:

    def __init__(self, **kwargs):
        self.base_url = kwargs['base_url']
        self.local_img_dir = kwargs['local_img_dir']
        self.base_url_wallpapers = kwargs['base_url_wallpapers']

    def fetch_remote_file(self, url, repeat):
        local_file = self.local_img_dir + url.split('/')[-1]
        try:
            print 'fetching ' + str(local_file)
            urllib.urlretrieve(url, local_file)
            with open(local_file):
                pass
            return local_file
        except IOError:
            if repeat:  # try again..
                sleep(3)
                return self.fetch_remote_file(url, False)
            else:
                print "can't fetch remote file " + url
                return False

    def grab_all_page_urls(self, page_min, page_max):

        page_urls = []
        print("starting at " + self.base_url)

        # construct the index page urls from self.base_url and page no
        for i in range(page_max, page_min-1, -1):
            if i > 1:  # first page url has no page query var
                page_urls.append(self.base_url + '?page=%s' % str(i))

        all_links = []
        for url in page_urls:
            try:
                index_page = urllib2.urlopen(url).read()
            except urllib2.HTTPError:
                print 'urlopen fail ' + url
                continue

            # make sure index_page is not actually their 404 page that isn't returning a 404

            try:
                print("looking for detail page links at  " + url)
                index_soup = BeautifulSoup(index_page)
                all_cells = index_soup.findAll('td')  # each listing is in a table cell
                for cell in all_cells:
                    detail_page_link = '/'.join(self.base_url.split('/')[:-2]) + \
                                       '/' + cell.a.get('href').split('/')[1:][0]
                    all_links.append(detail_page_link)
                    print("got link: " + detail_page_link)
            except:
                print("failed to get content from index page " + url)
                continue  # malformity

            print("got content from " + url)

        return all_links

    def grab_content_from_page(self, detail_page_url, fetch_img_file):

        try:
            index_page = urllib2.urlopen(detail_page_url).read()
        except urllib2.HTTPError:
            print 'FAIL ' + detail_page_url
            return False

        soup = BeautifulSoup(index_page)

        img = ''
        for l in soup.findAll('a'):
            try:
                if str(l.contents[0]) == '1280':  # designer lady wants the 1280 image, sometimes there isn't one..
                    img = str(l.get('href'))
            except (IndexError, UnicodeEncodeError), e:
                pass  # none or strange link contents no worries

        if not img:
            print 'no suitable image url found at ' + url
            return False  # if we can't get the 1280 image we are passing on this page ..

        try:
            title = soup.findAll('a', {'id': 'example1'})[0].get('title'
                    )
        except IndexError:
            print 'could not find title'
            return False  # no title no post move along

        # fetch the image so we have it locally
        if fetch_img_file:
            local_img_file = self.fetch_remote_file(self.base_url_wallpapers + img, True)
            if not local_img_file:
                print "couldn't fetch remot file it, move along"
                return False
        else:
            local_img_file = False

        # scrape the content and clean it up a bit..
        content = re.findall(r'<div class="caption-text">\s*(.*?)\s*<div class="social">' \
                       , ' '.join(str(soup).splitlines()))[0]
        soup_content = BeautifulSoup(content)
        content = soup_content.prettify()
        content = self.prepare_content(content, detail_page_url)

        return {'title': title, 'content': content, 'page_url': detail_page_url, 'img_url': self.base_url_wallpapers + img, 'local_img_file': local_img_file}


    def prepare_content(self, content, detail_page_url):

        # makes inline reletive links into direct links

        return content.replace('\n', ' ').replace('href="images/',
                'target = "_blank" href="http://hirise.lpl.arizona.edu/images/'
                ).replace('href="E',
                          'target = "_blank" href="http://hirise.lpl.arizona.edu/E'
                          ).replace('href="T',
                                    'target = "_blank" href="http://hirise.lpl.arizona.edu/T'
                                    ).replace('href="r',
                'target = "_blank" href="http://hirise.lpl.arizona.edu/r'
                ).replace('href="j',
                          'target = "_blank" href="http://hirise.lpl.arizona.edu/j'
                          ).replace('href="p',
                                    'target = "_blank" href="http://hirise.lpl.arizona.edu/p'
                                    ).replace('href="d',
                'target = "_blank" href="http://hirise.lpl.arizona.edu/d'
                ).replace('href="e',
                          'target = "_blank" href="http://hirise.lpl.arizona.edu/e'
                          ).replace('href="P',
                                    'target = "_blank" href="http://hirise.lpl.arizona.edu/P'
                                    )



# READY GO

scrape = Scrape(base_url=base_url, local_img_dir=local_img_dir,
                base_url_wallpapers=base_url_wallpapers)

all_links = scrape.grab_all_page_urls(page_min, page_max)

print("got all detail page links")

order = 0
posted = []
for detail_page_url in all_links:
    img_id = detail_page_url.split('/')[-1]

    if img_id in posted:
        continue

    posted.append(img_id)

    print 'fetching data from ' + detail_page_url
    try:
        data = scrape.grab_content_from_page(detail_page_url, False)
    except:
        print 'nope'
        continue  # move along

    if not data:
        print "couldn't get data from " + detail_page_url
        continue

    del data['local_img_file']
    data['id'] = img_id
    data['order'] = order
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    order = order + 1
