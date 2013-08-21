import scraperwiki

# Blank Python

def safestrip(text):
    try:
        return text.strip()
    except:
        return ''

def get_td_from_tr(tr):
    return nid_tr.cssselect("td")[1].text

baseurl = "http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx"
html = scraperwiki.scrape("http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results")

print html

import lxml.html 
root = lxml.html.fromstring(html) 
for tr in root.cssselect("tbody tr"):
    
    # get a basic link/description
    row = {}
    data = tr.cssselect("td") 
    row['trade_name'] = data[0].text
    row['suburb'] = data[1].text
    row['council'] = data[2].text
    notice = data[3].cssselect("a")[0]
    row['notice_id'] = notice.text.strip()
    row['date'] = data[4].text
    row['party'] = data[5].text
    row['notes'] = data[6].text

    if row['notice_id']:
        try:
            nid_html = scraperwiki.scrape(baseurl+notice.attrib['href'])
        except:
            pass
        
        nid_root = lxml.html.fromstring(nid_html)
        nid_trs = nid_root.cssselect("tbody tr") 
        row['address'] = nid_trs[2].cssselect("td")[1].text 

        scraperwiki.sqlite.save(table_name='notice_details', unique_keys=['notice_id'], data=row)

    """
    # get detailed data from the follow-through page
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


    # add categories
    row2 = {}
    categories = tr.cssselect("a[class='result-category roundedCorner']")
    for category in categories:    
        row2['category'] = category.text
        row2['title'] = row['title']
        scraperwiki.sqlite.save(table_name='category_to_title', unique_keys=['category', 'title'], data=row2)
    """