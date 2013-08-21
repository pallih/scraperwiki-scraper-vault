from time import time as now,sleep
from scraperwiki.sqlite import save as swsave
SCRIPTS=('script.rb','script.py','script.php')

class Scraper():
  def __init__(self):
    baz={}
    for s in SCRIPTS:
      baz[s]=''
    self.current=baz
    self.last=baz

  def scrape(self):
    for s in SCRIPTS:
      self.current[s]=open(s,'r').read()

  def save(self):
    date=now()
    for s in SCRIPTS:
      changed=(self.last[s]!=self.current[s]) #Check the last dict
      d={"date":date,"file":s,"changed":changed}
      if changed:
        d["contents"]=self.last[s]
      swsave([],d,'scripts')
      self.last[s]=self.current[s] #Overwrite the last dict now that we've checked it

scraper=Scraper()
while True:
  scraper.scrape()
  scraper.save()
  sleep(5*60)
