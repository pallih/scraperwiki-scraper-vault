from scraperwiki.sqlite import save,select,show_tables
from urllib import urlopen
from lxml.html import fromstring
from time import time


def scrape(url,table_name="swdata"):
  html=urlopen(url).read()
  x=fromstring(html)
  d=get_rsvp_lists(x)
  save([],d,table_name)
  save_attendee_counts(x)

def save_attendee_counts(x):
  save(['date'],{
    "meetup-attending":'\n'.join(x.xpath('//span[@class="rsvp-count-number rsvp-count-going"]/text()'))
  , "meetup-not":'\n'.join(x.xpath('id("no-list-count")/text()'))
  , "parse-attending":x.xpath('count(id("rsvp-list")/descendant::a[@class="mem-name"])')
  , "parse-not":x.xpath('count(id("rsvp-list-no")/descendant::a[@class="mem-name"])')
  , "date":time()
  },'attendee_counts')

def get_rsvp_lists(x):
  d=[]
  attending_ids={'rsvp-list':True,'rsvp-list-no':False}
  for id in attending_ids.keys():
    d.extend([dict(zip(["attending","name","member-page"],[attending_ids[id]]+a.xpath('text()')+a.xpath('attribute::href'))) for a in x.xpath('id("%s")/descendant::a[@class="mem-name"]' % id)])
  return d
