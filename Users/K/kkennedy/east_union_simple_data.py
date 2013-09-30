import scraperwiki

# Blank Python

schoolcodes = ['308']
years = ["2010-2011","2009-2010"]


import scraperwiki           
html = scraperwiki.scrape("http://www.ncreportcard.org/src/schDetails.jsp?Page=4&pSchCode=308&pLEACode=900&pYear=2010-2011")
print html

import lxml.html 
import lxml.etree           
root = lxml.html.fromstring(html)
tbl = root.xpath("/html//table")
for t in tbl:
    if t.get("summary") is not None and t.get("summary").startswith("The total number of classroom teachers"):
        tds = t.cssselect("td")
        print tds
        data = {
                'classroom_teachers' : tds[1].text_content(),
                #'classroom_teachers' : int(tds[1].text_content()),
                'district_avg_ct' : int(tds[2].text_content()),
                'state_avg_ct': int(tds[3].text_content())
        }
        #for tr in tds:
        #    data = {
        #        'classroom_teachers' : tds[1].text_content(),
        #        #'classroom_teachers' : int(tds[1].text_content()),
        #        'district_avg' : int(tds[2].text_content()),
        #        'state_avg': int(tds[3].text_content())
        #    }
            #print tr.text_content()
        #print data

        #print lxml.etree.tostring(t)
    if t.get("summary") is not None and t.get("summary").startswith("The number of school staff, including teachers"):
        tds = t.cssselect("td")
        scratch = [ tr.text_content() for tr in tds ]
        #print scratch
        data['nat_board_teachers'] = tds[1].text_content()
        data['district_avg_nb'] = tds[1].text_content()
        data['state_avg_nb'] = tds[1].text_content()
        #print lxml.etree.tostring(t)

print dataimport scraperwiki

# Blank Python

schoolcodes = ['308']
years = ["2010-2011","2009-2010"]


import scraperwiki           
html = scraperwiki.scrape("http://www.ncreportcard.org/src/schDetails.jsp?Page=4&pSchCode=308&pLEACode=900&pYear=2010-2011")
print html

import lxml.html 
import lxml.etree           
root = lxml.html.fromstring(html)
tbl = root.xpath("/html//table")
for t in tbl:
    if t.get("summary") is not None and t.get("summary").startswith("The total number of classroom teachers"):
        tds = t.cssselect("td")
        print tds
        data = {
                'classroom_teachers' : tds[1].text_content(),
                #'classroom_teachers' : int(tds[1].text_content()),
                'district_avg_ct' : int(tds[2].text_content()),
                'state_avg_ct': int(tds[3].text_content())
        }
        #for tr in tds:
        #    data = {
        #        'classroom_teachers' : tds[1].text_content(),
        #        #'classroom_teachers' : int(tds[1].text_content()),
        #        'district_avg' : int(tds[2].text_content()),
        #        'state_avg': int(tds[3].text_content())
        #    }
            #print tr.text_content()
        #print data

        #print lxml.etree.tostring(t)
    if t.get("summary") is not None and t.get("summary").startswith("The number of school staff, including teachers"):
        tds = t.cssselect("td")
        scratch = [ tr.text_content() for tr in tds ]
        #print scratch
        data['nat_board_teachers'] = tds[1].text_content()
        data['district_avg_nb'] = tds[1].text_content()
        data['state_avg_nb'] = tds[1].text_content()
        #print lxml.etree.tostring(t)

print data