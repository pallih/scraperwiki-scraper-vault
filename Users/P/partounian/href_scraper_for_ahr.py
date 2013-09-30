import scraperwiki
import lxml.html as lh


for i in range(1, 21):
    list_html = scraperwiki.scrape('http://ahr13.mapyourshow.com/5_0/exhibitor_results.cfm?alpha=%40&type=alpha&page=' + str(i) + '#GoToResults')
    list_html_root = lh.fromstring(list_html)
# Get the hrefs
    hrefs = list_html_root.xpath('//td[@class="mys-elastic mys-left"]/a')
  
    try:
            for href in hrefs:
                url_list = 'http://ahr13.mapyourshow.com' + href.attrib['href'] 
                data = {}
                data['id'] = url_list
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % url_list
        break
        import scraperwiki
import lxml.html as lh


for i in range(1, 21):
    list_html = scraperwiki.scrape('http://ahr13.mapyourshow.com/5_0/exhibitor_results.cfm?alpha=%40&type=alpha&page=' + str(i) + '#GoToResults')
    list_html_root = lh.fromstring(list_html)
# Get the hrefs
    hrefs = list_html_root.xpath('//td[@class="mys-elastic mys-left"]/a')
  
    try:
            for href in hrefs:
                url_list = 'http://ahr13.mapyourshow.com' + href.attrib['href'] 
                data = {}
                data['id'] = url_list
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % url_list
        break
        