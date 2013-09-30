import scraperwiki
import lxml.html   

# https://scraperwiki.com/docs/python/python_intro_tutorial/#

html = scraperwiki.scrape("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS")
root = lxml.html.fromstring(html)

#create list of URLs
##url_list=[]

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)>3:

        links = tds[0].cssselect('a')
        for link in links:
            url = link.attrib.get('href')
##        url_list.append(url)

        data = {
            'legislator' : tds[0].text_content(),
            'district' : tds[1].text_content(),
            'county' : tds[2].text_content(),
            'link' : url
         }

# sample link ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS']:
#url_list= ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=afzali&stab=01&ys=2013RS','http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS', 'http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=branch&stab=01&ys=2013RS']
##for link in url_list:
#        link='http://mgaleg.maryland.gov/webmga/'+link
        link=url  ##
        html1 = scraperwiki.scrape(link)
        root1 = lxml.html.fromstring(html1)
        more_data =[]
    
    # h2 tag contains legislator name and position
        for header in root1.cssselect("h2"):
            legindex = header.text_content().find(' ')
            legtitlename = header.text_content()
            legtitle = legtitlename[:legindex]
            legname = legtitlename[legindex+1:]
            more_data.append(legtitle)
            more_data.append(legname)


        for tr1 in root1.cssselect("#ContentPlaceHolder1_div_03 tr"):
            tds1 = tr1.cssselect("td")
            more_data.append(tds1[0].text_content())

        dictmore = {
        'position': more_data[0],
        'name1': more_data[1],
        'address': more_data[3],
        'phone': more_data[4],
        'contact': more_data[5],
        'first_appointed': more_data[6],
        'committees': more_data[7],
        'party': more_data[8] 
        }
    #print more_data
#print data
#print dictmore

# combine the dictionary from the main page, with the dictionary from the linked page
        dictlist = [data, dictmore]
        legislators = {}
        for d in dictlist:
            legislators.update(d)
scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)

#print legislators
#scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)
#        print data
    #print url_list


import scraperwiki
import lxml.html   

# https://scraperwiki.com/docs/python/python_intro_tutorial/#

html = scraperwiki.scrape("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS")
root = lxml.html.fromstring(html)

#create list of URLs
##url_list=[]

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)>3:

        links = tds[0].cssselect('a')
        for link in links:
            url = link.attrib.get('href')
##        url_list.append(url)

        data = {
            'legislator' : tds[0].text_content(),
            'district' : tds[1].text_content(),
            'county' : tds[2].text_content(),
            'link' : url
         }

# sample link ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS']:
#url_list= ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=afzali&stab=01&ys=2013RS','http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS', 'http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=branch&stab=01&ys=2013RS']
##for link in url_list:
#        link='http://mgaleg.maryland.gov/webmga/'+link
        link=url  ##
        html1 = scraperwiki.scrape(link)
        root1 = lxml.html.fromstring(html1)
        more_data =[]
    
    # h2 tag contains legislator name and position
        for header in root1.cssselect("h2"):
            legindex = header.text_content().find(' ')
            legtitlename = header.text_content()
            legtitle = legtitlename[:legindex]
            legname = legtitlename[legindex+1:]
            more_data.append(legtitle)
            more_data.append(legname)


        for tr1 in root1.cssselect("#ContentPlaceHolder1_div_03 tr"):
            tds1 = tr1.cssselect("td")
            more_data.append(tds1[0].text_content())

        dictmore = {
        'position': more_data[0],
        'name1': more_data[1],
        'address': more_data[3],
        'phone': more_data[4],
        'contact': more_data[5],
        'first_appointed': more_data[6],
        'committees': more_data[7],
        'party': more_data[8] 
        }
    #print more_data
#print data
#print dictmore

# combine the dictionary from the main page, with the dictionary from the linked page
        dictlist = [data, dictmore]
        legislators = {}
        for d in dictlist:
            legislators.update(d)
scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)

#print legislators
#scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)
#        print data
    #print url_list


import scraperwiki
import lxml.html   

# https://scraperwiki.com/docs/python/python_intro_tutorial/#

html = scraperwiki.scrape("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS")
root = lxml.html.fromstring(html)

#create list of URLs
##url_list=[]

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)>3:

        links = tds[0].cssselect('a')
        for link in links:
            url = link.attrib.get('href')
##        url_list.append(url)

        data = {
            'legislator' : tds[0].text_content(),
            'district' : tds[1].text_content(),
            'county' : tds[2].text_content(),
            'link' : url
         }

# sample link ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS']:
#url_list= ['http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=afzali&stab=01&ys=2013RS','http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=reilly&stab=01&ys=2013RS', 'http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=sponpage&tab=subject6&id=branch&stab=01&ys=2013RS']
##for link in url_list:
#        link='http://mgaleg.maryland.gov/webmga/'+link
        link=url  ##
        html1 = scraperwiki.scrape(link)
        root1 = lxml.html.fromstring(html1)
        more_data =[]
    
    # h2 tag contains legislator name and position
        for header in root1.cssselect("h2"):
            legindex = header.text_content().find(' ')
            legtitlename = header.text_content()
            legtitle = legtitlename[:legindex]
            legname = legtitlename[legindex+1:]
            more_data.append(legtitle)
            more_data.append(legname)


        for tr1 in root1.cssselect("#ContentPlaceHolder1_div_03 tr"):
            tds1 = tr1.cssselect("td")
            more_data.append(tds1[0].text_content())

        dictmore = {
        'position': more_data[0],
        'name1': more_data[1],
        'address': more_data[3],
        'phone': more_data[4],
        'contact': more_data[5],
        'first_appointed': more_data[6],
        'committees': more_data[7],
        'party': more_data[8] 
        }
    #print more_data
#print data
#print dictmore

# combine the dictionary from the main page, with the dictionary from the linked page
        dictlist = [data, dictmore]
        legislators = {}
        for d in dictlist:
            legislators.update(d)
scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)

#print legislators
#scraperwiki.sqlite.save(unique_keys=['legislator'], data=legislators)
#        print data
    #print url_list


