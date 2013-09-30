# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.gorkanajobs.co.uk/jobs/journalist/intern/")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called internspage
internspage = lxml.html.fromstring(html) 
# get all the <div> tags from within that, put in variable called jobdescs
jobdescs = internspage.cssselect("div class='jobWrap'")
for joblinks in jobdescs:
    print lxml.html.tostring(joblinks) #the tostring command converts the lxml element back to string
    print joblinks.text
#for joblinks in jobdescs:
#    record = { "jobtext" : joblinks.text } #jobtext is the name of the column, storing the text of joblinks
#    scraperwiki.sqlite.save(["jobtext"], record) #save the records# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.gorkanajobs.co.uk/jobs/journalist/intern/")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called internspage
internspage = lxml.html.fromstring(html) 
# get all the <div> tags from within that, put in variable called jobdescs
jobdescs = internspage.cssselect("div class='jobWrap'")
for joblinks in jobdescs:
    print lxml.html.tostring(joblinks) #the tostring command converts the lxml element back to string
    print joblinks.text
#for joblinks in jobdescs:
#    record = { "jobtext" : joblinks.text } #jobtext is the name of the column, storing the text of joblinks
#    scraperwiki.sqlite.save(["jobtext"], record) #save the records# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.gorkanajobs.co.uk/jobs/journalist/intern/")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called internspage
internspage = lxml.html.fromstring(html) 
# get all the <div> tags from within that, put in variable called jobdescs
jobdescs = internspage.cssselect("div class='jobWrap'")
for joblinks in jobdescs:
    print lxml.html.tostring(joblinks) #the tostring command converts the lxml element back to string
    print joblinks.text
#for joblinks in jobdescs:
#    record = { "jobtext" : joblinks.text } #jobtext is the name of the column, storing the text of joblinks
#    scraperwiki.sqlite.save(["jobtext"], record) #save the records# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.gorkanajobs.co.uk/jobs/journalist/intern/")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called internspage
internspage = lxml.html.fromstring(html) 
# get all the <div> tags from within that, put in variable called jobdescs
jobdescs = internspage.cssselect("div class='jobWrap'")
for joblinks in jobdescs:
    print lxml.html.tostring(joblinks) #the tostring command converts the lxml element back to string
    print joblinks.text
#for joblinks in jobdescs:
#    record = { "jobtext" : joblinks.text } #jobtext is the name of the column, storing the text of joblinks
#    scraperwiki.sqlite.save(["jobtext"], record) #save the records# import a module (library) that helps us do scraping
import scraperwiki
# import another that helps us extract things from the scraped data
import lxml.html
# use that module's scrape function to grab the contents of a URL and put it in the variable HTML
html = scraperwiki.scrape("http://www.gorkanajobs.co.uk/jobs/journalist/intern/")
# use the lxml.html's fromstring function to grab some structured data, put in a variable called internspage
internspage = lxml.html.fromstring(html) 
# get all the <div> tags from within that, put in variable called jobdescs
jobdescs = internspage.cssselect("div class='jobWrap'")
for joblinks in jobdescs:
    print lxml.html.tostring(joblinks) #the tostring command converts the lxml element back to string
    print joblinks.text
#for joblinks in jobdescs:
#    record = { "jobtext" : joblinks.text } #jobtext is the name of the column, storing the text of joblinks
#    scraperwiki.sqlite.save(["jobtext"], record) #save the records