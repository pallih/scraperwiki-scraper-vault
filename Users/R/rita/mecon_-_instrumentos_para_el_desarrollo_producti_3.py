import scraperwiki           
import lxml.html
import urllib2
import urllib

print "Starting"

base_url = "http://www.tours.com/tours_vacations.htm?kwd=fishing&pg=%s"
header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=de45029e5e2fab4f6e5eef56515d6c1c; __utma=123692957.1658163614.1349740913.1349740913.1352756518.2; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }


def parse_list(root):
    """ Takes a listing page and indexes all the listings in it """
    for el in root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"): 
        page_url = "http://www.tours.com" + el.get("href");
        print "Tours.com Url: %s" % page_url  
        page_html = scraperwiki.scrape(page_url) 
        page = lxml.html.fromstring(page_html)
        
        links = page.cssselect("body div.lbbg.pp div.p.s a")
        operator_url = links[-1].get("href")
        print "Operator Url: %s" % operator_url
        operator_email = links[-2].get("href").replace("mailto:", "") # we want valid emails
        print "Operator Email: %s" % operator_email
    
        data = {
            'url': operator_url,
            'email': operator_email,
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="tours_com_fishing")


# not iterate over the pages 
count = 0
while True:
    print "On page %s" % count
    url = base_url % count # targets each page in the list
    req = urllib2.Request(url, None, header)  
    response = urllib2.urlopen(req)
    root = lxml.html.fromstring(response.read())

    # check if there are items, if not stop since you exceeded the total pages
    if not root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"):
        print "Reached end at page %s" % count
        break

    # this will parse the first listing page
    parse_list(root)
    print "Finished page %s" % count
    count = count + 1

