import scraperwiki
import lxml.html  

#function rstrip() and lstrip() for striping all kinds of whitespace by default        

urls = ['http://data-gov.tw.rpi.edu/demo/stable/demo-1356-1623-health-claim-vs-income.html', 'http://data-gov.tw.rpi.edu/demo/stable/budget/show_details.php', 'http://data-gov.tw.rpi.edu/demo/stable/budget/show_summary.php', 'http://data-gov.tw.rpi.edu/demo/stable/demo-353-library.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1187-40x-wildfire-budget.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1322-1464-stimulus-and-public-housing.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1580-bankruptcy.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-10040-broadband-home.html']

for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    content = {}
    data = []
    i = 0
    titre = root.cssselect("title")
    for tr in root.cssselect("table[class='pretty']  tr"):
        tds = tr.cssselect("td")
       
        desc = (tds[0].text_content()).rstrip('\n\t\n\t').lstrip('\n\t')
        contenu = (tds[1].text_content()).rstrip('\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t').lstrip('\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t')   
        if len(desc) > 1:
                if (contenu  !='\n\t') :
                    i = i + 1
                    data1 ={
                       desc : contenu.lstrip('\t\t\n\t\t\t\n\t\t\t\n\n\t\t'),
                   
                       }
        data.append(data1)

    print data[0]
    #if (desc == data[4]['SPARQL queries']) :
            #queries = desc
            
    #if (desc == data[4]['SPARQL queries']):
            #queries = desc
       
      
    
    for i in range(0,len(data)):
        content ={
                'title': titre[0].text_content(),
                'description' : data[0]['description'],
                'creator': data[1]['creator'],
                'created': data[2]['created'],
                'datasets': data[3]['datasets'],
                'enpoint': data[5]['SPARQL endpoint'],
                'href': url
                }

    scraperwiki.sqlite.save(unique_keys=['href'], data=content)
    # TODO: see how to write the output in a file directly

import scraperwiki
import lxml.html  

#function rstrip() and lstrip() for striping all kinds of whitespace by default        

urls = ['http://data-gov.tw.rpi.edu/demo/stable/demo-1356-1623-health-claim-vs-income.html', 'http://data-gov.tw.rpi.edu/demo/stable/budget/show_details.php', 'http://data-gov.tw.rpi.edu/demo/stable/budget/show_summary.php', 'http://data-gov.tw.rpi.edu/demo/stable/demo-353-library.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1187-40x-wildfire-budget.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1322-1464-stimulus-and-public-housing.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-1580-bankruptcy.html', 'http://data-gov.tw.rpi.edu/demo/stable/demo-10040-broadband-home.html']

for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    content = {}
    data = []
    i = 0
    titre = root.cssselect("title")
    for tr in root.cssselect("table[class='pretty']  tr"):
        tds = tr.cssselect("td")
       
        desc = (tds[0].text_content()).rstrip('\n\t\n\t').lstrip('\n\t')
        contenu = (tds[1].text_content()).rstrip('\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t').lstrip('\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t\n\t')   
        if len(desc) > 1:
                if (contenu  !='\n\t') :
                    i = i + 1
                    data1 ={
                       desc : contenu.lstrip('\t\t\n\t\t\t\n\t\t\t\n\n\t\t'),
                   
                       }
        data.append(data1)

    print data[0]
    #if (desc == data[4]['SPARQL queries']) :
            #queries = desc
            
    #if (desc == data[4]['SPARQL queries']):
            #queries = desc
       
      
    
    for i in range(0,len(data)):
        content ={
                'title': titre[0].text_content(),
                'description' : data[0]['description'],
                'creator': data[1]['creator'],
                'created': data[2]['created'],
                'datasets': data[3]['datasets'],
                'enpoint': data[5]['SPARQL endpoint'],
                'href': url
                }

    scraperwiki.sqlite.save(unique_keys=['href'], data=content)
    # TODO: see how to write the output in a file directly

