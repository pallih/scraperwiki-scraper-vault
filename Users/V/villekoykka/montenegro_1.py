import scraperwiki   
import json       
scraperwiki.sqlite.attach("montenegro")

data = scraperwiki.sqlite.select(           
    '''* from montenegro.data'''
)

for detail in data:

    print "<table>"
    
    d = scraperwiki.sqlite.select(           
        '''* from montenegro.data'''
    )
          
    print "<tr>"
    print "<td>"
    print detail['href']
    print "</td>"
    print "<td>"
    print detail['sku']
    
    print "</td>"

    print "</tr>"
    print "</table>"import scraperwiki   
import json       
scraperwiki.sqlite.attach("montenegro")

data = scraperwiki.sqlite.select(           
    '''* from montenegro.data'''
)

for detail in data:

    print "<table>"
    
    d = scraperwiki.sqlite.select(           
        '''* from montenegro.data'''
    )
          
    print "<tr>"
    print "<td>"
    print detail['href']
    print "</td>"
    print "<td>"
    print detail['sku']
    
    print "</td>"

    print "</tr>"
    print "</table>"