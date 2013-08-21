import scraperwiki
import lxml.html
import re

base="http://www.parliament.gh"
member_list="http://www.parliament.gh/members_list.php?"

def get_pages(url):
    html=scraperwiki.scrape(url)
    root=lxml.html.fromstring(html)
    return ["%s%s"%(base,i.get("href")) for i in root.cssselect("a.pagi")]
    
def get_member_urls(url):
    html=scraperwiki.scrape(url)
    root=lxml.html.fromstring(html)
    return ["%s/%s"%(base,i.get("href")) for i in root.cssselect("div.mp_repeater a")]

def get_member_info(url):
    data={"url":url}
    html=scraperwiki.scrape(url)
    root=lxml.html.fromstring(html)
    data["name"]=root.cssselect("div.mps_page_name_text_large")[0].text_content()
    ctext=root.cssselect("div.mps_page_name_text")[0].text_content()
    cmtch=re.search("MP for ([A-Za-z -]+) constituency, ([A-Za-z -]+) Region",ctext)
    data["constituency"]=cmtch.group(1)
    data["region"]=cmtch.group(2)
    tables=root.cssselect("td.line_under_table table tr")
    for table in tables:
        row=table.cssselect("td")
        if len(row)>1:
            data[row[0].text_content().strip().replace(":","")]=row[1].text_content().strip()
    data["image"]="%s%s"%(base,root.cssselect("td.content_text_column table img")[0].get("src"))
    data["Party"]=re.search("^([A-Za-z ]+)",data["Party"]).group(1).strip()
    scraperwiki.sqlite.save(unique_keys=["url"],data=data)
    
    
    
    
    
member_urls=set(reduce(lambda x,y: x+y,[get_member_urls(url) for url in get_pages(member_list)]))
for url in member_urls:
    get_member_info(url)  

