import scraperwiki           
import lxml.html  
import re         

html = scraperwiki.scrape("http://maggi.is/transmit/new.php")
root = lxml.html.fromstring(html)

html = scraperwiki.scrape("http://maggi.is/transmit/")
root = lxml.html.fromstring(html)

def clean(text):
    cleaned = re.sub("\s\s+", "  ", text)
    return cleaned.strip()


for tr in root.cssselect("table")[1]:
    tds = tr.cssselect("td")
    if tds[0].text_content() == "!":
        continue

    data = {
      'timestamp' : tds[1].text_content(),
      'team_yellow' : clean(tds[2].text_content()),
      'team_yellow_score' : tds[3].text_content(),
      'team_red_score' : tds[4].text_content(),
      'team_red' : clean(tds[5].text_content()),
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data, table_name="foosregard")


import scraperwiki           
import lxml.html  
import re         

html = scraperwiki.scrape("http://maggi.is/transmit/new.php")
root = lxml.html.fromstring(html)

html = scraperwiki.scrape("http://maggi.is/transmit/")
root = lxml.html.fromstring(html)

def clean(text):
    cleaned = re.sub("\s\s+", "  ", text)
    return cleaned.strip()


for tr in root.cssselect("table")[1]:
    tds = tr.cssselect("td")
    if tds[0].text_content() == "!":
        continue

    data = {
      'timestamp' : tds[1].text_content(),
      'team_yellow' : clean(tds[2].text_content()),
      'team_yellow_score' : tds[3].text_content(),
      'team_red_score' : tds[4].text_content(),
      'team_red' : clean(tds[5].text_content()),
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data, table_name="foosregard")


