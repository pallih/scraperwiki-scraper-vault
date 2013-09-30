import scraperwiki
import lxml.html           
html = scraperwiki.scrape("http://query.nictusa.com/cgi-bin/com_ind/C00432906/A-E/")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[tbody]"): 
    tds = tr.cssselect("td")
    data = {
      'Contributor' : tds[0].text_content(),
      'Address' : tds[1].text_content(),
      'Date' : int(tds[2].text_content()),
      'Amount' : int(tds[3].text_content()),
      'Employer' : tds[4].text_content(),
      'Image Number' : int(tds[5].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['Contributor'], data=data)import scraperwiki
import lxml.html           
html = scraperwiki.scrape("http://query.nictusa.com/cgi-bin/com_ind/C00432906/A-E/")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[tbody]"): 
    tds = tr.cssselect("td")
    data = {
      'Contributor' : tds[0].text_content(),
      'Address' : tds[1].text_content(),
      'Date' : int(tds[2].text_content()),
      'Amount' : int(tds[3].text_content()),
      'Employer' : tds[4].text_content(),
      'Image Number' : int(tds[5].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['Contributor'], data=data)