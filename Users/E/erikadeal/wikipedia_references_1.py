#This scraper gathers the references from a Wikipedia article by querying the API, finding the <ref> tags, and putting the attributes in separate data fields to be saved in a database. This represents something of a workaround because Wikipedia footnotes are stored in templates and we could not retrieve the data directly from the API; instead, we had to search the article body text for references and their metadata.
import scraperwiki
import lxml.html

#Retrieve the API data and format as HTML
html = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=2013%20Savar%20building%20collapse&prop=revisions&rvprop=content")

#Parse the HTML page as XML
root = lxml.html.fromstring(html)

#Select the <ref> tags, which contain metadata about news references
true = root.cssselect("ref")[0].text
true = true.split("|")
true = "url" in true[2]

#Select each <ref> as text for parsing into different data fields
for ref in root.cssselect("ref"):
    ref = ref.text
    
#Exception handling for refs that are not strings (the data format tends to be erratic)
    if type(ref) != str:
        ref = 0
#Split apart the ref into components
    else:
        ref = ref.split("|")
        print ref
    #Grab the url and split off the text. Lots of exceptions for unexpected or missing data fields because the references are not formatted consistently
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
    #Do the same for the reference title
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
    #Access date for the reference
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
    #Newspaper that published the reference
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
    #Publisher
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
    #Publication date
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
    #Save the data fields in a SQLite database so that it can be downloaded and used.

        data = {"url" : url, "title" : title, "accessdate" : accessdate, "newspaper" : newspaper, "publisher" : publisher, "date" : date}
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)

