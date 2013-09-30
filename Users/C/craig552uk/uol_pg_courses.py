import scraperwiki, lxml.html, re

html = scraperwiki.scrape("http://www2.le.ac.uk/study/postgrad/new-prospectus")
root = lxml.html.fromstring(html)

for link in root.cssselect("#content a"):
    dept = {}
    dept['url']  = link.attrib["href"]
    dept['name'] = link.text_content()
    print dept['name']

    dept_html = scraperwiki.scrape(dept['url'])
    dept_root = lxml.html.fromstring(dept_html)
    
    for course_link in dept_root.cssselect("#content a"):
        # Ignore links outside the prospectus
        if "new-prospectus" in course_link.attrib["href"]:
            course = {}
            course["url"] = course_link.attrib["href"]

            # Follow course links
            course_html = scraperwiki.scrape("http://www2.le.ac.uk" + course['url'])
            course_root = lxml.html.fromstring(course_html)

            course["title"]           = course_root.cssselect("#content h1")[0].text_content().strip()
            course["director"]        = course_root.cssselect("#content li")[0].cssselect("em")[0].text_content().strip()
            course["department"]      = dept['name']
            course["fees"]            = {}
            course["fees"]["2012_13"] = {}
            course["fees"]["2012_13"]["home_eu"]       = re.sub(r"/[^0-9]/", "", course_root.cssselect("#content table")[0].cssselect("li")[0].text_content().strip().split(":")[1])
            course["fees"]["2012_13"]["international"] = course_root.cssselect("#content table")[0].cssselect("li")[1].text_content().strip().split(":")[1]
            course["fees"]["2013_14"] = {}
            course["fees"]["2013_14"]["home_eu"]       = course_root.cssselect("#content table")[0].cssselect("li")[2].text_content().strip().split(":")[1]
            course["fees"]["2013_14"]["international"] = course_root.cssselect("#content table")[0].cssselect("li")[3].text_content().strip().split(":")[1]

            print "- %s" % courseimport scraperwiki, lxml.html, re

html = scraperwiki.scrape("http://www2.le.ac.uk/study/postgrad/new-prospectus")
root = lxml.html.fromstring(html)

for link in root.cssselect("#content a"):
    dept = {}
    dept['url']  = link.attrib["href"]
    dept['name'] = link.text_content()
    print dept['name']

    dept_html = scraperwiki.scrape(dept['url'])
    dept_root = lxml.html.fromstring(dept_html)
    
    for course_link in dept_root.cssselect("#content a"):
        # Ignore links outside the prospectus
        if "new-prospectus" in course_link.attrib["href"]:
            course = {}
            course["url"] = course_link.attrib["href"]

            # Follow course links
            course_html = scraperwiki.scrape("http://www2.le.ac.uk" + course['url'])
            course_root = lxml.html.fromstring(course_html)

            course["title"]           = course_root.cssselect("#content h1")[0].text_content().strip()
            course["director"]        = course_root.cssselect("#content li")[0].cssselect("em")[0].text_content().strip()
            course["department"]      = dept['name']
            course["fees"]            = {}
            course["fees"]["2012_13"] = {}
            course["fees"]["2012_13"]["home_eu"]       = re.sub(r"/[^0-9]/", "", course_root.cssselect("#content table")[0].cssselect("li")[0].text_content().strip().split(":")[1])
            course["fees"]["2012_13"]["international"] = course_root.cssselect("#content table")[0].cssselect("li")[1].text_content().strip().split(":")[1]
            course["fees"]["2013_14"] = {}
            course["fees"]["2013_14"]["home_eu"]       = course_root.cssselect("#content table")[0].cssselect("li")[2].text_content().strip().split(":")[1]
            course["fees"]["2013_14"]["international"] = course_root.cssselect("#content table")[0].cssselect("li")[3].text_content().strip().split(":")[1]

            print "- %s" % course