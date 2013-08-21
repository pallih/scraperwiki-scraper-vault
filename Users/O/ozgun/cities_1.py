# Blank Python
sourcescraper = 'cities'

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''* from cities.swdata 
    '''
)

for d in data:
        print "&lt;City&gt;" 
        print "&lt;Slug&gt;"+d["Slug"]+"&lt;/Slug&gt;" 
        print "&lt;Name&gt;"+d["Name"]+"&lt;/Name&gt;" 
        print "&lt;Code&gt;"+d["Code"]+"&lt;/Code&gt;" 
        print "&lt;Country&gt;"+d["Country"]+"&lt;/Country&gt;" 
        print "&lt;/City&gt;"