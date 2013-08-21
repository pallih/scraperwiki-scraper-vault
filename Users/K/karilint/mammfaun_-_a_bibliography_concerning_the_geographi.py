###############################################################################
# MAMMFAUN - A Bibliography Concerning the Geographical Distribution of Mammals
# http://people.wku.edu/charles.smith/mamm/MAMMFAUN.htm
###############################################################################

# -----------------------------------------------------------------------------
# Scraped by: Kari Lintulaakso
# Date:17.09.2012
# 
# This is another test scraper I made. This time a Bibliography Concerning the Geographical Distribution of Mammals
# -----------------------------------------------------------------------------


import scraperwiki
import lxml.html
url = "http://people.wku.edu/charles.smith/mamm/MAMMFAUN.htm"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("CREATE TABLE if not exists reference (Ref INTEGER, Authors text, Year text, Title text PRIMARY KEY, Source text);")

blockquotes = root.cssselect('blockquote') # get all the <blockquote> tags
brs = blockquotes[3].cssselect('br')       # get all the <br> tags from the fourth blockquote
ref_id = 0                                 # This id is going to be used for linking the reference and its keywords, not implemented yet

for br in brs:
#    print lxml.html.tostring(brs[i]) # the full HTML tag
#    print brs[i].tail # just the text inside the HTML tag
    raws = str(br.tail).split('--')
    row = 1
    for raw in raws:
        if raw != "None" and row ==1:
            ref_id = ref_id+1
            authors = ''
            years = ''
            title = ''
            source = ''
#http://stackoverflow.com/questions/1546226/the-shortest-way-to-remove-multiple-spaces-in-a-string-in-python
            curString = " ".join(raw.replace('\r\n','').split())

#            print str(row) + curString
            details = curString .split(', 1',1)    
            millenium = 1
#            print str(row)+str(raw)+curString+details[0]+str(len(details))
            if len(details) == 1:
                details = curString .split(', 2',1)    
                millenium = 2
            if len(details) > 1:
#                print details[0]
                authors = details[0]
                temp = details[1].split('.', 1 )
                years = (str(millenium) + temp[0]).strip()
                title = temp[1].strip()
                source = curString
#                print authors +"|"+years+"|"+title
            row = row+1
            # Set up our data record - we'll need it later
            record = {}
            record['Ref'] = ref_id
            record['Authors'] = authors.strip()
            record['Year'] = years.strip()
            record['Title'] = title.strip()
            record['Source'] = source.strip()

    # Print out the data we've gathered
            print record, '------------'
    # Finally, save the record to the datastore - 'Title' is our unique key
#            scraperwiki.sqlite.save(['Title'], record, "reference")
            scraperwiki.sqlite.save(['Title'], record, "reference")

