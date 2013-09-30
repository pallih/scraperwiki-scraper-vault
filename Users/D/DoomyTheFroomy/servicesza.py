import scraperwiki
import simplejson
import urllib2
import lxml.html

# def detail
def getDetails(detail, detail_url, category):
    print "Detail function" 
    data = {}
    data["id"] = detail_url 
    data["category"] = category
    if (len(detail.cssselect("a#Top")) > 0) and (detail.cssselect("a#Top")[0].text is not None): 
        data["service_name"] = detail.cssselect("a#Top")[0].text
        print data["service_name"]
        for content in detail.cssselect("div.content"):
            #print lxml.html.tostring(content)
            if len(content.cssselect("a.content")) > 0:
                contentype = content.cssselect("a.content")[0].attrib['id']
                print contentype
                if contentype == "Cost":
                    data['costs'] = ""
                    for idx,costs in enumerate(content.cssselect("p")):
                        #print idx
                        if idx > 0:
                            #print costs.text
                            if (costs.text is not None) and (len(costs.text) > 0):
                                data['costs'] += costs.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                            elif costs.tail is not None:
                                data['costs'] += costs.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                elif contentype == "Process":
                    if len(content.cssselect("li")) > 0:
                        for idx,step in enumerate(content.cssselect("li")):
                            if step.text is not None: 
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                                data['process'+str(idx+1)] = proc_step
                    else:
                        for idx,step in enumerate(content): 
                            if step.tail is not None: 
                                proc_step = step.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                            elif step.text is not None:
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                elif contentype == "Description":
                    data['desc'] = ""
                    for header in content.cssselect("b"): 
                        if header.text is not None:
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    for header in content.cssselect('span'):
                        if header.text is not None: 
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    data['name'] = data['desc'].replace('About', '').lstrip().rstrip()
                elif contentype == "Forms":
                    print content.text                             
        print data
        scraperwiki.sqlite.save(["id"], data)


def getDetailContent(url,base_url):
    try: 
        html = scraperwiki.scrape(url)
        content =  lxml.html.fromstring(html)
        if len(content.cssselect("div.service-item")) > 0 :
            for el in content.cssselect("div#services-inside a"):
                further_url = base_url + el.attrib['href']
                detail_url = getDetailContent(further_url,base_url)
                if detail_url is not None:
                    detail_html = scraperwiki.scrape(detail_url)
                    detail =  lxml.html.fromstring(detail_html)
                    getDetails(detail, detail_url, category)
    
        else:
            #print url
            return url
    except: 
        print 'Oh dear, failed to scrape %s' % url


not_given = "keine Angabe"
base_url = 'http://www.services.gov.za'
home_url = base_url + '/services/content/Home/'
categories = ["ServicesForPeople", "OrganisationServices", "ServicesforForeignNationals"]
for category in categories:
    start_url = home_url + category
    detail_url = getDetailContent(start_url,base_url)
    print detail_url
    if detail_url is not None:
        detail_html = scraperwiki.scrape(detail_url)
        detail =  lxml.html.fromstring(detail_html)
        getDetails(detail, detail_url, category)import scraperwiki
import simplejson
import urllib2
import lxml.html

# def detail
def getDetails(detail, detail_url, category):
    print "Detail function" 
    data = {}
    data["id"] = detail_url 
    data["category"] = category
    if (len(detail.cssselect("a#Top")) > 0) and (detail.cssselect("a#Top")[0].text is not None): 
        data["service_name"] = detail.cssselect("a#Top")[0].text
        print data["service_name"]
        for content in detail.cssselect("div.content"):
            #print lxml.html.tostring(content)
            if len(content.cssselect("a.content")) > 0:
                contentype = content.cssselect("a.content")[0].attrib['id']
                print contentype
                if contentype == "Cost":
                    data['costs'] = ""
                    for idx,costs in enumerate(content.cssselect("p")):
                        #print idx
                        if idx > 0:
                            #print costs.text
                            if (costs.text is not None) and (len(costs.text) > 0):
                                data['costs'] += costs.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                            elif costs.tail is not None:
                                data['costs'] += costs.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                elif contentype == "Process":
                    if len(content.cssselect("li")) > 0:
                        for idx,step in enumerate(content.cssselect("li")):
                            if step.text is not None: 
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                                data['process'+str(idx+1)] = proc_step
                    else:
                        for idx,step in enumerate(content): 
                            if step.tail is not None: 
                                proc_step = step.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                            elif step.text is not None:
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                elif contentype == "Description":
                    data['desc'] = ""
                    for header in content.cssselect("b"): 
                        if header.text is not None:
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    for header in content.cssselect('span'):
                        if header.text is not None: 
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    data['name'] = data['desc'].replace('About', '').lstrip().rstrip()
                elif contentype == "Forms":
                    print content.text                             
        print data
        scraperwiki.sqlite.save(["id"], data)


