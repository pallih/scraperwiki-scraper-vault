import scraperwiki
import lxml.html 

#letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

letters = ['a']

for letter in letters:
    html = scraperwiki.scrape("http://www.ncbi.nlm.nih.gov/pubmedhealth/s/diseases_and_conditions/" + letter + "/");
    root = lxml.html.fromstring(html)
    for a in root.cssselect(".resultList a"):
        data = {
            'url' : a.attrib['href'],
            'disease' : a.text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
        print data

