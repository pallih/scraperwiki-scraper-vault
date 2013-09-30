import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.grosserrat.bs.ch/de/mitglieder-gremien/mitglieder-a-z")
root = lxml.html.fromstring(html)

for x in range (0, 101):
    
    el = root.cssselect("ul.ri_fe_miglieder_ul div.ri_fe_miglieder_div1")[x]           
    unique_key = el.text_content()
    el = root.cssselect("ul.ri_fe_miglieder_ul a")[x]           
    url = el.attrib['href']
    subpage_html = scraperwiki.scrape(url)
    subpage_root = lxml.html.fromstring(subpage_html)
    subpage_el = subpage_root.cssselect("div#gr_cms_mit_div_content_detail div")[3]
    out = lxml.html.tostring(subpage_el)
    out2 = lxml.html.fromstring(out)
    verbindungen = out2.text_content()
    
    data = {
            'key' : 1
            'verbindungen' : out2.text_content()
        }
    
    scraperwiki.sqlite.save(unique_keys=['key'], data=data)
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.grosserrat.bs.ch/de/mitglieder-gremien/mitglieder-a-z")
root = lxml.html.fromstring(html)

for x in range (0, 101):
    
    el = root.cssselect("ul.ri_fe_miglieder_ul div.ri_fe_miglieder_div1")[x]           
    unique_key = el.text_content()
    el = root.cssselect("ul.ri_fe_miglieder_ul a")[x]           
    url = el.attrib['href']
    subpage_html = scraperwiki.scrape(url)
    subpage_root = lxml.html.fromstring(subpage_html)
    subpage_el = subpage_root.cssselect("div#gr_cms_mit_div_content_detail div")[3]
    out = lxml.html.tostring(subpage_el)
    out2 = lxml.html.fromstring(out)
    verbindungen = out2.text_content()
    
    data = {
            'key' : 1
            'verbindungen' : out2.text_content()
        }
    
    scraperwiki.sqlite.save(unique_keys=['key'], data=data)
