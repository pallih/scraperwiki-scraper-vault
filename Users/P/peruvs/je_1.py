import scraperwiki
import lxml.html

urls = [
    "http://www.just-eat.ca/blog/delivery/edmonton/",
    "http://www.just-eat.ca/blog/delivery/edmonton/american/",
    "http://www.just-eat.ca/blog/delivery/edmonton/burger/",
    "http://www.just-eat.ca/blog/delivery/edmonton/chinese/",
    "http://www.just-eat.ca/blog/delivery/edmonton/greek/",
    "http://www.just-eat.ca/blog/delivery/edmonton/indian/",
    "http://www.just-eat.ca/blog/delivery/edmonton/jamaican/",
    "http://www.just-eat.ca/blog/delivery/edmonton/lebanese/",
    "http://www.just-eat.ca/blog/delivery/edmonton/mexican/",
    "http://www.just-eat.ca/blog/delivery/edmonton/middleeastern/",
    "http://www.just-eat.ca/blog/delivery/edmonton/pizza/",
    "http://www.just-eat.ca/blog/delivery/edmonton/sushi/",
    "http://www.just-eat.ca/blog/delivery/edmonton/thai/",
    "http://www.just-eat.ca/blog/delivery/edmonton/vietnamese/",
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
