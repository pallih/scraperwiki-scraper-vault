"""
How this site works
==========
Mortals access the data through [this page](http://www.absa.co.za/Absacoza/Contact-Us).

Searching with the search bar brings you here,

    https://e91.absa.co.za/esl/locatorResult.do?Quicksearch=true&Invalid=true&Token=%s

where "%s" refers to the search string. Clicking "next" brings you here,

    https://e91.absa.co.za/esl/locatorResult.do

presumably using cookies.

"""
from scraperwiki.sqlite import save,save_var,get_var
from scraperwiki import swimport
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep
from string import ascii_lowercase
from time import time
from mechanize import Browser,URLError
from lxml.html import fromstring,tostring

def main():
  if None==get_var('DATE'):
    save_var('DATE',time())

  searchTerms=get_searchTerms()
  for searchTerm in searchTerms:
    d=paginate(searchTerm)
    for row in d:
      row['date_scraped']=get_var('DATE')
      row['searchTerm']=searchTerm

    save_var('previous_searchTerm',searchTerm)
    save(['date_scraped', 'Name'],d,'initial')

  save_var('previous_searchTerm',None)
  save_var('DATE',None)

def get_searchTerms():
  searchTerm=get_var('previous_searchTerm')
  if searchTerm==None:
    i=0
  else:
    i=ascii_lowercase.index(searchTerm)+1
  return ascii_lowercase[i:]

def paginate(searchTerm,verbose=True):
  if verbose:
    print('Searching for "%s"' % searchTerm)
  d=[]
  s=Searching(searchTerm)

  if s.on_last_page()==False:
    d.extend(s.parse())

  while False==s.on_last_page():
    s.nextpage()
    d.extend(s.parse())
    randomsleep()
  return d

class Searching(Browser):
  def __init__(self,searchString):
    Browser.__init__(self)
    self.set_handle_robots(False)
    while True:
      try:
        self.r=self.open("https://e91.absa.co.za/esl/locatorResult.do?Quicksearch=true&Invalid=true&Token=%s" % searchString).read()
      except URLError:
        randomsleep(80)
        pass
      else:
        break
    self.x=fromstring(self.r)

  def nextpage(self):
    "POST the next page and load the html."
    self.select_form('Buttonform')
    self.r=self.submit(name='button_Next',label='Next').read()
    self.x=fromstring(self.r)

  def on_last_page(self):
    return 0==self.x.xpath('count(//input[@type="submit" and @name="button_Next" and @value="Next"])')

  def parse(self,verbose=True):
    if verbose:
      print(tostring(self.x))
    colnames=map(keyify,self.x.xpath('//table[position()=1]/tr[count(th)="4"]/th/p/text()'))
    assert len(colnames)==4,colnames
    trs=self.x.xpath('//table[position()=1]/tr[count(td)="4"]')
    return [dict(zip(colnames,tr.xpath('td/text()'))) for tr in trs]

main()