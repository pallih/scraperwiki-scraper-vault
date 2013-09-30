import scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import json

url = "http://www.fanfiction.net/s/5782108/1/Harry_Potter_and_the_Methods_of_Rationality"
page = lxml.html.parse(url).getroot()
page = page.xpath("//select[@name='chapter']")[0].findall('option')
chapmax = len(page)

for chapt in range(1,chapmax+1):
    chapter = {}
    chapter['num'] = chapt

    url = "http://www.fanfiction.net/r/5782108/%s/1/" % (chapt)
    apiurl = "http://sharedcount.com/api/?url=http://www.fanfiction.net/s/5782108/%s/Harry_Potter_and_the_Methods_of_Rationality" % (chapt)

    page = lxml.html.parse(url).getroot()
    metadata = json.loads(urllib2.urlopen(apiurl).read())
    #print apiurl

    chapter['twitter'] = metadata.get('Twitter', 0)
    chapter['buzz'] = metadata.get('Buzz', 0)
    chapter['digg'] = metadata.get('Digg', 0)
    chapter['delicious'] = metadata.get('Delicious', 0)
    chapter['stumbleupon'] = metadata.get('StumbleUpon', 0)
    if metadata['Facebook'] is not None:
        chapter['fb click cnt'] = metadata['Facebook'].get('click_count', 0)
        chapter['fb shar cnt'] = metadata['Facebook'].get('share_count', 0)
        chapter['fb like cnt'] = metadata['Facebook'].get('like_count', 0)
        chapter['fb comm cnt'] = metadata['Facebook'].get('comment_count', 0)
        chapter['fb totl cnt'] = metadata['Facebook'].get('total_count', 0)
        chapter['fb comm fid'] = metadata['Facebook'].get('comments_fbid', 0)
        chapter['fb cbox cnt'] = metadata['Facebook'].get('commentsbox_count', 0)

    if page is not None:

        revs2 = page.find_class("alt2")
        revs1 = page.find_class("alt1")
        revs = revs2 + revs1
        
        chapter['reviews'] = len(revs)

        chapter['review_words'] = 0

        for item in revs:
            try:
                chapter['review_words'] += len(str.split( item.find('td/div').text_content() ))
            except TypeError:
                chapter['review_words'] += len(unicode.split( item.find('td/div').text_content() ))

        chapter['words_per_review'] = chapter['review_words'] / chapter['reviews']
               
    scraperwiki.sqlite.save(["num"], chapter) # save the records one by oneimport scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import json

url = "http://www.fanfiction.net/s/5782108/1/Harry_Potter_and_the_Methods_of_Rationality"
page = lxml.html.parse(url).getroot()
page = page.xpath("//select[@name='chapter']")[0].findall('option')
chapmax = len(page)

for chapt in range(1,chapmax+1):
    chapter = {}
    chapter['num'] = chapt

    url = "http://www.fanfiction.net/r/5782108/%s/1/" % (chapt)
    apiurl = "http://sharedcount.com/api/?url=http://www.fanfiction.net/s/5782108/%s/Harry_Potter_and_the_Methods_of_Rationality" % (chapt)

    page = lxml.html.parse(url).getroot()
    metadata = json.loads(urllib2.urlopen(apiurl).read())
    #print apiurl

    chapter['twitter'] = metadata.get('Twitter', 0)
    chapter['buzz'] = metadata.get('Buzz', 0)
    chapter['digg'] = metadata.get('Digg', 0)
    chapter['delicious'] = metadata.get('Delicious', 0)
    chapter['stumbleupon'] = metadata.get('StumbleUpon', 0)
    if metadata['Facebook'] is not None:
        chapter['fb click cnt'] = metadata['Facebook'].get('click_count', 0)
        chapter['fb shar cnt'] = metadata['Facebook'].get('share_count', 0)
        chapter['fb like cnt'] = metadata['Facebook'].get('like_count', 0)
        chapter['fb comm cnt'] = metadata['Facebook'].get('comment_count', 0)
        chapter['fb totl cnt'] = metadata['Facebook'].get('total_count', 0)
        chapter['fb comm fid'] = metadata['Facebook'].get('comments_fbid', 0)
        chapter['fb cbox cnt'] = metadata['Facebook'].get('commentsbox_count', 0)

    if page is not None:

        revs2 = page.find_class("alt2")
        revs1 = page.find_class("alt1")
        revs = revs2 + revs1
        
        chapter['reviews'] = len(revs)

        chapter['review_words'] = 0

        for item in revs:
            try:
                chapter['review_words'] += len(str.split( item.find('td/div').text_content() ))
            except TypeError:
                chapter['review_words'] += len(unicode.split( item.find('td/div').text_content() ))

        chapter['words_per_review'] = chapter['review_words'] / chapter['reviews']
               
    scraperwiki.sqlite.save(["num"], chapter) # save the records one by one