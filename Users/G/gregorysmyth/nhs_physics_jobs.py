import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.jobs.nhs.uk/cgi-bin/advsearch?location_within=10;quick_search=1;internal_only=N;group_internal=N;redeployment_type=PUBLIC;stext=physics;stext_type=advert;location_include=;agency_name_include=;reqd_salary=;staff_group=all;jobtype=E;displayrows=80")
root = lxml.html.fromstring(html)

title = []
summary = []

for el in root.cssselect("dl.latest b"):
    title.append(el.text)
#    elb=root.cssselect("dd.jobAbstract")
#    data1 = { "titles" : el.text } # column name and value
#    scraperwiki.sqlite.save(["titles"], data1) # save the records one by one

for elb in root.cssselect("dd.jobAbstract"):
    summary.append(elb.text)
#    data2 = { "summary" : elb.text } # column name and value
#    scraperwiki.sqlite.save(["summary"], data2) # save the records one by one


#print data1
#print title[3]
#print title
#print summary

#print "<table>"
#print "<tr><th>Job title</th><th>Job summary</th>"
#for index in range(len(title)):
#    print "<tr>"
#    print "<td>", title[index], "</td>"
#    print "<td>", summary[index], "</td>"
#    print "</tr>"
#print "</table>"

#for index in range(len(title)):
#    print index
#    data = {
#            index['title'] : title[index],
#            index['summary'] : summary[index]
#    }
#data={}

#eg = root.cssselect("div#footer_inner strong")[0]
#print el
record={}
record['title'] = {}


for index in range(len(title)):
        record['title'][index]=(title[index])
        record['summary']=(summary[index])
#try
 #  self.features[cat]['tempHigh']
#except KeyError, e:
 #  self.features[cat]['tempHigh'] = {}
#print record
#scraperwiki.sqlite.save(['title'], record)

scraperwiki.sqlite.save(unique_keys=["titles"], data={"titles":record['title'], "summarys":record['summary']})
