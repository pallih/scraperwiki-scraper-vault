import scraperwiki
import lxml.html    

root = scraperwiki.scrape('http://www.edwardtufte.com/bboard/q-and-a?topic_id=1')
content = lxml.html.etree.HTML(root)
tds = content.xpath("//tr/td")

for td in tds:
    
    if ''.join(td.xpath("a/@href")).startswith("q-and-a-fetch-msg?msg_id="):
        data = {
            'link' : 'http://www.edwardtufte.com/bboard/' + td.xpath("a/@href")[0],
            'text' : td.xpath("a/text()")[0],
            'stars' : '0'
        }
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    elif ''.join(td.xpath("font/text()")) == "***":
        data = {
            'link' : 'http://www.edwardtufte.com/bboard/' + td.xpath("following-sibling::td/a/@href")[0],
            'text' : td.xpath("following-sibling::td/a/text()")[0],
            'stars' : '3'
        }
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
        

# to do: get authors
# to do: remove dups


    