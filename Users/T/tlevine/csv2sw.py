import csv
from urllib2 import urlopen
from scraperwiki import swimport
keyify=swimport('keyify').keyify

def csv2dict(csvfile,*args,**kwargs):
  "Turn a csv file into a list of json dicts"
  r= csv.reader(csvfile,*args,**kwargs)
  header=[keyify(key) for key in r.next()]
  d=[dict(zip(header,row)) for row in r]
  return d

csv2json=csv2dict

class read:
  "Unnecessary class to make this read like R"

  @staticmethod
  def csv(url, na_strings = "NA"):
    h=urlopen(url)
    d = csv2dict(h)
    if na_strings != None:
      for row in d:
        for k,v in row.items():
          if v == na_strings:
            row[k] = None
    return dimport csv
from urllib2 import urlopen
from scraperwiki import swimport
keyify=swimport('keyify').keyify

def csv2dict(csvfile,*args,**kwargs):
  "Turn a csv file into a list of json dicts"
  r= csv.reader(csvfile,*args,**kwargs)
  header=[keyify(key) for key in r.next()]
  d=[dict(zip(header,row)) for row in r]
  return d

csv2json=csv2dict

class read:
  "Unnecessary class to make this read like R"

  @staticmethod
  def csv(url, na_strings = "NA"):
    h=urlopen(url)
    d = csv2dict(h)
    if na_strings != None:
      for row in d:
        for k,v in row.items():
          if v == na_strings:
            row[k] = None
    return d