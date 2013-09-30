import scraperwiki
import re
import lxml.html
from datetime import date

no = 0

while(1):
    html = scraperwiki.scrape("http://www.bikesales.com.au/all-bikes/results.aspx?Ns=p_IsPoa_Int32%7c0%7c%7cp_RankSort_Int32%7c1%7c%7cp_HasPhotos_Int32%7c1%7c%7cp_Make_String%7c0%7c%7cp_Model_String%7c0%7c%7cp_YearMade_Int32%7c1%7c%7cp_PriceSort_Decimal%7c1%7c%7cp_PhotoCount_Int32%7c1&N=1432%20604%201430%201429%201626%201428&SearchAction=N&Qpb=1&sid=1398D8747985&No="+str(no)+"&Nne=15")

    root = lxml.html.fromstring(html)

    ads = root.cssselect(".private, .dealer")
    if ads:
        for ad in ads:
            try:

                title = ad.cssselect(".title, .premium-title")[0].text_content()
                title = re.match(r"(\d+) (\S+) (.+)", title)
                url = re.match(r"window.location='(.*)\?", ad.get('onclick')).group(1)
                category = ad.cssselect(".summary-list-item")[1].text_content()
                subcategory = ''

                if " - " in category:
                    split = category.split(' - ')
                    category = split[0]
                    subcategory = split[1]


                data = {
                        'url' : url,
                        'year' : int(float(title.group(1))),
                        'make' : title.group(2),
                        'model' : title.group(3),
                        'price' : int(float(ad.cssselect(".price")[0].text_content().translate(None, '$,*'))),

                        # note sometimes dirtbikes specify hours so code will need modification if analysis on dirt bikes
                        # is needed
                        'kms' : int(float(ad.cssselect(".summary-list-item")[0].text_content().translate(None, ',kmsKhours '))),
                        'category' : category,
                        'subcategory' : subcategory,
                        'state' : ad.cssselect(".state")[0].text_content(),
                        'date' : date.today()
                        };
                scraperwiki.sqlite.save(unique_keys=['url'], data=data)
            except Exception, e:
                print e
        no+=15
    else:
        break;

import scraperwiki
import re
import lxml.html
from datetime import date

no = 0

while(1):
    html = scraperwiki.scrape("http://www.bikesales.com.au/all-bikes/results.aspx?Ns=p_IsPoa_Int32%7c0%7c%7cp_RankSort_Int32%7c1%7c%7cp_HasPhotos_Int32%7c1%7c%7cp_Make_String%7c0%7c%7cp_Model_String%7c0%7c%7cp_YearMade_Int32%7c1%7c%7cp_PriceSort_Decimal%7c1%7c%7cp_PhotoCount_Int32%7c1&N=1432%20604%201430%201429%201626%201428&SearchAction=N&Qpb=1&sid=1398D8747985&No="+str(no)+"&Nne=15")

    root = lxml.html.fromstring(html)

    ads = root.cssselect(".private, .dealer")
    if ads:
        for ad in ads:
            try:

                title = ad.cssselect(".title, .premium-title")[0].text_content()
                title = re.match(r"(\d+) (\S+) (.+)", title)
                url = re.match(r"window.location='(.*)\?", ad.get('onclick')).group(1)
                category = ad.cssselect(".summary-list-item")[1].text_content()
                subcategory = ''

                if " - " in category:
                    split = category.split(' - ')
                    category = split[0]
                    subcategory = split[1]


                data = {
                        'url' : url,
                        'year' : int(float(title.group(1))),
                        'make' : title.group(2),
                        'model' : title.group(3),
                        'price' : int(float(ad.cssselect(".price")[0].text_content().translate(None, '$,*'))),

                        # note sometimes dirtbikes specify hours so code will need modification if analysis on dirt bikes
                        # is needed
                        'kms' : int(float(ad.cssselect(".summary-list-item")[0].text_content().translate(None, ',kmsKhours '))),
                        'category' : category,
                        'subcategory' : subcategory,
                        'state' : ad.cssselect(".state")[0].text_content(),
                        'date' : date.today()
                        };
                scraperwiki.sqlite.save(unique_keys=['url'], data=data)
            except Exception, e:
                print e
        no+=15
    else:
        break;

