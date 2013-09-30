import scraperwiki
import nltk

scraperwiki.sqlite.attach("sotcc_cabinet")
cabinet_data =  scraperwiki.sqlite.select("Councillor from sotcc_cabinet.swdata")
scraperwiki.sqlite.attach("councillorquotes")
quote_data =  scraperwiki.sqlite.select("* from councillorquotes.swdata")

for quote in quote_data:
    row = {}
    quote['quote'] = quote['quote'].encode('utf8', 'replace')
    quote_mark = quote['quote'].find("&#8220;")
    quote_clean = quote['quote'][quote_mark+7:]
    quote_clean = quote_clean.replace("&#8217;", "'")
    quote_clean = quote_clean.replace("&#8221;", '')
    quote_clean = quote_clean.replace("&#8220;", '')
    quote_clean = quote_clean.replace("“", '')
    quote_clean = quote_clean.replace("&#163;90", '£')
    quote_clean = quote_clean.replace("</p>", "")
    quote_clean = quote_clean.replace("<br>", "")
    quote_clean = nltk.clean_html(quote_clean)
    
    row['subject'] = ""
    for coun in cabinet_data:
        
        if coun['Councillor'] in quote['quote']:
            row['subject'] = coun['Councillor']
    row['index'] = quote['index']
    row['quote_clean'] = quote_clean
    if row['subject']=="":
        row['subject'] = "NA"
    scraperwiki.sqlite.save(unique_keys=['index'], data=row)
        
        
    import scraperwiki
import nltk

scraperwiki.sqlite.attach("sotcc_cabinet")
cabinet_data =  scraperwiki.sqlite.select("Councillor from sotcc_cabinet.swdata")
scraperwiki.sqlite.attach("councillorquotes")
quote_data =  scraperwiki.sqlite.select("* from councillorquotes.swdata")

for quote in quote_data:
    row = {}
    quote['quote'] = quote['quote'].encode('utf8', 'replace')
    quote_mark = quote['quote'].find("&#8220;")
    quote_clean = quote['quote'][quote_mark+7:]
    quote_clean = quote_clean.replace("&#8217;", "'")
    quote_clean = quote_clean.replace("&#8221;", '')
    quote_clean = quote_clean.replace("&#8220;", '')
    quote_clean = quote_clean.replace("“", '')
    quote_clean = quote_clean.replace("&#163;90", '£')
    quote_clean = quote_clean.replace("</p>", "")
    quote_clean = quote_clean.replace("<br>", "")
    quote_clean = nltk.clean_html(quote_clean)
    
    row['subject'] = ""
    for coun in cabinet_data:
        
        if coun['Councillor'] in quote['quote']:
            row['subject'] = coun['Councillor']
    row['index'] = quote['index']
    row['quote_clean'] = quote_clean
    if row['subject']=="":
        row['subject'] = "NA"
    scraperwiki.sqlite.save(unique_keys=['index'], data=row)
        
        
    