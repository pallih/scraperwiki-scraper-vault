#The data collected here is for educational purposes only. It will only be used for a class research project. All data belongs to airbnb.

import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    r = requests.get('https://www.airbnb.se/s/Stockholm--Sweden', verify=False)
    if r.status_code==200:
        dom = lxml.html.fromstring(r.text)
        search_results = dom.cssselect('.search_result')
        if len(search_results):
            for result in search_results:
                # Great! This page contains ads to scrape.
                ad = {
                    'name': result.cssselect('a.name')[0].text_content().strip().replace(',',''),
                    'url': result.cssselect('a.name')[0].get('href')
                }

                
                r = requests.get('https://www.airbnb.se'+ad['url'], verify=False)
                dom = lxml.html.fromstring(r.text)
                ad['price per night'] = dom.cssselect('h2#price_amount')[0].text_content()
                scraperwiki.sqlite.save(['url'], ad)

                
            

scrape_ads()