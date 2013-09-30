import scraperwiki
import lxml.html
import unicodedata


link = "http://www.hdpi.com.cn/est/TZ/GSGK/about.aspx"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#find the locations that are in the tables we want to parse
#The first table is coal/natural gas, while the second is renewable
findTheTables = root.xpath("//table/tbody/tr/td/p/strong/font/span[text()='Installed']")


for findTheTable in findTheTables:
    #back up and find the table
    table = findTheTable.xpath("../../../../../../..")[0]
    #now get the list of entries in the table
    rows = table.xpath("./tbody/tr[position()>1]")
    for row in rows:
        installationInfo = dict()

        #just get the text_content of the td node
        #and ignore all the span & font tags that are nested in there
        installationInfo['Name'] = row.xpath("./td[1]")[0].text_content().replace('  ', ' ')
        installationInfo['Installed Capacity'] = row.xpath("./td[2]")[0].text_content()
        installationInfo['Equity Interest'] = row.xpath("./td[3]")[0].text_content()
        installationInfo['Generating units'] = row.xpath("./td[4]")[0].text_content().replace('  ', ' ')

        #add reference link to original data source
        installationInfo['reference_link'] = 'http://www.hdpi.com.cn/est/TZ/GSGK/about.aspx'
        scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
import scraperwiki
import lxml.html
import unicodedata


link = "http://www.hdpi.com.cn/est/TZ/GSGK/about.aspx"
html = scraperwiki.scrape(link)
root = lxml.html.fromstring(html)

#find the locations that are in the tables we want to parse
#The first table is coal/natural gas, while the second is renewable
findTheTables = root.xpath("//table/tbody/tr/td/p/strong/font/span[text()='Installed']")


for findTheTable in findTheTables:
    #back up and find the table
    table = findTheTable.xpath("../../../../../../..")[0]
    #now get the list of entries in the table
    rows = table.xpath("./tbody/tr[position()>1]")
    for row in rows:
        installationInfo = dict()

        #just get the text_content of the td node
        #and ignore all the span & font tags that are nested in there
        installationInfo['Name'] = row.xpath("./td[1]")[0].text_content().replace('  ', ' ')
        installationInfo['Installed Capacity'] = row.xpath("./td[2]")[0].text_content()
        installationInfo['Equity Interest'] = row.xpath("./td[3]")[0].text_content()
        installationInfo['Generating units'] = row.xpath("./td[4]")[0].text_content().replace('  ', ' ')

        #add reference link to original data source
        installationInfo['reference_link'] = 'http://www.hdpi.com.cn/est/TZ/GSGK/about.aspx'
        scraperwiki.sqlite.save(unique_keys=['Name'], data=installationInfo)
