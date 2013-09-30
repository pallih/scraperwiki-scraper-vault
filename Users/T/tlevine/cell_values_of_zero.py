"""Demonstration of cell values being rendered as zero"""
from scraperwiki.sqlite import save, execute
from time import time
from urllib2 import urlopen

def make_row():
  """Create a 0 and a 1 with save."""
  save([],{"1":1,"0":0},'0')

def drop_table():
  """In case you want to drop the test 1-0 table"""
  execute('DROP TABLE `0`')

def render_datastore():
  """Save the rendered pages"""
  URLS={
    "json":"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=cell_values_of_zero&query=select+*+from+`0`&apikey="
  , "csv":"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=cell_values_of_zero&query=select+*+from+`0`&apikey="
  , "html":"https://scraperwiki.com/scrapers/cell_values_of_zero/"
  }
  d={"time":time()}
  for key in URLS:
    d[key]=urlopen(URLS[key]).read()
  save([],d,'render')

make_row()
render_datastore()"""Demonstration of cell values being rendered as zero"""
from scraperwiki.sqlite import save, execute
from time import time
from urllib2 import urlopen

def make_row():
  """Create a 0 and a 1 with save."""
  save([],{"1":1,"0":0},'0')

def drop_table():
  """In case you want to drop the test 1-0 table"""
  execute('DROP TABLE `0`')

def render_datastore():
  """Save the rendered pages"""
  URLS={
    "json":"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=cell_values_of_zero&query=select+*+from+`0`&apikey="
  , "csv":"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=cell_values_of_zero&query=select+*+from+`0`&apikey="
  , "html":"https://scraperwiki.com/scrapers/cell_values_of_zero/"
  }
  d={"time":time()}
  for key in URLS:
    d[key]=urlopen(URLS[key]).read()
  save([],d,'render')

make_row()
render_datastore()