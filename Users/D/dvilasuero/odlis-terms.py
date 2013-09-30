import scraperwiki

ini_html = scraperwiki.scrape('http://www.abc-clio.com/ODLIS/odlis_b.aspx')



import lxml.html

from lxml.html.clean import clean_html


ini_root = lxml.html.fromstring(ini_html) # turn our HTML into an lxml object

# retrieve list of URLs
seeds = ini_root.cssselect('div.inner a')
for seed in seeds:
    # get href of each anchor
    if seed.get("href").find("ODLIS/odlis_"):
        dict_url = "http://www.abc-clio.com" + seed.get("href")
        
        # for each dictionary page retrive terms
        html = scraperwiki.scrape(dict_url)
        root = lxml.html.fromstring(html) # turn our HTML into an lxml object
        terms = root.cssselect('div#ctl00_center_AutomatedContent div') # get all the <td> tags
        for term in terms:
           
            # extract term name
            term_label = term.xpath('a/b')[0].text 
            
            # extract term description and strip all html tags
            html_desc = clean_html(term.xpath('dd')[0])
            term_description = html_desc.text_content()
        
            # save the data in the datastore
            scraperwiki.sqlite.save(['label'], data={"label":term_label, "description":term_description}) 
import scraperwiki

ini_html = scraperwiki.scrape('http://www.abc-clio.com/ODLIS/odlis_b.aspx')



import lxml.html

from lxml.html.clean import clean_html


ini_root = lxml.html.fromstring(ini_html) # turn our HTML into an lxml object

# retrieve list of URLs
seeds = ini_root.cssselect('div.inner a')
for seed in seeds:
    # get href of each anchor
    if seed.get("href").find("ODLIS/odlis_"):
        dict_url = "http://www.abc-clio.com" + seed.get("href")
        
        # for each dictionary page retrive terms
        html = scraperwiki.scrape(dict_url)
        root = lxml.html.fromstring(html) # turn our HTML into an lxml object
        terms = root.cssselect('div#ctl00_center_AutomatedContent div') # get all the <td> tags
        for term in terms:
           
            # extract term name
            term_label = term.xpath('a/b')[0].text 
            
            # extract term description and strip all html tags
            html_desc = clean_html(term.xpath('dd')[0])
            term_description = html_desc.text_content()
        
            # save the data in the datastore
            scraperwiki.sqlite.save(['label'], data={"label":term_label, "description":term_description}) 
