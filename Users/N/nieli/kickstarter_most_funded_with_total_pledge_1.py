"""
This a test scraper.

Kickstarter pagination:
[...]
<a href="/discover/categories/art/most-funded?page=8">8</a> <a href="/discover/categories/art/most-funded?page=9">9</a> <span class="gap">&hellip;</span> <a href="/discover/categories/art/most-funded?page=162">162</a> <a href="/discover/categories/art/most-funded?page=163">163</a> <a class="next_page" href="/discover/categories/art/most-funded?page=2" rel="next">Next</a></div>
[...]

Final page:
[...]
<a href="/discover/categories/art/most-funded?page=159">159</a> <a href="/discover/categories/art/most-funded?page=160">160</a> <a href="/discover/categories/art/most-funded?page=161">161</a> <a href="/discover/categories/art/most-funded?page=162" rel="prev">162</a> <em class="current">163</em> <span class="next_page disabled">Next</span></div>
[...]

Example of page url:
http://www.kickstarter.com/discover/categories/art/most-funded?page=47
"""
import scraperwiki, lxml.html, itertools, datetime


"""
Dummy boilerplate function.
Parse a single page with projects.
Each page contains 15 projects.

elementPage = returned by  lxml.html.fromstring()

returns an array:
[0] = number of projects.
[1] = total amount pledge.
[2] = page minimum pledge.
[3] = page maximum pledge.
"""
def parsePage(elementPage):
    projects = elementPage.find_class("project")
    counter = 0
    pledgeValue = 0
    min = -1
    max = 0
    res = []
    for prj in projects :
        pledgeText = (prj.find_class("pledged")[0]).text_content()
        pledgeText = pledgeText.replace(',', '').replace('$', '').replace('\npledged\n', '')
        amount = float(pledgeText)
        pledgeValue += amount
        if(amount>max) :
            max = amount
        if(min<0 or amount<min) :
            min = amount
        counter += 1
    res.append(counter)
    res.append(pledgeValue)
    res.append(min)
    res.append(max)
    return res

host = "http://www.kickstarter.com"
baseUrl = "/discover/most-funded"

#Resume state.
mainPageCounter = scraperwiki.sqlite.get_var("first_category_to_parse", 0)
totalPrj = scraperwiki.sqlite.get_var("last_project_counter", 0)
totalPledge = scraperwiki.sqlite.get_var("pledge_total", 0.0)

print "Connecting to: " + host+baseUrl
mostFunded = scraperwiki.scrape(host+baseUrl)
root = lxml.html.fromstring(mostFunded)
#For each category there is one "View all" link.
categories = root.find_class("discover-row-header")
viewAllLinks = root.find_class("link-view-all")

date = datetime.datetime.now()

while mainPageCounter < min(len(categories), len(viewAllLinks)) :
    category = categories[mainPageCounter]
    viewAll = viewAllLinks[mainPageCounter]
    categoryLabel = category.text_content()
    linkViewAll = host + viewAll.get("href")
    print "Loading... Category: " + categoryLabel + " Link: " + linkViewAll
    page = lxml.html.fromstring(scraperwiki.scrape(linkViewAll))
    #Parse first page
    tmpValue = parsePage(page)
    tmpPrj = tmpValue[0]
    tmpPledge = tmpValue[1]
    catMin = tmpValue[2]
    catMax = tmpValue[3]
    totalPrj+=tmpPrj
    totalPledge+=tmpPledge
    #Next page
    nextPage = page.find_class("next_page")
    pageCounter = 1
    #There is always at least one element. See top comment for details.
    while(nextPage[0].get("href") is not None) :
        pageCounter += 1
        #print "   Loading page " + str(pageCounter)
        #There is always at least one element. See top comment for details.
        page = lxml.html.fromstring(scraperwiki.scrape(host + nextPage[0].get("href")))
        #Next page
        tmpValue = parsePage(page)
        tmpPrj+=tmpValue[0]
        tmpPledge+=tmpValue[1]
        if(catMin>tmpValue[2]) :
            catMin = tmpValue[2]
        if(catMax<tmpValue[3]) :
            catMax = tmpValue[3]
        print "Category " + categoryLabel + " pledged: " + str(tmpPledge) + " $ MIN: " + str(catMin) + " $ MAX: " + str(catMax) + " $"
        totalPrj+=tmpValue[0]
        totalPledge+=tmpValue[1]
        nextPage = page.find_class("next_page")
    #Save in DB
    record = {
             'Category' : categoryLabel,
             'Number of projects' : tmpPrj,
             'US dollars' : tmpPledge,
             'Min' : catMin,
             'Max' : catMax,
             'Avg' : (tmpPledge / tmpPrj),
             'M_Y' : date.strftime("%m_%Y")
             }
    scraperwiki.sqlite.save(unique_keys=['Category'], data=record)
    print "Category loaded. Number of projects: " + str(tmpPrj)
    mainPageCounter+=1
    scraperwiki.sqlite.save_var("first_category_to_parse", mainPageCounter)
    print "first_category_to_parse -> " + str(mainPageCounter)
    scraperwiki.sqlite.save_var("last_project_counter", totalPrj)
    scraperwiki.sqlite.save_var("pledge_total", totalPledge)

print "Done. Total number of projects: " + str(totalPrj)
record = {
         'Category' : "Total",
         'Number of projects' : totalPrj,
         'US dollars' : totalPledge,
         'M_Y' : date.strftime("%m_%Y")
         }
scraperwiki.sqlite.save(unique_keys=['Category'], data=record)

#Reset for next time.
scraperwiki.sqlite.save_var("first_category_to_parse", 0)
scraperwiki.sqlite.save_var("last_project_counter", 0)
scraperwiki.sqlite.save_var("pledge_total", 0.0)