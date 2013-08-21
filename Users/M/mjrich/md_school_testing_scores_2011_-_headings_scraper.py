import urllib2
import scraperwiki as sw
import lxml.html as html
import re
from scraperwiki.sqlite import save
from geopy import geocoders

variables = [
    'name','principal','address','phone',
    'cluster', 'supt', 'hours', 'website', 
    'fax', 'receiving_schools', 'feeder_schools'
]

def paginating(url):
    pages = range(13, 276, 2)
    pdf_data = urllib2.urlopen(url).read()
    xml_data = sw.pdftoxml(pdf_data)
    html_data = html.fromstring(xml_data)
    for page in pages:
        page_data = html_data.cssselect('page')[page]
        
        print html.tostring(page_data)
        
        parse_pdf_header(page_data)




def parse_pdf_header(page_data):
    sc_data_agg = []
    nums = range(5, 16)
    for num in nums:
        sc_data = page_data.cssselect('text')[num].text_content()
        match = re.search(r':', sc_data)
        if match:
            sc_data = sc_data.split(':', 1)[1].strip()
        sc_data_agg += [sc_data]
        
    data = dict(zip(variables, sc_data_agg))
    
    if data['address'] != '':
        us = geocoders.GeocoderDotUS() 
        place, (lat, lng) = us.geocode(data['address'])  
        print "%s: %.5f, %.5f" % (place, lat, lng) 
    
        data['lat'] = lat
        data['lng'] = lng
    

    save([], data)


    print data

paginating('http://www.montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/currentyear/SAAG2012.pdf')

#Note: This 500 page PDF breaks after the 5th elementary school.  Needs to be revisited based on DOM varation within the above PDF.
