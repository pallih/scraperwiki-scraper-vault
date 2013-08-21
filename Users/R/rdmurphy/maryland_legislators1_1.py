import scraperwiki
import lxml.html   

html = scraperwiki.scrape("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS")
root = lxml.html.fromstring(html)


def process_multirows(doc):
    return ';'.join(doc.itertext())

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)>3:
        links = tds[0].cssselect('a')
        for link in links:
            url = link.attrib.get('href')
            link='http://mgaleg.maryland.gov/webmga/' + url
            html1 = scraperwiki.scrape(link)
            root1 = lxml.html.fromstring(html1)
            more_data =[]    
    
            # h2 tag contains legislator name and position
            for header in root1.cssselect("h2"):
                legindex = header.text_content().find(' ')
                legtitlename = header.text_content()
                position = legtitlename[:legindex]
                legname1 = legtitlename[legindex+1:]
                more_data.append(position)
                more_data.append(legname1)
    
            #add items to more_data
            for tr1 in root1.cssselect("#ContentPlaceHolder1_div_03 tr"):
                tds1 = tr1.cssselect("td")
                more_data.append(tds1[0])

            #populate dictmore with linked-page items
            dictmore = {
            'position': more_data[0],
            'legname1': more_data[1],
            'address': process_multirows(more_data[3]),
            'phone': more_data[4].text_content(),
            'contact': more_data[5].text_content(),
            'first_appointed': more_data[6].text_content(),
            'committees': process_multirows(more_data[7]),
            'party': more_data[8].text_content()
            }

        legis_dict = {
        'legislator' : tds[0].text_content(),
        'district' : tds[1].text_content(),
        'county' : tds[2].text_content(),
        'link' : link
         }


        # combine the dictionary from the main page, with the dictionary from the linked page
        legis_dict.update(dictmore)

        scraperwiki.sqlite.save(unique_keys=['legislator'], data=legis_dict)