def getDetailContent(url,base_url):
    try: 
        html = scraperwiki.scrape(url)
        content =  lxml.html.fromstring(html)
        if len(content.cssselect("div.service-item")) > 0 :
            for el in content.cssselect("div#services-inside a"):
                further_url = base_url + el.attrib['href']
                detail_url = getDetailContent(further_url,base_url)
                if detail_url is not None:
                    detail_html = scraperwiki.scrape(detail_url)
                    detail =  lxml.html.fromstring(detail_html)
                    getDetails(detail, detail_url, category)
    
        else:
            #print url
            return url
    except: 
        print 'Oh dear, failed to scrape %s' % url


not_given = "keine Angabe"
base_url = 'http://www.services.gov.za'
home_url = base_url + '/services/content/Home/'
categories = ["ServicesForPeople", "OrganisationServices", "ServicesforForeignNationals"]
for category in categories:
    start_url = home_url + category
    detail_url = getDetailContent(start_url,base_url)
    print detail_url
    if detail_url is not None:
        detail_html = scraperwiki.scrape(detail_url)
        detail =  lxml.html.fromstring(detail_html)
        getDetails(detail, detail_url, category)import scraperwiki
import simplejson
import urllib2
import lxml.html

# def detail
def getDetails(detail, detail_url, category):
    print "Detail function" 
    data = {}
    data["id"] = detail_url 
    data["category"] = category
    if (len(detail.cssselect("a#Top")) > 0) and (detail.cssselect("a#Top")[0].text is not None): 
        data["service_name"] = detail.cssselect("a#Top")[0].text
        print data["service_name"]
        for content in detail.cssselect("div.content"):
            #print lxml.html.tostring(content)
            if len(content.cssselect("a.content")) > 0:
                contentype = content.cssselect("a.content")[0].attrib['id']
                print contentype
                if contentype == "Cost":
                    data['costs'] = ""
                    for idx,costs in enumerate(content.cssselect("p")):
                        #print idx
                        if idx > 0:
                            #print costs.text
                            if (costs.text is not None) and (len(costs.text) > 0):
                                data['costs'] += costs.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                            elif costs.tail is not None:
                                data['costs'] += costs.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                elif contentype == "Process":
                    if len(content.cssselect("li")) > 0:
                        for idx,step in enumerate(content.cssselect("li")):
                            if step.text is not None: 
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()
                                data['process'+str(idx+1)] = proc_step
                    else:
                        for idx,step in enumerate(content): 
                            if step.tail is not None: 
                                proc_step = step.tail.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                            elif step.text is not None:
                                proc_step = step.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                                data['process'+str(idx+1)] = proc_step
                elif contentype == "Description":
                    data['desc'] = ""
                    for header in content.cssselect("b"): 
                        if header.text is not None:
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    for header in content.cssselect('span'):
                        if header.text is not None: 
                            data['desc'] += " " + header.text.lstrip('\r\n\t').rstrip('\r\n\t').lstrip().rstrip()  
                    data['name'] = data['desc'].replace('About', '').lstrip().rstrip()
                elif contentype == "Forms":
                    print content.text                             
        print data
        scraperwiki.sqlite.save(["id"], data)


def getDetailContent(url,base_url):
    try: 
        html = scraperwiki.scrape(url)
        content =  lxml.html.fromstring(html)
        if len(content.cssselect("div.service-item")) > 0 :
            for el in content.cssselect("div#services-inside a"):
                further_url = base_url + el.attrib['href']
                detail_url = getDetailContent(further_url,base_url)
                if detail_url is not None:
                    detail_html = scraperwiki.scrape(detail_url)
                    detail =  lxml.html.fromstring(detail_html)
                    getDetails(detail, detail_url, category)
    
        else:
            #print url
            return url
    except: 
        print 'Oh dear, failed to scrape %s' % url


not_given = "keine Angabe"
base_url = 'http://www.services.gov.za'
home_url = base_url + '/services/content/Home/'
categories = ["ServicesForPeople", "OrganisationServices", "ServicesforForeignNationals"]
for category in categories:
    start_url = home_url + category
    detail_url = getDetailContent(start_url,base_url)
    print detail_url
    if detail_url is not None:
        detail_html = scraperwiki.scrape(detail_url)
        detail =  lxml.html.fromstring(detail_html)
        getDetails(detail, detail_url, category)