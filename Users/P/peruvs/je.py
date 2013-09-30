import scraperwiki
import lxml.html

urls = [
    "http://www.just-eat.ca/blog/delivery/calgary/american/",
    "http://www.just-eat.ca/blog/delivery/calgary/burger/",
    "http://www.just-eat.ca/blog/delivery/calgary/chinese/",
    "http://www.just-eat.ca/blog/delivery/calgary/greek/",
    "http://www.just-eat.ca/blog/delivery/calgary/indian/",
    "http://www.just-eat.ca/blog/delivery/calgary/jamaican/",
    "http://www.just-eat.ca/blog/delivery/calgary/lebanese/",
    "http://www.just-eat.ca/blog/delivery/calgary/mexican/",
    "http://www.just-eat.ca/blog/delivery/calgary/middleeastern/",
    "http://www.just-eat.ca/blog/delivery/calgary/pizza/",
    "http://www.just-eat.ca/blog/delivery/calgary/sushi/",
    "http://www.just-eat.ca/blog/delivery/calgary/thai/",
    "http://www.just-eat.ca/blog/delivery/calgary/vietnamese/",
]


for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    
    for rest in root.cssselect('div.w783 table.rl_rest'):
        if rest.cssselect('a.rest_name'):
            data = {
                'name': rest.cssselect('a.rest_name')[0].text_content(),
                'addy': rest.cssselect('td.greyText')[0].text_content(),
            }
        
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki
import lxml.html

urls = [
    "http://www.just-eat.ca/blog/delivery/calgary/american/",
    "http://www.just-eat.ca/blog/delivery/calgary/burger/",
    "http://www.just-eat.ca/blog/delivery/calgary/chinese/",
    "http://www.just-eat.ca/blog/delivery/calgary/greek/",
    "http://www.just-eat.ca/blog/delivery/calgary/indian/",
    "http://www.just-eat.ca/blog/delivery/calgary/jamaican/",
    "http://www.just-eat.ca/blog/delivery/calgary/lebanese/",
    "http://www.just-eat.ca/blog/delivery/calgary/mexican/",
    "http://www.just-eat.ca/blog/delivery/calgary/middleeastern/",
    "http://www.just-eat.ca/blog/delivery/calgary/pizza/",
    "http://www.just-eat.ca/blog/delivery/calgary/sushi/",
    "http://www.just-eat.ca/blog/delivery/calgary/thai/",
    "http://www.just-eat.ca/blog/delivery/calgary/vietnamese/",
]


for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    
    for rest in root.cssselect('div.w783 table.rl_rest'):
        if rest.cssselect('a.rest_name'):
            data = {
                'name': rest.cssselect('a.rest_name')[0].text_content(),
                'addy': rest.cssselect('td.greyText')[0].text_content(),
            }
        
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)
