##################################################################
# Press Complaints Commission decisions: cases from their database
# http://www.pcc.org.uk/advanced_search.html
# Sorts cases by publication, outcome, and PCC code clause
# Adapted from an original version by Tom Lynn
##################################################################
# To do: fix up so doesn't fail if page=None (ie if scraperwiki breaks)

import scraperwiki
import BeautifulSoup
import base64
import lxml.etree
import re
from pprint import pprint

# Tom L's helper function to clean up the text
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    # An internal "helper for the helper" function: only keep <br> tags
    def replace_tag(match):
        tag = match.group()
        tagname = tag[1:].lstrip().lower()
        if tagname.startswith('br'):
            return tag  # don't replace it
        else:
            return ''   # replace it with nothing, i.e. remove it
    # Remove tags except <br> tags
    text = re.sub('<.*?>', replace_tag, html)
    # Collapse whitespace to single spaces
    text = ' '.join(text.split())
    # Replace one or more <br> tags and any surrounding spaces
    # with two newlines
    text = re.sub('\s*(<.*?>\s*)+', '\n\n', text)
    # Remove whitespace from either end
    text = text.strip()
    return text
    
def scrape(article_id):
        # Encode article ID into base-64 - this is TL's observation
        encoded_id = base64.urlsafe_b64encode(str(article_id))
        print str(article_id) + ", " + str(encoded_id)
        url = 'http://www.pcc.org.uk/news/index.html?article=' + encoded_id
        page = scraperwiki.scrape(url)   
        # Convert to Unicode                              
        page = page.decode('latin-1')
        data = {'id': article_id}
        publications_array = []
        # Find each section of the page marked as: "<p><span class="GreyTitle">...</p>"
        # Helpfully, that gets exactly the data we want and no other junk.  
        values = re.findall('<p><span class="GreyTitle">(.*?)</p>', page, re.DOTALL)
        if values:
            for value in values:
                # fieldname and value always seem to be separated by "</span>"
                fieldname, value = value.split('</span>', 1)
                # Discard the colon separator from whichever it ends up in.
                fieldname = gettext(fieldname).rstrip(':')
                #value = gettext(value.lstrip(':'))
                #soup = BeautifulSoup.BeautifulSoup(value)
                #value = soup.findAll(text=True)
                if fieldname=="Publication": # Split out publications & clauses 
                    publications = re.split(r'[,/]', value)
                    print publications
                    for i, publication in enumerate(publications):
                        print i, publication.strip()
                        data[fieldname + "_" + str(i+1)] = publication.strip()
                        publications_array.append(publication.strip())
                elif fieldname=="Clauses Noted":
                    clauses = value.split(",")
                    for i, clause in enumerate(clauses):
                        data["clause_" + str(i+1)] = clause.strip()                    
                else:
                     data[fieldname] = value                        
            data['url'] = url
        return data

# ----- START -----

for article_id in xrange(6402, # this is the first article - 1767
                         6403): # hacky: but we can't tell when the last article will be using the base-64 method above, so choose 9999
    data = scrape(article_id)
    if data is None:
        print "Problem scraping article: " + str(article_id)
    elif data=={"id":article_id}:
        print "Article exists but is not structured:" + str(article_id)
    else:
        pprint(data)                           
        scraperwiki.datastore.save(['id'], data)

##################################################################
# Press Complaints Commission decisions: cases from their database
# http://www.pcc.org.uk/advanced_search.html
# Sorts cases by publication, outcome, and PCC code clause
# Adapted from an original version by Tom Lynn
##################################################################
# To do: fix up so doesn't fail if page=None (ie if scraperwiki breaks)

import scraperwiki
import BeautifulSoup
import base64
import lxml.etree
import re
from pprint import pprint

# Tom L's helper function to clean up the text
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    # An internal "helper for the helper" function: only keep <br> tags
    def replace_tag(match):
        tag = match.group()
        tagname = tag[1:].lstrip().lower()
        if tagname.startswith('br'):
            return tag  # don't replace it
        else:
            return ''   # replace it with nothing, i.e. remove it
    # Remove tags except <br> tags
    text = re.sub('<.*?>', replace_tag, html)
    # Collapse whitespace to single spaces
    text = ' '.join(text.split())
    # Replace one or more <br> tags and any surrounding spaces
    # with two newlines
    text = re.sub('\s*(<.*?>\s*)+', '\n\n', text)
    # Remove whitespace from either end
    text = text.strip()
    return text
    
def scrape(article_id):
        # Encode article ID into base-64 - this is TL's observation
        encoded_id = base64.urlsafe_b64encode(str(article_id))
        print str(article_id) + ", " + str(encoded_id)
        url = 'http://www.pcc.org.uk/news/index.html?article=' + encoded_id
        page = scraperwiki.scrape(url)   
        # Convert to Unicode                              
        page = page.decode('latin-1')
        data = {'id': article_id}
        publications_array = []
        # Find each section of the page marked as: "<p><span class="GreyTitle">...</p>"
        # Helpfully, that gets exactly the data we want and no other junk.  
        values = re.findall('<p><span class="GreyTitle">(.*?)</p>', page, re.DOTALL)
        if values:
            for value in values:
                # fieldname and value always seem to be separated by "</span>"
                fieldname, value = value.split('</span>', 1)
                # Discard the colon separator from whichever it ends up in.
                fieldname = gettext(fieldname).rstrip(':')
                #value = gettext(value.lstrip(':'))
                #soup = BeautifulSoup.BeautifulSoup(value)
                #value = soup.findAll(text=True)
                if fieldname=="Publication": # Split out publications & clauses 
                    publications = re.split(r'[,/]', value)
                    print publications
                    for i, publication in enumerate(publications):
                        print i, publication.strip()
                        data[fieldname + "_" + str(i+1)] = publication.strip()
                        publications_array.append(publication.strip())
                elif fieldname=="Clauses Noted":
                    clauses = value.split(",")
                    for i, clause in enumerate(clauses):
                        data["clause_" + str(i+1)] = clause.strip()                    
                else:
                     data[fieldname] = value                        
            data['url'] = url
        return data

# ----- START -----

for article_id in xrange(6402, # this is the first article - 1767
                         6403): # hacky: but we can't tell when the last article will be using the base-64 method above, so choose 9999
    data = scrape(article_id)
    if data is None:
        print "Problem scraping article: " + str(article_id)
    elif data=={"id":article_id}:
        print "Article exists but is not structured:" + str(article_id)
    else:
        pprint(data)                           
        scraperwiki.datastore.save(['id'], data)

