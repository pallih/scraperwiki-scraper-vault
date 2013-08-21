import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://search.ucas.com/cgi-bin/hsrun/search/search/search.hjx;start=search.HsCodeSearch.run")
#print html

root = lxml.html.fromstring(html)
for option in root.cssselect("select[id='cmbInst'] option"):
        data = {
            'inst_code' : option.text_content().split()[0],
            'inst_name' : option.text_content().partition(' ')[2]
        }
        if option.text_content().split()[0] <> 'all':
            scraperwiki.sqlite.save(unique_keys=['inst_code'], data=data)