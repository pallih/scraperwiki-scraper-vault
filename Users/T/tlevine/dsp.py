from urllib2 import urlopen
from time import time
from lxml.html import fromstring
from scraperwiki.sqlite import save as swsave

def dsp(url,save=True):
  html=urlopen(url).read()
  if save:
    swsave([],{
      "url":url
    , "html":html
    , "time":time()
    },'raw_pages')
  xml=fromstring(html)
  return xml

def test():
  dsp('http://www.tebabank.co.za/dist_branch_locs.php')

#test()