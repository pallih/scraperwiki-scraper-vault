#Import Neccessary Packages
import scraperwiki
import lxml.html
import string
import mechanize
import re

targetURL="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Economic_Data/Cultivators.aspx"


#This Code Snippet store all the statename in a list
#stateName[]

# Opening URL
webMechanize = mechanize.Browser()
webMechanize.addHeaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
webPage = webMechanize.open(targetURL)

#reads the source file for the web page
webPageSource = webPage.read() 

#webMechanize.select_form(nr=0)    #Point1
#webMechanize.select_form(name="Form1")
#webMechanize.set_all_readonly(False)
print "webpagesource"
print(webPageSource)

#webMechanize["txtUserId"] = "UserName"
#webMechanize["Document.Form1.txtPassword.value"] = "Password"
#var=webMechanize.submit()

html = scraperwiki.scrape(targetURL)
root = lxml.html.fromstring(html)

print(html)

#javaMechanize = re.search("rdb", webPageSource)
#if not javaMechanize:
#    print "xyz"


#webMechanize["__EVENTTARGET"] = "01"
#webMechanize["__EVENTARGUMENT"] =""

#webPage = webMechanize.submit()

 # source code after selecting State Option
#webPageSource=webPage.read()

#Store StateName in StateName List
#for webPageSourceState in webPageSource.cssselect("select.drpState option"):
#    print(webPageSourceState.text_content())

print("Complete")
