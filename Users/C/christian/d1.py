# This scraper extracts a list of TU Vienna master studies

import scraperwiki
import lxml.html 

# open index site
indexsite = scraperwiki.scrape("http://www.tuwien.ac.at/lehre/masterstudien/") 
indexroot = lxml.html.fromstring(indexsite)
# select all study programmes
for el in indexroot.cssselect("div.csc-textpic-text p strong a.link_intern"): 
 detailsite = scraperwiki.scrape("http://www.tuwien.ac.at/" + el.attrib['href']) 
 detailroot = lxml.html.fromstring(detailsite) 
 # select the title on the detail page for each study programme
 for el2 in detailroot.cssselect("div.csc-header.csc-header-n1 h1.csc-firstHeader"): 
   studyname = el2.text
 # save to database
 scraperwiki.sqlite.save(unique_keys=["study"], data={"study":"http://www.tuwien.ac.at/" +el.attrib['href'], "title":studyname})
# This scraper extracts a list of TU Vienna master studies

import scraperwiki
import lxml.html 

# open index site
indexsite = scraperwiki.scrape("http://www.tuwien.ac.at/lehre/masterstudien/") 
indexroot = lxml.html.fromstring(indexsite)
# select all study programmes
for el in indexroot.cssselect("div.csc-textpic-text p strong a.link_intern"): 
 detailsite = scraperwiki.scrape("http://www.tuwien.ac.at/" + el.attrib['href']) 
 detailroot = lxml.html.fromstring(detailsite) 
 # select the title on the detail page for each study programme
 for el2 in detailroot.cssselect("div.csc-header.csc-header-n1 h1.csc-firstHeader"): 
   studyname = el2.text
 # save to database
 scraperwiki.sqlite.save(unique_keys=["study"], data={"study":"http://www.tuwien.ac.at/" +el.attrib['href'], "title":studyname})
