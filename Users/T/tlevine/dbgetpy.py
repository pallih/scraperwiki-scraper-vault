"""Save a URL directly to the datastore, and
retrieve urls directly from the datastore."""
from urllib2 import urlopen,HTTPError,URLError as urllib2_URLError
from httplib import BadStatusLine
from scraperwiki.sqlite import save,select,show_tables

class PageNotSavedError(Exception):
  def __init__(self, url):
    self.url=url

class DatastoreError(Exception):
  def __init__(self, url,message):
    self.url=url
    self.message=message

class ConnectionError(Exception):
  "Raised when a page has errors making it inconvenient to save this way."
  def __init__(self, url, exception):
    self.url=url
    self.exception=exception

class URLError(Exception):
  "Raised when a URL does not point to anything."
  def __init__(self, url, exception):
    self.url=url
    self.exception=exception

def badurl(url,e):
  "Raise an error if a url doesn't point anywhere."
  print """
The page you requested, %s, does not seem to exist.
Check whether the url is correct.

If it is, the server may have some problems. Try
wrapping this function in a loop that retries it
on an exception.

If you are brute-forcing a bunch of possible urls,
wrap this in a loop that handles this exception.
""" % url
  raise URLError(url,e)


def badpage(url,e):
  "Raise an error if a page doesn't load."
  print """
The page you requested, %s, is behaving strangely.
Check whether the url is correct.

If it is, the server may have some problems. Try
wrapping this function in a loop that retries it
on an exception.

If that doesn't work, you may need to write your
own function to download and save the page.
""" % url
  raise ConnectionError(url,e)

def save_page(url,table_name="pages"):
  "Save a url directly to the datastore."
  try:
    handle=urlopen(url)
    text=handle.read()
  except urllib2_URLError as e:
    badurl(url,e)
  except HTTPError as e:
    badurl(url,e)
  except BadStatusLine as e:
    badpage(url,e)
  else:
    d={"url":url,"text":text}
    save(['url'],d,table_name)

def get_page(url,table_name="pages"):
  if not table_name in show_tables():
    raise PageNotSavedError(url)
  else:
    rows=select("`text` from %s where url=?" % table_name,[url])
    l=len(rows)
    if l==0:
      raise PageNotSavedError(url)
    elif l>1:
      raise DatastoreError(url,"Multiple rows match this url.")
    elif l==1:
      if not 'text' in rows[0].keys():
        raise DatastoreError(url,"The database does not have a `text` column.")
      else:
        return rows[0]['text']


#Tests

#import unittest
#class TestGetPage(unittest.TestCase):
#  def test_good_page(self):
#    url="https://scraperwiki.com/scrapers/dbgetpy/"
#    get_page(url)
#    row=select('* from `pages` where url=?',[url])[0]
#    assertEqual(set(row.keys()),set(["url","text"]))
#    assertIn("dbget=swimport('dbgetpy')",row['text'])

#if __name__ == '__main__':
#  print "Running tests"
#  unittest.main()
#else:
#  import os
#  print "Running from bash"
#  print os.execvp("python",["script.py"])