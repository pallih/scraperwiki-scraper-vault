import scraperwiki
start_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors'
def scrape_site(start_url):
    html_cintent = scraperwiki.scrape(start_url)
    root = lxml.html.fromstring(html_content)
    data_list = root.cssselect('div[id="col1_content"] div')
    for item in data_list:
        com_link=item.cssselect('a.href')
        print comp_link
def scrape_info(comp_link):
    pass
# Blank Python


