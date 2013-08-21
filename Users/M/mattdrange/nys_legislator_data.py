from urllib2 import urlopen
from scraperwiki import swimport
from scraperwiki.sqlite import save,select,attach

URL="http://sw.thomaslevine.com/disclosures.csv"
attach('open_book_new_york')

def load_disclosures():
  csv=urlopen(URL)
  d=swimport('csv2sw').csv2json(csv)
  save([],d,'disclosures')

def join():
  disclosures=select('Entity,upper(Entity) as "ENTITY" from disclosures where entity is not null')
  disclosures_cleaned=[{
    "raw":row['Entity']
  , "clean":remove_ny(row['ENTITY']).strip()
  } for row in disclosures]
  save([],disclosures_cleaned,'disclosures_cleaned')


  licenses=select('Vendor,upper(Vendor) as "VENDOR" from swdata where Vendor is not null')
  licenses_cleaned=[{
    "raw":row['Vendor']
  , "clean":remove_ny(row['VENDOR']).strip()
  } for row in licenses]
  save([],licenses_cleaned,'licenses_cleaned')

def remove_ny(string):
  for ny in ("N.Y.S.","NYS","NEW YORK STATE","NEW YORK","N.Y.","NY"):
    string=string.replace(ny,'')
  return string

#load_disclosures()
join()