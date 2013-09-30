# Parse the ESTYN database getting list of schools

import lxml.html
import urlparse
import re
import scraperwiki


for i in range(259, 270):

    url = "http://www.estyn.gov.uk/english/inspection/inspection-reports/?offset=%s&submitted=1&searchTitle=&searchType=All&searchPostcode=&localAuthority=All&searchDistance=10" % i
    
    root=lxml.html.parse(url).getroot()
    nodes=root.cssselect('#provider_search_results ul h2')
    
    #print nodes
    for node in nodes:
        #print lxml.html.tostring(node)
        #print lxml.html.tostring(node.getnext())
        #print node[0].text
        #print urlparse.urljoin(url,node[0].attrib.get('href'))
        p = node.getnext()
        txt = ""
        if p.text!=None:
            txt = p.text
        addr = [txt]
        for br in p:
            assert br.tag == "br"
            if br.tail:
                addr.append(br.tail)
        #print addr
    
        data = {"url":urlparse.urljoin(url,node[0].attrib.get('href')),"name":node[0].text}
    
        # For each school page, extract the PDF link.
        if data["url"]:
            schoolroot = lxml.html.parse(data["url"]).getroot()
            if schoolroot:
                link = schoolroot.cssselect('.pdf')
                if link:
                    data["report"] = urlparse.urljoin(url,link[0].attrib.get('href'))
        else:
            print "Can't find a URL for "+data["name"]

        postcode = ""
        postcode = addr[-1]
        if postcode:
            latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
            if latlng:
                data["lat"] = latlng[0]
                data["long"] = latlng[1]
                data["postcode"] = postcode
    
            # if re.match("[A-Z]{1,2}\d{1,2} +\d{1}[A-Z]{2}$",postcode):
            
    
        data["address"] = ", ".join(addr)
        if re.search("provider/[A-Za-z0-9]+/$",data["url"]):
            data['id'] = re.search("provider/([A-Za-z0-9]+)/$",data["url"]).group(1)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        else:
            print "Can't find a unique ID for "+data["name"]
        print data
    

#"http://www.estyn.gov.uk/download/publication/12694.5/inspection-reportabercerdin-primary-schooleng2008/"
# Parse the ESTYN database getting list of schools

import lxml.html
import urlparse
import re
import scraperwiki


for i in range(259, 270):

    url = "http://www.estyn.gov.uk/english/inspection/inspection-reports/?offset=%s&submitted=1&searchTitle=&searchType=All&searchPostcode=&localAuthority=All&searchDistance=10" % i
    
    root=lxml.html.parse(url).getroot()
    nodes=root.cssselect('#provider_search_results ul h2')
    
    #print nodes
    for node in nodes:
        #print lxml.html.tostring(node)
        #print lxml.html.tostring(node.getnext())
        #print node[0].text
        #print urlparse.urljoin(url,node[0].attrib.get('href'))
        p = node.getnext()
        txt = ""
        if p.text!=None:
            txt = p.text
        addr = [txt]
        for br in p:
            assert br.tag == "br"
            if br.tail:
                addr.append(br.tail)
        #print addr
    
        data = {"url":urlparse.urljoin(url,node[0].attrib.get('href')),"name":node[0].text}
    
        # For each school page, extract the PDF link.
        if data["url"]:
            schoolroot = lxml.html.parse(data["url"]).getroot()
            if schoolroot:
                link = schoolroot.cssselect('.pdf')
                if link:
                    data["report"] = urlparse.urljoin(url,link[0].attrib.get('href'))
        else:
            print "Can't find a URL for "+data["name"]

        postcode = ""
        postcode = addr[-1]
        if postcode:
            latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
            if latlng:
                data["lat"] = latlng[0]
                data["long"] = latlng[1]
                data["postcode"] = postcode
    
            # if re.match("[A-Z]{1,2}\d{1,2} +\d{1}[A-Z]{2}$",postcode):
            
    
        data["address"] = ", ".join(addr)
        if re.search("provider/[A-Za-z0-9]+/$",data["url"]):
            data['id'] = re.search("provider/([A-Za-z0-9]+)/$",data["url"]).group(1)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        else:
            print "Can't find a unique ID for "+data["name"]
        print data
    

#"http://www.estyn.gov.uk/download/publication/12694.5/inspection-reportabercerdin-primary-schooleng2008/"
