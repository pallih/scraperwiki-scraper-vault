import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.etymonline.com/index.php?search=arabic&searchmode=&p=9&allowed_in_frame=0")
## print html


root = lxml.html.fromstring(html)
for word in root.cssselect("dl dt"):
    ## print "###################"
    ## print word[0].text
    defn = ""
    defs = word.cssselect("+dd")
    for part in defs[0].itertext():
        ## print part
        defn += part
    ## print defs[0].text
    data1 = {
        'word' : word[0].text,
        'def' : defn
    }
    scraperwiki.sqlite.save(unique_keys=["word"], data=data1)



import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.etymonline.com/index.php?search=arabic&searchmode=&p=9&allowed_in_frame=0")
## print html


root = lxml.html.fromstring(html)
for word in root.cssselect("dl dt"):
    ## print "###################"
    ## print word[0].text
    defn = ""
    defs = word.cssselect("+dd")
    for part in defs[0].itertext():
        ## print part
        defn += part
    ## print defs[0].text
    data1 = {
        'word' : word[0].text,
        'def' : defn
    }
    scraperwiki.sqlite.save(unique_keys=["word"], data=data1)



