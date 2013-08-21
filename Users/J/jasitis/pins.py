from urllib2 import urlopen
from lxml.html import fromstring
from time import time
from scraperwiki.sqlite import save

#The view counts of threadss in this dictionary will be tracked
threads={
  "pin":"http://pinterest.com/sameerg/feed.rss"
}

def get_count(html):
  xml=fromstring(html)
  count_str=xml.xpath('id("watch-actions-right")/descendant::strong/text()')[0]
  count=int(count_str.replace(',',''))
  return count

def scrape_thread(key,url):
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
  for key in threads.keys():
    html,count=scrape_threads(key,threadsS[key])
    save([],{
      "threads_key":key
    , "html":html
    , "view_count":count
    , "date":time()
    },'pages')
    save([],{
      "threads_key":key
    , "view_count":count
    , "date":time()
    },'counts')

main()