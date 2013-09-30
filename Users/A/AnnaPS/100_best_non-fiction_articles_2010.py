###############################################################################
# Getting all links from Conor Friedersdorf's list of the 100 best 
# long-form articles in 2010. 
###############################################################################

import scraperwiki
import lxml.html
# From Dirty Medicine (5) to Tokyo Hooters (103)
def scrape(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # split at elements with the style attribute "font-size: 1.5625em"
    results = {}
    for (i,e) in enumerate(root.xpath('.//div[@class="articleContent"]/a')):
        if (i<5) or (i>103) or (e.text=="story") or (e.text=="this episode"):
            continue
        results['publication'] = e.xpath('preceding-sibling::b')[-1].text.title()
        results['category'] = e.xpath('preceding-sibling::div/font')[-1].text
        results['link']=e.get('href')
        results['title']=e.text
        print results['title'], results['publication']
        scraperwiki.sqlite.save(['link'], results)

base_url = 'http://www.theatlantic.com/entertainment/archive/2011/05/nearly-100-fantastic-pieces-of-journalism/238230/'
scrape(base_url)
###############################################################################
# Getting all links from Conor Friedersdorf's list of the 100 best 
# long-form articles in 2010. 
###############################################################################

import scraperwiki
import lxml.html
# From Dirty Medicine (5) to Tokyo Hooters (103)
def scrape(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # split at elements with the style attribute "font-size: 1.5625em"
    results = {}
    for (i,e) in enumerate(root.xpath('.//div[@class="articleContent"]/a')):
        if (i<5) or (i>103) or (e.text=="story") or (e.text=="this episode"):
            continue
        results['publication'] = e.xpath('preceding-sibling::b')[-1].text.title()
        results['category'] = e.xpath('preceding-sibling::div/font')[-1].text
        results['link']=e.get('href')
        results['title']=e.text
        print results['title'], results['publication']
        scraperwiki.sqlite.save(['link'], results)

base_url = 'http://www.theatlantic.com/entertainment/archive/2011/05/nearly-100-fantastic-pieces-of-journalism/238230/'
scrape(base_url)
