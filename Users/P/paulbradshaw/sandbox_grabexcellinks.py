import scraperwiki
import lxml.html

def grabexcellinks(URL):
    #Use Scraperwiki's scrape function on 'URL', put results in new variable 'html'
    html = scraperwiki.scrape(URL)
    #and show it us
    print html
    #Use lxml.html's fromstring function on 'html', put results in new variable 'root'
    root = lxml.html.fromstring(html)
    #use cssselect method on 'root' to grab all <a> tags within a <li> tag - and put in a new list variable 'links'
    links = root.cssselect('div.rte li a')
    #for each item in that list variable, from the first to the second last [0:-1], put it in the variable 'link'
    for link in links[0:]:
        #and print the text_content of that (after the string "link text:")
        print "link text:", link.text_content()
        #use the attrib.get method on 'link' to grab the href= attribute of the HTML, and put in new 'linkurl' variable
        linkurl = link.attrib.get('href')
        #print it
        print "link type:", linkurl[-4:]
        #run the function scrapesheets, using that variable as the parameter
        if linkurl[-4:] == "xlsx":
            print "EXCEL!"
        #scrapespreadsheet(linkurl)

grabexcellinks('http://www.parliament.uk/business/lords/whos-in-the-house-of-lords/house-of-lords-expenses/')

#for http://www.parliament.uk/business/lords/whos-in-the-house-of-lords/house-of-lords-expenses/
#the links are in <li><a href="/documents/lords-finance-office/2012-13/allowances-expenses-2012-13-month-10-january-2013.xlsx" class="document">January 2013 (<span><img src="/assets/images/xlsx-icon.gif" alt="XLSX" /></span> XLSX 94 KB)</a></li>

#So the line 11 would be: links = root.cssselect('li a')

#We also want to only grab XLS links so we also need a test
