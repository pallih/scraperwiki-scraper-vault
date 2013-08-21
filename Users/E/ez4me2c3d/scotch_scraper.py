import scraperwiki
import lxml.html
import mechanize
import time
import re

site = 0
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def cask_store_np(page):
    print "Looking For Next Page Link"
    root = lxml.html.fromstring(page)
    for link in br.links():
        if link.text == "Next[IMG]":
            print "Found Next Link"
            break
    try:
        print "Sending HTTP Request"
        response = br.follow_link(link)
        html = response.read()
        print "Received HTTP Response"
        scrape_page(html)
    except:
        pass

def surdyks_np(page):
    print "Looking For Next Page Link"
    root = lxml.html.fromstring(page)
    try:
        next_page = re.findall(r'(ctl00\$CPH\$ctl00\$FV\$RG\$ctl01\$ctl02\$ctl00\$ctl07)', root.xpath("//a[@title='Next Page'][1]")[0].get('href'))[0]
        br.select_form(name="aspnetForm")
        br.set_all_readonly(False)
        try:
            email = br.form.find_control("ctl00$ucSecondaryNavigationTop$ImageButtonEmailSignUp")
            email.disabled = True
        except:
            pass
        br["__EVENTTARGET"] = "ctl00$CPH$ctl00$FV$RG$ctl01$ctl02$ctl00$ctl07"
        try:
            print "Found Next Page Link"
            print "Sending HTTP Request"
            next_page = br.submit()
            html = next_page.read()
            print "Received HTTP Response"
            scrape_page(html)
        except:
            pass
    except:
        pass

def scrape_page(page):
    print "Starting Page Scraper"
    scrape_datetime  = int(time.mktime(time.localtime()))
    
    html_root = lxml.html.fromstring(page)
    
    products = html_root.xpath(site['xpath_products'])
    print "Found %d Items" % (len(products))
    
    for product in products:
        try:
            try:
                name = re.findall(site['regex_name'], product.xpath(site['xpath_name'])[0].text)[0].strip()
            except:
                pass
            else:
                try:
                    price = re.findall(site['regex_price2'], product.xpath(site['xpath_price2'])[0].text)[0]
                except:
                    try:
                        price = re.findall(site['regex_price'], product.xpath(site['xpath_price'])[0].text)[0]
                    except:
                        price = ''

                try:
                    size = re.findall(site['regex_size'], product.xpath(site['xpath_size'])[0].text_content())[0]
                except:
                    size = ''

                try:
                    unit = re.findall(site['regex_unit'], product.xpath(site['xpath_unit'])[0].text_content())[0].upper()
                    if unit == "L":
                        unit = "LT"
                except:
                    unit = ''
    
                print "%s has a %s %s of %s for $%s" % (site['long_name'], size, unit, name, price)
                
                scraperwiki.sqlite.save(
                    ['timestamp', 'store_short_name', 'store_long_name', 'product_name', 'product_price', 'product_size', 'size_unit'],
                    {
                        'timestamp': scrape_datetime,
                        'store_short_name': site['short_name'],
                        'store_long_name': site['long_name'],
                        'product_name': name,
                        'product_price': price,
                        'product_size': size,
                        'size_unit': unit
                    }
                )
                
        except:
            pass
    
    if len(products) != 0 and site.has_key('next_page'):
        site['next_page'](page)

def main():
    global site
    for site in sites:
        if site['enabled']:
            print "Site: %s" % (site['long_name'])
            print "Sending HTTP Request"
            http_resp = br.open(site['url'])
            html = http_resp.read()
            print "Recieved HTTP Response"
            scrape_page(html)

sites = [
    {
        'enabled': True,
        'short_name': 'france_44',
        'long_name': 'France 44 Wine and Spirits',
        'url': "http://www.france44.com/browse.cfm/scotch/2,712.html?VIEW=ALL",
        'xpath_products': "//div[@class='tiledItem']",
        'xpath_name': ".//a[@class='tiledItemNameLink']/b",
        'xpath_price': ".//span[@class='itemSellPrice']",
        'xpath_size': ".//span[@class='itemSellPrice']",
        'xpath_unit': ".//span[@class='itemSellPrice']",
        'regex_name': r'.+',
        'regex_price': r'^\$(\d+\.\d+)',
        'regex_size': r'(\d+)$',
        'regex_unit': r'(LT|ML)'
    },
    {
        'enabled': True,
        'short_name': 'surdyks',
        'long_name': "Surdyk's Liquor",
        'url': "http://www.surdyks.com/SubCategoryDetail.aspx?CategoryName=SingleMaltScotch",
        'xpath_products': "//div[@class='productItem']",
        'xpath_name': ".//span[substring(@id, string-length(@id)-20)='ShortDescriptionLabel']",
        'xpath_price': ".//span[substring(@id, string-length(@id)-15)='LabelSinglePrice']",
        'xpath_price2': ".//span[substring(@id, string-length(@id)-19)='LabelSingleSalePrice']",
        'xpath_size': ".//div[@class='detail-left']/div[2]",
        'xpath_unit': ".//div[@class='detail-left']/div[2]",
        'regex_name': r'.+',
        'regex_price': r'^\$(\d+\.\d+)',
        'regex_price2': r'^\$(\d+\.\d+)',
        'regex_size': r'(\d+)',
        'regex_unit': r'([mM][lL]|[lL][tT]*)',
        'next_page': surdyks_np
    },
    {
        'enabled': True,
        'short_name': 'cask_store',
        'long_name': "Cask Store",
        'url': "http://www.caskstore.com/spirits/whisk-e-y/scotch-whisky?p=1",
        'xpath_products': "//td[@class='item']",
        'xpath_name': ".//h5",
        'xpath_price': ".//span[@class='price']",
        'regex_name': r'.+',
        'regex_price': r'^\$(\d+\.\d+)',
        'next_page': cask_store_np
    }
]

main()