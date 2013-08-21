import scraperwiki
import lxml.html
import re

url="http://www.ppbghana.org/contracts_results.asp?Ministry=%%25&Region=%%25&Agency=%%25&TNDType=%%25&ppb_date=356&Submit=Search&offset=%d"
base="http://www.ppbghana.org/"

def get_lxml(url):
    html=scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def get_pages(url):
    root=get_lxml(url)
    pstr=root.cssselect("td[colspan=7] td.bodytext")[0].text_content()
    pages=int(re.search("of ([0-9]+)",pstr).group(1))
    return range (0,pages,10)
    
def get_contract_urls(url):
    root=get_lxml(url)
    return ["%s%s"%(base,i.get("href")) for i in root.cssselect("td[colspan=7] td a")]

def clean_name(strn):
    remove=[":","(",")","/",".","\n","\r"]
    for r in remove:
        strn=strn.replace(r,"")
    return re.sub("[ ]+"," ",strn).strip()

def get_contract_details(url):
    data={"url":url}
    root=get_lxml(url)
    data["name"]=root.cssselect("td.subhead font")[0].text_content()
    for row in root.cssselect("tr.bodymain"):
        rd=row.cssselect("td")
        data[clean_name(rd[0].text_content().strip())]=rd[1].text_content().strip().replace("\n"," ").replace("\r","")
    if "Contract Award Price" in data.keys():
        data["Contract Award Price"]=float(re.sub("[^0-9.]","",data["Contract Award Price"]))
    if "Tender Type" in data.keys():
        scraperwiki.sqlite.save(unique_keys=["url"],data=data)

contract_urls=set(reduce(lambda x,y: x+y,[get_contract_urls(url%p) for p in get_pages(url%0)]))

for cu in contract_urls:
    try:
        get_contract_details(cu)
    except:
        pass

#get_contract_details("http://www.ppbghana.org/contracts.asp?Con_ID=5710")

