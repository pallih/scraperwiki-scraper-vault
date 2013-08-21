"""
"Caterpillar":http://www.cat.com/equipment/wheel-tractor-scrapers wheel tractor-scraper models

h3. Brand inspiration

People

* "Mine engineer":http://en.wikipedia.org/wiki/Mining_engineering
* "* Operator":http://jobs.aol.com/jobs-by-title/earth-moving-equipment-operator-jobs/
* "Earthmoving *":http://www.careerjet.com.au/earthmoving-jobs.html
* "Deisel mechanic":http://diesel-mechanic.net/
* "Heavy Civil Project Estimator":http://www.americasjobexchange.com/job-detail/job-opening-AJE-554634478?source=carjet&utm_source=careerjet&utm_medium=standard
* "More":http://duckduckgo.com/?q=earthmoving+jobs

Vehicle

* "Tournahoppers":http://en.wikipedia.org/wiki/Wheel_tractor-scraper
* "R.G. LeTourneau":http://en.wikipedia.org/wiki/R._G._LeTourneau
* "Earthmoving":http://en.wikipedia.org/wiki/Earthworks_(engineering)
* "Heavy equipment":http://en.wikipedia.org/wiki/Heavy_equipment
* "Hydrolics":http://en.wikipedia.org/wiki/Hydraulics

Disciplines/Projects
* "Cut and fill":http://en.wikipedia.org/wiki/Cut_and_fill
* "Transportation":http://en.wikipedia.org/wiki/Transport_engineering
* "Glossary of mining terms":https://scraperwiki.com/scrapers/coal_mining_glossary/

==========

There's way much Javascript for non-current models for me
to feel like parsing the Javascript. I'll just use a Chrome
extension or something.

http://www.cat.com/cmms/xslt/cmms.js

http://www.cat.com/cda/jsp/cdaTransform.jsp?xslt=/cmms/xslt/subFamily-range.xsl&xml=/cmms/xslt/_en/746/752589_en.xml&xml=/cmms/xslt/_en/746/752580_en.xml&xml=/cmms/xslt/_en/746/752581_en.xml&xml=/cmms/xslt/_en/746/752588_en.xml&xml=/cmms/xslt/_en/746/752596_en.xml&xml=/cmms/xslt/_en/746/752584_en.xml&xml=/cmms/xslt/_en/746/752587_en.xml&xml=/cmms/xslt/_en/746/752597_en.xml&xml=/cmms/xslt/_en/746/752586_en.xml&xml=/cmms/xslt/_en/746/752593_en.xml&xml=/cmms/xslt/_en/746/752585_en.xml&xml=/cmms/xslt/_en/746/752594_en.xml&xml=/cmms/xslt/_en/746/752582_en.xml

"""

from scraperwiki.sqlite import save,select,show_tables
from scraperwiki import swimport
from urllib2 import urlopen
from lxml.html import fromstring,HtmlElement,tostring
keyify=swimport('keyify').keyify

DOMAIN="http://www.cat.com"
MENU="http://www.cat.com/equipment/wheel-tractor-scrapers"

NUMERIC=('Capacity','Power','Rated_Load')

def main():
  if 'productlines' not in show_tables():
    save(['href'],getproductlinelinks(MENU),'productlines')
  hrefs=[row['href'] for row in select('href from productlines')]
  for href in hrefs:
    p=ProductLine(href)
    t=p.current_models_table()

    #Overview
    save(['href'],p.overview(),'overview')

    #Specifications
    save([],t.specifications(units="english"),'specifications')
    save([],t.specifications(units="metric"),'specifications')

    #Links to models
    model_links=t.model_links()
    for model_link in model_links:
      model_link['product-line-href']=p.href
    save(['href'],model_links,'models')

    #Links to non-current models
    save([],p.noncurrent_models_link(),'current_noncurrent')

def cat_keyify(raw):
  for term in NUMERIC:
    if term in raw:
      return term

  #Otherwise
  return keyify(raw)

def getproductlinelinks(menuurl):
  x=load(menuurl)
  a_nodes=x.xpath('//a[@class="type-W sys"]')
  return map(getproductlinelink,a_nodes)

def getproductlinelink(a):  
  return {
    "product-line":a.xpath('preceding-sibling::div[@class="wideTicklerTitle"][position()=1]/h2/a/text()')[0]
  , "href":a.attrib['href']
  }

def load(url_or_href):
  if url_or_href[0]=="/":
    url=DOMAIN+url_or_href
  else:
    url=url_or_href
  return fromstring(urlopen(url).read())

def getone(tree,path):
  nodes=tree.xpath(path)
  assert 1==len(nodes)
  return nodes[0]

class ProductLine:
  def __init__(self,href):
    "Open the page"
    self.href=href
    self.x=load(self.href)

  def overview(self):
    "An overview info record"
    overview_nodes=self.x.xpath('//div[div/a[text()="Overview"]]/descendant::td[@valign="top"]')
    if len(overview_nodes)==0:
      overview_nodes=self.x.xpath('id("tabs-1")/descendant::td[@valign="top"]')
    overview_text='\n'.join([node.text_content() for node in overview_nodes])
    d={"href":self.href,"overview":overview_text}
    return d

  def current_models_table(self):
    table=self.x.get_element_by_id("contentList")
    return CurrentModelTable(table)

  def noncurrent_models_link(self):
    noncurrent_href=getone(self.x,'//*[text()="View Non-Current Models"]/@href')
    return {"current-models-href":self.href,"noncurrent-models-href":noncurrent_href}

class ModelTable:
  """A table with model information, wherein "model" is the primary key"""
  def __init__(self,table):
    "Table is an lxml object"
    if type(table)==HtmlElement:
      self.table=table
    else:
      raise TypeError

  def model_links(self):
    "The hrefs to the models"
    a_nodes=self.table.xpath('tbody/tr/td[position()=1]/a')
    return [{"href":a.attrib['href'],"model":a.text} for a in a_nodes]

  def table_rows(self,units):
    "A slightly cleaned list of lists for table row contents"
    return [[cell.text for cell in tr.xpath('descendant::*[self::th or self::a or self::div[@class="%s"]]' % units)] for tr in self.table.cssselect('tr')]

class CurrentModelTable(ModelTable):
  def specifications(self,units="english"):
    "The specifications table"
    rows=self.table_rows(units)
    header=map(cat_keyify,rows.pop(0))
    d=[dict(zip(["units"]+header,[units]+row)) for row in rows]
    for row in d:
      for term in NUMERIC:
        if row.has_key(term):
          value,unit=row[term].split(' ')
          row[term+'_value']=float(value)
          row[term+'_unit']=unit
          del(row[term])
    return d

def test():
  p=ProductLine(u'/equipment/wheel-tractor-scrapers/towed-scrapers')
  t=p.current_models_table()
  print tostring(t.table)
  print t.model_links()
  print t.table_rows("english")
  print t.table_rows("metric")
  print t.specifications()

main()
#test()