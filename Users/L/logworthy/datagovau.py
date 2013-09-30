import scraperwiki

# Blank Python

def safestrip(text):
    try:
        return text.strip()
    except:
        return ''

html = scraperwiki.scrape("http://data.gov.au/data/")

print html

import lxml.html 
root = lxml.html.fromstring(html) 
for tr in root.cssselect("tbody tr"):
    
    # get a basic link/description
    row = {}
    data = tr.cssselect("a[class='result-title']") 
    row['href'] = data[0].attrib['href']
    row['title'] = data[0].text
    scraperwiki.sqlite.save(table_name='href_to_title', unique_keys=['title'], data=row)

    # get detailed data from the follow-through page
    try:
        row_html = scraperwiki.scrape(row['href'])
        row_root = lxml.html.fromstring(row_html) 
        
        det_row = {}
        # general descriptors
        dds = row_root.cssselect('dl:first-child dd')
        for dd in dds:
            try:
                text = dd.text.strip()
            except:
                text = ''
            if text != '' and dd.attrib.has_key('property'):
                prop = dd.attrib['property'].replace(':', '_').replace('.', '_')
                det_row[prop] = text
        
        # description
        ps = row_root.cssselect("dd[property='dc:description'] p")
        desc = ' '.join([safestrip(x.text) for x in ps])
        det_row['description'] = desc
    
        # add our primary key
        det_row['title'] = row['title']
        
        #save the row
        scraperwiki.sqlite.save(table_name='title_details', unique_keys=['title'], data=det_row)
        
        # links
        link_row = {}
        link_list = row_root.cssselect("dd ul li")
        for li in link_list:
            try:
                link_row['title'] = row['title']
                link_row['link'] = li.cssselect("a[property='dcat:accessURL']")[0].attrib['href']
                link_row['format'] = li.cssselect(":nth-child(2)")[0].text.strip()
                link_row['size'] = li.cssselect(":nth-child(3)")[0].text.strip()
                link_row['hits'] = li.cssselect(":nth-child(4)")[0].text.strip()
                scraperwiki.sqlite.save(table_name='title_links', unique_keys=['title', 'link'], data=link_row)
            except:
                pass
    except:
        pass


    # add categories
    row2 = {}
    categories = tr.cssselect("a[class='result-category roundedCorner']")
    for category in categories:    
        row2['category'] = category.text
        row2['title'] = row['title']
        scraperwiki.sqlite.save(table_name='category_to_title', unique_keys=['category', 'title'], data=row2)
import scraperwiki

# Blank Python

def safestrip(text):
    try:
        return text.strip()
    except:
        return ''

html = scraperwiki.scrape("http://data.gov.au/data/")

print html

import lxml.html 
root = lxml.html.fromstring(html) 
for tr in root.cssselect("tbody tr"):
    
    # get a basic link/description
    row = {}
    data = tr.cssselect("a[class='result-title']") 
    row['href'] = data[0].attrib['href']
    row['title'] = data[0].text
    scraperwiki.sqlite.save(table_name='href_to_title', unique_keys=['title'], data=row)

    # get detailed data from the follow-through page
    try:
        row_html = scraperwiki.scrape(row['href'])
        row_root = lxml.html.fromstring(row_html) 
        
        det_row = {}
        # general descriptors
        dds = row_root.cssselect('dl:first-child dd')
        for dd in dds:
            try:
                text = dd.text.strip()
            except:
                text = ''
            if text != '' and dd.attrib.has_key('property'):
                prop = dd.attrib['property'].replace(':', '_').replace('.', '_')
                det_row[prop] = text
        
        # description
        ps = row_root.cssselect("dd[property='dc:description'] p")
        desc = ' '.join([safestrip(x.text) for x in ps])
        det_row['description'] = desc
    
        # add our primary key
        det_row['title'] = row['title']
        
        #save the row
        scraperwiki.sqlite.save(table_name='title_details', unique_keys=['title'], data=det_row)
        
        # links
        link_row = {}
        link_list = row_root.cssselect("dd ul li")
        for li in link_list:
            try:
                link_row['title'] = row['title']
                link_row['link'] = li.cssselect("a[property='dcat:accessURL']")[0].attrib['href']
                link_row['format'] = li.cssselect(":nth-child(2)")[0].text.strip()
                link_row['size'] = li.cssselect(":nth-child(3)")[0].text.strip()
                link_row['hits'] = li.cssselect(":nth-child(4)")[0].text.strip()
                scraperwiki.sqlite.save(table_name='title_links', unique_keys=['title', 'link'], data=link_row)
            except:
                pass
    except:
        pass


    # add categories
    row2 = {}
    categories = tr.cssselect("a[class='result-category roundedCorner']")
    for category in categories:    
        row2['category'] = category.text
        row2['title'] = row['title']
        scraperwiki.sqlite.save(table_name='category_to_title', unique_keys=['category', 'title'], data=row2)
