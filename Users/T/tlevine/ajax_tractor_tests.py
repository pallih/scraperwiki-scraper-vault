from scraperwiki.sqlite import attach,select
import requests
from json import dumps
from time import time,sleep

url="https://views.scraperwiki.com/run/ajax_tractor/"

def test_wrapper(test_func):
  attach('scraperwiki_events_eventbrite_guestlists')
  original_data=select('* from `ny` where `Twitter Handle`="thomaslevine";')

  table_name=test_func(original_data)
  sleep(5)

  attach('ajax_tractor')
  ajaxed_data=select('* from `%s` where `Twitter Handle`="thomaslevine";' % table_name)
  print original_data,ajaxed_data
  print original_data==ajaxed_data

def t1(original_data):
  table_name=str(int(time()))
  r=requests.post(url,{
    "data":dumps(original_data)
  , "table_name":table_name
  })
  print r.content
  return table_name

def foo(original_data):
  return 'ny'

#test_wrapper(foo)
test_wrapper(t1)