#Works on one specified linked page
#NEXT: Store all links and loop through javascript for each (i.e. add @Title=...)

import scraperwiki
import mechanize
import re
import lxml.html

#This url is where adult hearing results start - but other services have the same URL
#we need to use mechanize to submit the javascript link to those.

#HTML of link is:
#href="javascript:__doPostBack('ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519','__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};')">Continuing Care Children and Young People</a>

url = 'https://www.supply2health.nhs.uk/AQPResourceCentre/AQPMap/Pages/servicesmapdata.aspx'
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

record = {} 
id = 0 

#We only want to grab the first page linked from here, so this loop only needs to run twice:
#Once (0) for the main page and then again (1) for the linked page
for pagenum in range(2):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    #html = scraperwiki.scrape(url)
    print "HTML", html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.AspNet-WebPart table tr")
    for row in rows[5:]:
        print row
        record['row'] = row.text_content()
        table_cells = row.cssselect("td")
  #      if table_cells[2] is not None:
#        record['First col'] = table_cells[0].text_content()
#            record['2nd col'] = table_cells[1].text_content()
 #           record['3rd col'] = table_cells[2].text_content()
        scraperwiki.sqlite.save(['row'],record) 
#    for name in re.findall("tr>(.*?)</tr>", html): #NEW CODE
#        id = id+1 #NEW CODE
 #       record['ID'] = id #NEW CODE
  #      record['Name'] = name #NEW CODE
        record['resultspage'] = pagenum
        print record #NEW CODE
    meyelink = re.search("javascript:__doPostBack", html) 
    if not meyelink:
        print "NOTLINKING!"
        break

    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519'
    br['__EVENTARGUMENT'] = '__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};'
    response = br.submit()

#Works on one specified linked page
#NEXT: Store all links and loop through javascript for each (i.e. add @Title=...)

import scraperwiki
import mechanize
import re
import lxml.html

#This url is where adult hearing results start - but other services have the same URL
#we need to use mechanize to submit the javascript link to those.

#HTML of link is:
#href="javascript:__doPostBack('ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519','__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};')">Continuing Care Children and Young People</a>

url = 'https://www.supply2health.nhs.uk/AQPResourceCentre/AQPMap/Pages/servicesmapdata.aspx'
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

record = {} 
id = 0 

#We only want to grab the first page linked from here, so this loop only needs to run twice:
#Once (0) for the main page and then again (1) for the linked page
for pagenum in range(2):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    #html = scraperwiki.scrape(url)
    print "HTML", html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.AspNet-WebPart table tr")
    for row in rows[5:]:
        print row
        record['row'] = row.text_content()
        table_cells = row.cssselect("td")
  #      if table_cells[2] is not None:
#        record['First col'] = table_cells[0].text_content()
#            record['2nd col'] = table_cells[1].text_content()
 #           record['3rd col'] = table_cells[2].text_content()
        scraperwiki.sqlite.save(['row'],record) 
#    for name in re.findall("tr>(.*?)</tr>", html): #NEW CODE
#        id = id+1 #NEW CODE
 #       record['ID'] = id #NEW CODE
  #      record['Name'] = name #NEW CODE
        record['resultspage'] = pagenum
        print record #NEW CODE
    meyelink = re.search("javascript:__doPostBack", html) 
    if not meyelink:
        print "NOTLINKING!"
        break

    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519'
    br['__EVENTARGUMENT'] = '__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};'
    response = br.submit()

#Works on one specified linked page
#NEXT: Store all links and loop through javascript for each (i.e. add @Title=...)

import scraperwiki
import mechanize
import re
import lxml.html

#This url is where adult hearing results start - but other services have the same URL
#we need to use mechanize to submit the javascript link to those.

#HTML of link is:
#href="javascript:__doPostBack('ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519','__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};')">Continuing Care Children and Young People</a>

url = 'https://www.supply2health.nhs.uk/AQPResourceCentre/AQPMap/Pages/servicesmapdata.aspx'
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

record = {} 
id = 0 

#We only want to grab the first page linked from here, so this loop only needs to run twice:
#Once (0) for the main page and then again (1) for the linked page
for pagenum in range(2):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    #html = scraperwiki.scrape(url)
    print "HTML", html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.AspNet-WebPart table tr")
    for row in rows[5:]:
        print row
        record['row'] = row.text_content()
        table_cells = row.cssselect("td")
  #      if table_cells[2] is not None:
#        record['First col'] = table_cells[0].text_content()
#            record['2nd col'] = table_cells[1].text_content()
 #           record['3rd col'] = table_cells[2].text_content()
        scraperwiki.sqlite.save(['row'],record) 
#    for name in re.findall("tr>(.*?)</tr>", html): #NEW CODE
#        id = id+1 #NEW CODE
 #       record['ID'] = id #NEW CODE
  #      record['Name'] = name #NEW CODE
        record['resultspage'] = pagenum
        print record #NEW CODE
    meyelink = re.search("javascript:__doPostBack", html) 
    if not meyelink:
        print "NOTLINKING!"
        break

    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519'
    br['__EVENTARGUMENT'] = '__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};'
    response = br.submit()

#Works on one specified linked page
#NEXT: Store all links and loop through javascript for each (i.e. add @Title=...)

import scraperwiki
import mechanize
import re
import lxml.html

#This url is where adult hearing results start - but other services have the same URL
#we need to use mechanize to submit the javascript link to those.

#HTML of link is:
#href="javascript:__doPostBack('ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519','__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};')">Continuing Care Children and Young People</a>

url = 'https://www.supply2health.nhs.uk/AQPResourceCentre/AQPMap/Pages/servicesmapdata.aspx'
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

record = {} 
id = 0 

#We only want to grab the first page linked from here, so this loop only needs to run twice:
#Once (0) for the main page and then again (1) for the linked page
for pagenum in range(2):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    #html = scraperwiki.scrape(url)
    print "HTML", html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.AspNet-WebPart table tr")
    for row in rows[5:]:
        print row
        record['row'] = row.text_content()
        table_cells = row.cssselect("td")
  #      if table_cells[2] is not None:
#        record['First col'] = table_cells[0].text_content()
#            record['2nd col'] = table_cells[1].text_content()
 #           record['3rd col'] = table_cells[2].text_content()
        scraperwiki.sqlite.save(['row'],record) 
#    for name in re.findall("tr>(.*?)</tr>", html): #NEW CODE
#        id = id+1 #NEW CODE
 #       record['ID'] = id #NEW CODE
  #      record['Name'] = name #NEW CODE
        record['resultspage'] = pagenum
        print record #NEW CODE
    meyelink = re.search("javascript:__doPostBack", html) 
    if not meyelink:
        print "NOTLINKING!"
        break

    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl06$g_fca36db7_d8d6_45d7_a92c_3c9f09d59519'
    br['__EVENTARGUMENT'] = '__connect={g_bf685cc5_241d_474e_a4fd_08634fd8fecd*@Title=Continuing Care Children and Young People};'
    response = br.submit()

