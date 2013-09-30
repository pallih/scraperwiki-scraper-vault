import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=2013%20Savar%20building%20collapse&prop=revisions&rvprop=content")

root = lxml.html.fromstring(html)

true = root.cssselect("ref")[0].text
true = true.split("|")
true = "url" in true[2]

for ref in root.cssselect("ref"):
    ref = ref.text

    if type(ref) != str:
        ref = 0

    else:
        ref = ref.split("|")
        print ref

        try:
            url = ref[1]

        except:
            url = "None"
        try:
            url = url.split("=")
            url = url[1]
            print url
        except:
            url = "None"
 
        try:
            title = ref[2]

        except:
            title = "None"
        try:
            title = title.split("=")
            title = title[1]
            print title
        except:
            title = "None"

        try:
            accessdate = ref[3]

        except:
            accessdate = "None"
        try:
            accessdate = accessdate.split("=")
            accessdate = accessdate[1]
            print accessdate 
        except: 
            accessdate = "None"

        try:
            newspaper = ref[4]

        except:
            newspaper = "list index out of range"
        try:
            newspaper= url.split("=")
            newspaper= url[1]
            print newspaper
        except:
            newspaper = "None"

        try:
            publisher = ref[5]

        except:
            publisher = "list index out of range"

        publisher = publisher.split("=")
        
        
        try:
            publisher = publisher[1]
        except:
            publisher = "None"

        print publisher 

        try:
            date = ref[6]

        except:
            date = "None"
        try:
            date = date.split("=")
            date = date[1] 
            print date
        except:
            date = "no date"

        data = {"url" : url, "title" : title, "accessdate" : accessdate, "newspaper" : newspaper, "publisher" : publisher, "date" : date}
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=2013%20Savar%20building%20collapse&prop=revisions&rvprop=content")

root = lxml.html.fromstring(html)

true = root.cssselect("ref")[0].text
true = true.split("|")
true = "url" in true[2]

for ref in root.cssselect("ref"):
    ref = ref.text

    if type(ref) != str:
        ref = 0

    else:
        ref = ref.split("|")
        print ref

        try:
            url = ref[1]

        except:
            url = "None"
        try:
            url = url.split("=")
            url = url[1]
            print url
        except:
            url = "None"
 
        try:
            title = ref[2]

        except:
            title = "None"
        try:
            title = title.split("=")
            title = title[1]
            print title
        except:
            title = "None"

        try:
            accessdate = ref[3]

        except:
            accessdate = "None"
        try:
            accessdate = accessdate.split("=")
            accessdate = accessdate[1]
            print accessdate 
        except: 
            accessdate = "None"

        try:
            newspaper = ref[4]

        except:
            newspaper = "list index out of range"
        try:
            newspaper= url.split("=")
            newspaper= url[1]
            print newspaper
        except:
            newspaper = "None"

        try:
            publisher = ref[5]

        except:
            publisher = "list index out of range"

        publisher = publisher.split("=")
        
        
        try:
            publisher = publisher[1]
        except:
            publisher = "None"

        print publisher 

        try:
            date = ref[6]

        except:
            date = "None"
        try:
            date = date.split("=")
            date = date[1] 
            print date
        except:
            date = "no date"

        data = {"url" : url, "title" : title, "accessdate" : accessdate, "newspaper" : newspaper, "publisher" : publisher, "date" : date}
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)

