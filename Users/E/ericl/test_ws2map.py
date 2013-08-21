import scraperwiki

html = scraperwiki.scrape("http://dbpedia.org/sparql/?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=SELECT+%3Fsubject+%3Flat+%3Flong++%3FisPrimaryTopicOf+%3Fthumbnail+WHERE+{%09%0D%0A%3Fsubject+foaf%3AisPrimaryTopicOf+%3FisPrimaryTopicOf.%0D%0A%3Fsubject+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2Fsubject%3E+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2FCategory%3ABuildings_and_structures_in_Alpes-de-Haute-Provence%3E.%0D%0A%3Fsubject+dbpedia-owl%3Athumbnail+%3Fthumbnail.%0D%0A%3Fsubject+geo%3Alat+%3Flat.%0D%0A%3Fsubject+geo%3Along+%3Flong.%0D%0A}+&format=text%2Fhtml&timeout=0&debug=on")

import lxml.html 
root = lxml.html.fromstring(html) 

for tr in root.cssselect("tr"): 
    tds = tr.cssselect("td")
    if len(tds)==5: ## nb de colonnes du tableau
        lat = tds[1].text_content()
        lng = tds[2].text_content()
        url = tds[0].text_content()
        picture = tds[4].text_content()
        link = url[7:]
        title =  url[28:]
        data = {
            's' : "Buildings_and_structures_in_Alpes-de-Haute-Provence",
            'a' : float(lat),
            'o' : float(lng),
#            'l' : link,
            't' : title,
            'p' : picture
        }
        scraperwiki.sqlite.save(unique_keys=['t'], data=data)
#        print data

