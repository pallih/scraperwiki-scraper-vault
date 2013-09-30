import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.hesa.ac.uk/index.php?option=com_collns&task=show_manuals&Itemid=233&r=06011&f=002")
#print html

root = lxml.html.fromstring(html)
tr = root.xpath('//*[@id="mainbody"]/div[2]/div/table[2]')
for tr in root.xpath('//*[@id="mainbody"]/div[2]/div/table[2]/tr'):
        tds = tr.cssselect("td")
        data = {
            'inst_code' : tds[0].text_content(),
            'inst_name' : tds[1].text_content()
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['inst_code'], data=data)import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.hesa.ac.uk/index.php?option=com_collns&task=show_manuals&Itemid=233&r=06011&f=002")
#print html

root = lxml.html.fromstring(html)
tr = root.xpath('//*[@id="mainbody"]/div[2]/div/table[2]')
for tr in root.xpath('//*[@id="mainbody"]/div[2]/div/table[2]/tr'):
        tds = tr.cssselect("td")
        data = {
            'inst_code' : tds[0].text_content(),
            'inst_name' : tds[1].text_content()
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['inst_code'], data=data)