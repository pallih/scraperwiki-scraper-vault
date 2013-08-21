import scraperwiki
import lxml.html
import re

# Blank Python

base="http://www.logintanzania.net/monitor2a.asp"
request="http://www.logintanzania.net/report2a.asp"

def get_options(root,id):
    options=root.cssselect("select[id=%s] option"%id)
    return [o.get("value") for o in options]



def c2i(strn):
    strn=strn.replace(",","")
    try:
        return int(strn)
    except ValueError:
        return strn

def get_data(council_id,period):
    params={"periodcriteria":period,
        "lgacriteria":council_id}
    uid="%s-%s"%(period,council_id)
    html=scraperwiki.scrape(request,params)
    root=lxml.html.fromstring(html)
    council=root.cssselect("table table tr td font")[0].text_content().strip()
    population=int(re.search("equals: ([0-9,]+).",root.cssselect("p[align=LEFT]")[0].text_content()).group(1).replace(",",""))
    headers=root.cssselect("table table table tr")[0]
    columns=[c.text_content().strip().replace("(","").replace(")","") for c in headers.cssselect("td")]
    body=root.cssselect("table table table tr")[1:]
    columns=["period","council_id","council","population","uid"]+columns
    
    for row in body:
        r=[c2i(i.text_content()) for i in row.cssselect("td")]
        addvalues=[period,council_id,council,population,"%s-%s"%(uid,r[0])]
        data=dict(zip(columns,addvalues+r))
        print data
        scraperwiki.sqlite.save(unique_keys=["uid"],
            data=data)

html=scraperwiki.scrape(base)
root=lxml.html.fromstring(html)

periods=get_options(root,"periodcriteria")
councils=get_options(root,"lgacriteria")

for period in periods:
    for council_id in councils:
        try:
            get_data(council_id,period)
        except:
            print "could not get data for %s %s"%(council_id,period)
    