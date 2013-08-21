import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://www.w4mpjobs.org/SearchJobs.aspx?search=alljobs'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

br = mechanize.Browser()
response = br.open(base_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

#the options in the form are as follows (found by looking at the results of print above)
#  <TextControl(ctl00$MainContent$txtSearch=)>
#  <RadioControl(ctl00$MainContent$rbPoliticalParties=[Labour, Conservative, Lib Dem, Any])>
#  <RadioControl(ctl00$MainContent$RadioButtonList2=[10, *20, 50, 100, 9999])>
 # <RadioControl(ctl00$MainContent$politicalParties=[labour, conservative, libdem, ])>
  #<RadioControl(ctl00$MainContent$rblSalary=[unpaid, nmwormore, both])>
#  <RadioControl(ctl00$MainContent$rblJobs=[inlondon, outside, both])>
 # <SubmitControl(ctl00$MainContent$btnSearch=Go Search) (readonly)>>

#Select the 'All' option for a search
br["ctl00$MainContent$RadioButtonList2"] = ["9999"]
br["ctl00$MainContent$politicalParties"] = ["labour"]

response = br.submit()
html = response.read()
print html
root = lxml.html.fromstring(html)

#NOW ADAPT BELOW TO USE THE RESULTS OF RESPONSE

lis = root.cssselect('ul.searchresults li') # get all the <li> tags within <ul class="searchresults">
for li in lis:
    record = {} 
    if len(li):
        record["allhtml"] = li.text_content()
        divs = li.cssselect('div div') # get all the <div><div> tags within <ul class="searchresults"><li>
        record["link"] = divs[0].text_content()
        record["location"] = divs[1].text_content()
        record["salary"] = divs[2].text_content()
        record["posted"] = divs[3].text_content()
        hrefs = li.cssselect('div div strong a') # get all the <a> tags 
        record["href"] = hrefs[0].attrib.get('href')
        scraperwiki.sqlite.save(["allhtml"],record)

import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://www.w4mpjobs.org/SearchJobs.aspx?search=alljobs'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

br = mechanize.Browser()
response = br.open(base_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

#the options in the form are as follows (found by looking at the results of print above)
#  <TextControl(ctl00$MainContent$txtSearch=)>
#  <RadioControl(ctl00$MainContent$rbPoliticalParties=[Labour, Conservative, Lib Dem, Any])>
#  <RadioControl(ctl00$MainContent$RadioButtonList2=[10, *20, 50, 100, 9999])>
 # <RadioControl(ctl00$MainContent$politicalParties=[labour, conservative, libdem, ])>
  #<RadioControl(ctl00$MainContent$rblSalary=[unpaid, nmwormore, both])>
#  <RadioControl(ctl00$MainContent$rblJobs=[inlondon, outside, both])>
 # <SubmitControl(ctl00$MainContent$btnSearch=Go Search) (readonly)>>

#Select the 'All' option for a search
br["ctl00$MainContent$RadioButtonList2"] = ["9999"]
br["ctl00$MainContent$politicalParties"] = ["labour"]

response = br.submit()
html = response.read()
print html
root = lxml.html.fromstring(html)

#NOW ADAPT BELOW TO USE THE RESULTS OF RESPONSE

lis = root.cssselect('ul.searchresults li') # get all the <li> tags within <ul class="searchresults">
for li in lis:
    record = {} 
    if len(li):
        record["allhtml"] = li.text_content()
        divs = li.cssselect('div div') # get all the <div><div> tags within <ul class="searchresults"><li>
        record["link"] = divs[0].text_content()
        record["location"] = divs[1].text_content()
        record["salary"] = divs[2].text_content()
        record["posted"] = divs[3].text_content()
        hrefs = li.cssselect('div div strong a') # get all the <a> tags 
        record["href"] = hrefs[0].attrib.get('href')
        scraperwiki.sqlite.save(["allhtml"],record)

import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://www.w4mpjobs.org/SearchJobs.aspx?search=alljobs'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

br = mechanize.Browser()
response = br.open(base_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

#the options in the form are as follows (found by looking at the results of print above)
#  <TextControl(ctl00$MainContent$txtSearch=)>
#  <RadioControl(ctl00$MainContent$rbPoliticalParties=[Labour, Conservative, Lib Dem, Any])>
#  <RadioControl(ctl00$MainContent$RadioButtonList2=[10, *20, 50, 100, 9999])>
 # <RadioControl(ctl00$MainContent$politicalParties=[labour, conservative, libdem, ])>
  #<RadioControl(ctl00$MainContent$rblSalary=[unpaid, nmwormore, both])>
#  <RadioControl(ctl00$MainContent$rblJobs=[inlondon, outside, both])>
 # <SubmitControl(ctl00$MainContent$btnSearch=Go Search) (readonly)>>

#Select the 'All' option for a search
br["ctl00$MainContent$RadioButtonList2"] = ["9999"]
br["ctl00$MainContent$politicalParties"] = ["labour"]

response = br.submit()
html = response.read()
print html
root = lxml.html.fromstring(html)

#NOW ADAPT BELOW TO USE THE RESULTS OF RESPONSE

lis = root.cssselect('ul.searchresults li') # get all the <li> tags within <ul class="searchresults">
for li in lis:
    record = {} 
    if len(li):
        record["allhtml"] = li.text_content()
        divs = li.cssselect('div div') # get all the <div><div> tags within <ul class="searchresults"><li>
        record["link"] = divs[0].text_content()
        record["location"] = divs[1].text_content()
        record["salary"] = divs[2].text_content()
        record["posted"] = divs[3].text_content()
        hrefs = li.cssselect('div div strong a') # get all the <a> tags 
        record["href"] = hrefs[0].attrib.get('href')
        scraperwiki.sqlite.save(["allhtml"],record)

