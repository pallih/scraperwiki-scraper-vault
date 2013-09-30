import scraperwiki
import lxml.html
import re

initial="http://www.necta.go.tz/2011/matokeo/csee2011/olevel.htm"
base="http://www.necta.go.tz/2011/matokeo/csee2011/"




def get_data_from_url(url):
    """ Get's the exam results from one page """
    root=lxml.html.fromstring(scraperwiki.scrape(url))
    school=root.cssselect("p[align=LEFT]")[1].text_content().strip() # find school name
    (school_id,school)=school.split(" ",1) # Split school name and school id
    if len(root.cssselect("table")) >1 :
        infotable= root.cssselect("table")[2]
        region=infotable.cssselect("td")[1].text_content().strip() #find region information if available
    else:
        region="n/a"
    results=root.cssselect("table")[0]
    hr=results.cssselect("table tr")[0]
    headers=[i.text_content().strip() for i in hr.cssselect("td b")] # get headers of results table
    headers=["school","school_id","region","url"]+headers
    rows=results.cssselect("table tr")[1:]
    for row in rows: # process results table on by one
        r=[i.text_content() for i in row.cssselect("td")]
        data=dict(zip(headers,[school,school_id,region,url]+r))
        scraperwiki.sqlite.save(unique_keys=["CNO"],data=data) #save the data

       
html=scraperwiki.scrape(initial)
root=lxml.html.fromstring(html)        

urls= ["%s%s"%(base,i.get("href")) for i in root.cssselect("table td a")]

for url in urls:
    get_data_from_url(url)
import scraperwiki
import lxml.html
import re

initial="http://www.necta.go.tz/2011/matokeo/csee2011/olevel.htm"
base="http://www.necta.go.tz/2011/matokeo/csee2011/"




def get_data_from_url(url):
    """ Get's the exam results from one page """
    root=lxml.html.fromstring(scraperwiki.scrape(url))
    school=root.cssselect("p[align=LEFT]")[1].text_content().strip() # find school name
    (school_id,school)=school.split(" ",1) # Split school name and school id
    if len(root.cssselect("table")) >1 :
        infotable= root.cssselect("table")[2]
        region=infotable.cssselect("td")[1].text_content().strip() #find region information if available
    else:
        region="n/a"
    results=root.cssselect("table")[0]
    hr=results.cssselect("table tr")[0]
    headers=[i.text_content().strip() for i in hr.cssselect("td b")] # get headers of results table
    headers=["school","school_id","region","url"]+headers
    rows=results.cssselect("table tr")[1:]
    for row in rows: # process results table on by one
        r=[i.text_content() for i in row.cssselect("td")]
        data=dict(zip(headers,[school,school_id,region,url]+r))
        scraperwiki.sqlite.save(unique_keys=["CNO"],data=data) #save the data

       
html=scraperwiki.scrape(initial)
root=lxml.html.fromstring(html)        

urls= ["%s%s"%(base,i.get("href")) for i in root.cssselect("table td a")]

for url in urls:
    get_data_from_url(url)
