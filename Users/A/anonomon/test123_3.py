import scraperwiki
import lxml.html    
import time       

for a in range(1, 465):
    link = "http://www.posharp.com/photovoltaic/database.aspx?pg=" + str(a)
    html = scraperwiki.scrape(link)
    time.sleep(10)
    
    print "Hello, Starting..."
    runonce = 'false'
    
    root = lxml.html.fromstring(html)
    for table in root.cssselect("table.igoogle"):           
        for trs in table.cssselect("tr"):
            if runonce == 'false':
                runonce = 'true'
                continue

            try:
                company = trs[0].cssselect("a")[0].text
            except:
                company = trs[0].text

            try:
                company_url = trs[0].cssselect("a")[0].attrib['href']
            except:
                company_url = ''

            try:
                panel = trs[1].cssselect("a")[0].text
            except:
                panel = trs[1].text

            try:
                panel_url = trs[1].cssselect("a")[0].attrib['href']
            except:
                panel_url = ''

            data = {
                'company' : company,
                'company_url' : company_url,
                'panel' : panel,
                'panel_url' : panel_url,
                'power' : trs[2].text,
                'eff' : trs[3].text,
                'Voc' : trs[4].text,
                'Isc' : trs[5].text,
                'Vmp' : trs[6].text,
                'Imp' : trs[7].text,
            }
            scraperwiki.sqlite.save(unique_keys=['panel'], data=data)
            import scraperwiki
import lxml.html    
import time       

for a in range(1, 465):
    link = "http://www.posharp.com/photovoltaic/database.aspx?pg=" + str(a)
    html = scraperwiki.scrape(link)
    time.sleep(10)
    
    print "Hello, Starting..."
    runonce = 'false'
    
    root = lxml.html.fromstring(html)
    for table in root.cssselect("table.igoogle"):           
        for trs in table.cssselect("tr"):
            if runonce == 'false':
                runonce = 'true'
                continue

            try:
                company = trs[0].cssselect("a")[0].text
            except:
                company = trs[0].text

            try:
                company_url = trs[0].cssselect("a")[0].attrib['href']
            except:
                company_url = ''

            try:
                panel = trs[1].cssselect("a")[0].text
            except:
                panel = trs[1].text

            try:
                panel_url = trs[1].cssselect("a")[0].attrib['href']
            except:
                panel_url = ''

            data = {
                'company' : company,
                'company_url' : company_url,
                'panel' : panel,
                'panel_url' : panel_url,
                'power' : trs[2].text,
                'eff' : trs[3].text,
                'Voc' : trs[4].text,
                'Isc' : trs[5].text,
                'Vmp' : trs[6].text,
                'Imp' : trs[7].text,
            }
            scraperwiki.sqlite.save(unique_keys=['panel'], data=data)
            