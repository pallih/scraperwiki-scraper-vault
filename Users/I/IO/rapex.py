import scraperwiki
import lxml.etree
import urllib2

def scrapePageWise(listID):
    url="http://ec.europa.eu/consumers/dyna/rapex/rapex_xml_en.cfm?rx_id="+str(listID)
    lookupUrl="http://ec.europa.eu/consumers/dyna/rapex/create_rapex.cfm?rx_id="+str(listID)
    src = urllib2.urlopen(url).read()
    try:
        root = lxml.etree.fromstring(src)
        week=root.findtext("report_week")
        year=root.findtext("report_year")
        products = root.findall("product")
        for product in products:
            ref=product.findtext("refnr")
            cty=product.findtext("country")
            desc=product.findtext("descript")
            danger=product.findtext("danger")
            measures=product.findtext("measures")

            
            scraperwiki.sqlite.save(unique_keys=['ID'], data={
                                        'ID':ref,
                                        'url':lookupUrl,
                                        'week':week,'year':year,
                                        'country':cty,
                                        'descr':desc,
                                        'danger':danger,
                                        'measures':measures
                                      })


    except:
        pass



for i in range (269,217,-1):
    try:
        print i
        scrapePageWise(i)
    except:
        pass
