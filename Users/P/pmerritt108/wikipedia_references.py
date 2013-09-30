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

        length = len(ref)

        for i in range(0, length):

            #url = "url" in ref[i]
            if "url" in ref[i]:
                url = ref[i]
                print url
            else:
                url = "none"

            #title = "title" in ref[i]
            if "title" in ref[i]:
                title = ref[i]
                print title
            else:
                title = "none"

            #accessdate = "accessdate" in ref[i]
            if "accessdate" in ref[i] == true:
                accessdate = ref[i]
                print accessdate
            else:
                accessdate = "none"


            #newspaper = "newspaper" in ref[i]
            if "newspaper" in ref[i] == true:
                newspaper = ref[i]
                print newspaper
            else:
                newspaper = "none"

            publisher = "publisher" in ref[i]
            if publisher == true:
                publisher = ref[i]
                print publisher
            else:
                publisher = "none"
            
            date = "date" in ref[i]
            if date == true:
                date = ref[i]
                print date
            else:
                date = "none"

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

        length = len(ref)

        for i in range(0, length):

            #url = "url" in ref[i]
            if "url" in ref[i]:
                url = ref[i]
                print url
            else:
                url = "none"

            #title = "title" in ref[i]
            if "title" in ref[i]:
                title = ref[i]
                print title
            else:
                title = "none"

            #accessdate = "accessdate" in ref[i]
            if "accessdate" in ref[i] == true:
                accessdate = ref[i]
                print accessdate
            else:
                accessdate = "none"


            #newspaper = "newspaper" in ref[i]
            if "newspaper" in ref[i] == true:
                newspaper = ref[i]
                print newspaper
            else:
                newspaper = "none"

            publisher = "publisher" in ref[i]
            if publisher == true:
                publisher = ref[i]
                print publisher
            else:
                publisher = "none"
            
            date = "date" in ref[i]
            if date == true:
                date = ref[i]
                print date
            else:
                date = "none"

        data = {"url" : url, "title" : title, "accessdate" : accessdate, "newspaper" : newspaper, "publisher" : publisher, "date" : date}
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)     
