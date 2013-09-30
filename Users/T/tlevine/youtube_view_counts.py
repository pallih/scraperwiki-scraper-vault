from urllib2 import urlopen
from lxml.html import fromstring
from time import time
from scraperwiki.sqlite import save

#The view counts of videos in this dictionary will be tracked
VIDEOS={
  "rap-news":"http://www.youtube.com/watch?v=j-rxe9Ayb8c"
, "occupy-thank-you":"http://www.youtube.com/watch?v=YZ6dNVRJEUA"
}

def get_count(html):
  xml=fromstring(html)
  count_str=xml.xpath('id("watch-actions-right")/descendant::strong/text()')[0]
  count=int(count_str.replace(',',''))
  return count

def scrape_video(key,url):
  html=urlopen(url).read()
  count=get_count(html)
  return html,count

def main():
  """
Save the whole page and just the view counts.

Use separate files so you can download it without the pages.

Name the one without pages first in alphabetical order
so you don't see the enormous html when you open the scraper overview.
"""
  for key in VIDEOS.keys():
    html,count=scrape_video(key,VIDEOS[key])
    save([],{
      "video_key":key
    , "html":html
    , "view_count":count
    , "date":time()
    },'pages')
    save([],{
      "video_key":key
    , "view_count":count
    , "date":time()
    },'counts')

main()from urllib2 import urlopen
from lxml.html import fromstring
from time import time
from scraperwiki.sqlite import save

#The view counts of videos in this dictionary will be tracked
VIDEOS={
  "rap-news":"http://www.youtube.com/watch?v=j-rxe9Ayb8c"
, "occupy-thank-you":"http://www.youtube.com/watch?v=YZ6dNVRJEUA"
}

def get_count(html):
  xml=fromstring(html)
  count_str=xml.xpath('id("watch-actions-right")/descendant::strong/text()')[0]
  count=int(count_str.replace(',',''))
  return count

def scrape_video(key,url):
  html=urlopen(url).read()
  count=get_count(html)
  return html,count

def main():
  """
Save the whole page and just the view counts.

Use separate files so you can download it without the pages.

Name the one without pages first in alphabetical order
so you don't see the enormous html when you open the scraper overview.
"""
  for key in VIDEOS.keys():
    html,count=scrape_video(key,VIDEOS[key])
    save([],{
      "video_key":key
    , "html":html
    , "view_count":count
    , "date":time()
    },'pages')
    save([],{
      "video_key":key
    , "view_count":count
    , "date":time()
    },'counts')

main()